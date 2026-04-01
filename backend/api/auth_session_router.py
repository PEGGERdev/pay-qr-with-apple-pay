from __future__ import annotations

from typing import Any, Dict, Type

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, ValidationError

from api.crud_base import GenericCrudRouter
from api.crud_validation import validation_error_details
from services.auth.session_runtime import (
    build_user_public_payload,
    create_registered_user,
    find_user_by_login,
    issue_auth_response_payload,
)
from services.shared import as_text


class AuthSessionRouter(GenericCrudRouter):
    def __init__(
        self,
        repository,
        register_model: Type[BaseModel],
        login_model: Type[BaseModel],
        user_public_model: Type[BaseModel],
        token_response_model: Type[BaseModel],
        token_extension,
        password_extension,
        prefix: str = "/auth",
        tags: list[str] | None = None,
    ) -> None:
        super().__init__(model=register_model, repository=repository, prefix=prefix, tags=tags or ["Auth"])
        self.register_model = register_model
        self.login_model = login_model
        self.user_public_model = user_public_model
        self.token_response_model = token_response_model
        self.token_extension = token_extension
        self.password_extension = password_extension

    def _to_user_public(self, user_doc: dict[str, Any]) -> BaseModel:
        payload = build_user_public_payload(user_doc)
        return self.user_public_model.model_validate(payload)

    def _to_auth_response(self, user_doc: dict[str, Any]) -> BaseModel:
        payload = issue_auth_response_payload(user_doc, self.token_extension)
        payload["user"] = self._to_user_public(user_doc)
        return self.token_response_model.model_validate(payload)

    def build(self) -> APIRouter:
        repository = self.repository
        router = APIRouter(prefix=self.prefix, tags=self.tags)

        @router.post("/register", response_model=self.token_response_model)
        @self.handle_exceptions
        async def register(payload: Dict[str, Any] = Body(...)):
            try:
                req = self.register_model.model_validate(payload)
            except ValidationError as exc:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=validation_error_details(exc),
                ) from exc

            if repository.find_one({"$or": [{"username": req.username.lower()}, {"email": req.email.lower()}]}):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")

            password_hash = self.password_extension.hash_password(req.password)
            user_doc = create_registered_user(repository, req, password_hash=password_hash)
            if not user_doc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")
            return self._to_auth_response(user_doc)

        @router.post("/login", response_model=self.token_response_model)
        @self.handle_exceptions
        async def login(payload: Dict[str, Any] = Body(...)):
            try:
                req = self.login_model.model_validate(payload)
            except ValidationError as exc:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=validation_error_details(exc),
                ) from exc

            user_doc = find_user_by_login(repository, req.username_or_email)
            if not user_doc:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/email or password")

            password_hash = as_text(user_doc.get("password_hash"))
            if not self.password_extension.verify_password(req.password, password_hash):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/email or password")

            return self._to_auth_response(user_doc)

        return router

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict, Type
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, ValidationError

from api.crud_base import GenericCrudRouter
from api.crud_validation import validation_error_details


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

    @staticmethod
    def _as_text(value: Any) -> str:
        return str(value or "").strip()

    def _normalize_login(self, value: Any) -> str:
        return self._as_text(value).lower()

    def _to_user_public(self, user_doc: dict[str, Any]) -> BaseModel:
        payload = {
            "id": self._as_text(user_doc.get("id")),
            "username": self._as_text(user_doc.get("username")),
            "email": self._as_text(user_doc.get("email")),
            "display_name": self._as_text(user_doc.get("display_name") or user_doc.get("username")),
            "created_at": user_doc.get("created_at") or datetime.now(UTC),
        }
        return self.user_public_model.model_validate(payload)

    def _to_auth_response(self, user_doc: dict[str, Any]) -> BaseModel:
        user_id = self._as_text(user_doc.get("id"))
        username = self._as_text(user_doc.get("username"))
        access_token = self.token_extension.issue_access_token(user_id=user_id, username=username)
        payload = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": self._to_user_public(user_doc),
        }
        return self.token_response_model.model_validate(payload)

    def _build_auth_user_document(self, req: BaseModel, password_hash: str) -> dict[str, Any]:
        username = self._normalize_login(getattr(req, "username", ""))
        email = self._normalize_login(getattr(req, "email", ""))
        display_name = self._as_text(getattr(req, "display_name", "")) or username

        return {
            "id": str(uuid4()),
            "username": username,
            "email": email,
            "password_hash": self._as_text(password_hash),
            "display_name": display_name,
            "created_at": datetime.now(UTC),
        }

    def _find_user_by_login(self, repository, username_or_email: str) -> dict[str, Any] | None:
        login = self._normalize_login(username_or_email)
        if not login:
            return None
        return repository.find_one({"$or": [{"username": login}, {"email": login}]})

    def _create_registered_user(self, repository, req: BaseModel, password_hash: str) -> dict[str, Any]:
        user_doc = self._build_auth_user_document(req, password_hash=password_hash)
        repository.insert_one(user_doc)
        return repository.find_one({"id": user_doc["id"]})

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
            user_doc = self._create_registered_user(repository, req, password_hash=password_hash)
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

            user_doc = self._find_user_by_login(repository, req.username_or_email)
            if not user_doc:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/email or password")

            password_hash = self._as_text(user_doc.get("password_hash"))
            if not self.password_extension.verify_password(req.password, password_hash):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/email or password")

            return self._to_auth_response(user_doc)

        return router

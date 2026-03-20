from __future__ import annotations

from typing import Any, Type, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel

from api.auth_session_router import AuthSessionRouter
from api.crud_authenticated import AuthenticatedCrudRouter
from api.crud_base import GenericCrudRouter

T = TypeVar("T", bound=BaseModel)


def router_create(model: Type[T], repository, prefix: str, tags: list[str] | None = None) -> APIRouter:
    return GenericCrudRouter(model=model, repository=repository, prefix=prefix, tags=tags).build()


def router_create_authenticated(
    model: Type[T],
    repository,
    prefix: str,
    auth_dependency: Any,
    tags: list[str] | None = None,
) -> APIRouter:
    return AuthenticatedCrudRouter(
        model=model,
        repository=repository,
        prefix=prefix,
        tags=tags,
        auth_dependency=auth_dependency,
    ).build()


def router_create_auth_sessions(
    repository,
    register_model: Type[BaseModel],
    login_model: Type[BaseModel],
    user_public_model: Type[BaseModel],
    token_response_model: Type[BaseModel],
    token_extension,
    password_extension,
    prefix: str = "/auth",
    tags: list[str] | None = None,
) -> APIRouter:
    return AuthSessionRouter(
        repository=repository,
        register_model=register_model,
        login_model=login_model,
        user_public_model=user_public_model,
        token_response_model=token_response_model,
        token_extension=token_extension,
        password_extension=password_extension,
        prefix=prefix,
        tags=tags,
    ).build()

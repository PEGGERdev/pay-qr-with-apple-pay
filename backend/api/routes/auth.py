from __future__ import annotations

from fastapi import APIRouter, Depends

from api.crud import router_create_auth_sessions
from core.config import app_config
from core.security import rate_limit_dependency
from repositories.auth_repository import get_auth_user_repository
from services.auth.password_service import password_service
from services.auth.token_service import token_service


_AUTH_ROUTER: APIRouter | None = None


def get_auth_router() -> APIRouter:
    global _AUTH_ROUTER
    if _AUTH_ROUTER is not None:
        return _AUTH_ROUTER

    from models.schemas import AuthTokenResponse, LoginRequest, RegisterRequest, UserPublic

    session_router = router_create_auth_sessions(
        repository=get_auth_user_repository(),
        register_model=RegisterRequest,
        login_model=LoginRequest,
        user_public_model=UserPublic,
        token_response_model=AuthTokenResponse,
        token_extension=token_service,
        password_extension=password_service,
        prefix="/auth",
        tags=["Auth"],
    )

    router = APIRouter(dependencies=[Depends(rate_limit_dependency("auth", app_config.auth_rate_limit))])
    router.include_router(session_router)
    _AUTH_ROUTER = router
    return _AUTH_ROUTER

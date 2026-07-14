from __future__ import annotations

from api.feature_builders import build_rate_limited_feature_spec
from api.crud import router_create_auth_sessions
from core.config import app_config
from core.security import rate_limit_dependency
from repositories.auth_repository import get_auth_user_repository
from services.auth.password_service import password_service
from services.auth.token_service import token_service


def build_auth_session_router():
    from models.schemas import AuthTokenResponse, LoginRequest, RegisterRequest, UserPublic

    return router_create_auth_sessions(
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
AUTH_FEATURE_SPEC = build_rate_limited_feature_spec(
    feature_id="auth",
    tags=("Auth",),
    rate_limit_dependency=rate_limit_dependency("auth", app_config.auth_rate_limit),
    included_router_builders=(build_auth_session_router,),
    test_targets=("backend/tests/test_auth_and_payments.py",),
)

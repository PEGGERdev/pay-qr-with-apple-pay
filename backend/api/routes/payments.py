from __future__ import annotations

from fastapi import Depends

from api.feature_builders import build_feature_route_spec, build_rate_limited_feature_spec
from api.crud import AuthenticatedCreateRouter
from core.config import app_config
from core.security import rate_limit_dependency
from models.schemas import PaymentSessionSummary
from repositories.payment_repository import get_payment_attempt_repository
from services.auth.current_user import get_current_user
from services.payment.payment_service import payment_service


def build_payments_create_router():
    from models.schemas import PaymentIntentCreateRequest, PaymentIntentResponse

    return AuthenticatedCreateRouter(
        model=PaymentIntentCreateRequest,
        repository=get_payment_attempt_repository(),
        prefix="/payments",
        auth_dependency=get_current_user,
        create_handler=payment_service.create_intent,
        tags=["Payments"],
        response_model=PaymentIntentResponse,
    ).build()


def build_payment_history_endpoint():
    def payment_history(current_user: dict = Depends(get_current_user)) -> list[PaymentSessionSummary]:
        return payment_service.list_payment_history(current_user)

    return payment_history


PAYMENTS_FEATURE_SPEC = build_rate_limited_feature_spec(
    feature_id="payments",
    tags=("Payments",),
    rate_limit_dependency=rate_limit_dependency("payments", app_config.payments_rate_limit),
    included_router_builders=(build_payments_create_router,),
    route_specs=(
        build_feature_route_spec(
            path="/payments/history",
            method="GET",
            endpoint=build_payment_history_endpoint(),
            response_model=list[PaymentSessionSummary],
        ),
    ),
    test_targets=("backend/tests/test_auth_and_payments.py",),
)

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.crud import AuthenticatedCreateRouter
from core.config import app_config
from core.security import rate_limit_dependency
from repositories.payment_repository import get_payment_attempt_repository
from services.auth.current_user import get_current_user
from services.payment.payment_service import payment_service


_PAYMENTS_ROUTER: APIRouter | None = None


def get_payments_router() -> APIRouter:
    global _PAYMENTS_ROUTER
    if _PAYMENTS_ROUTER is not None:
        return _PAYMENTS_ROUTER

    from models.schemas import PaymentIntentCreateRequest, PaymentIntentResponse, PaymentSessionSummary

    create_router = AuthenticatedCreateRouter(
        model=PaymentIntentCreateRequest,
        repository=get_payment_attempt_repository(),
        prefix="/payments",
        auth_dependency=get_current_user,
        create_handler=payment_service.create_intent,
        tags=["Payments"],
        response_model=PaymentIntentResponse,
    ).build()

    router = APIRouter(
        tags=["Payments"],
        dependencies=[Depends(rate_limit_dependency("payments", app_config.payments_rate_limit))],
    )
    router.include_router(create_router)

    @router.get("/payments/history", response_model=list[PaymentSessionSummary])
    def payment_history(
        _rate_limited=Depends(rate_limit_dependency("payments", app_config.payments_rate_limit)),
        current_user: dict = Depends(get_current_user),
    ):
        return payment_service.list_payment_history(current_user)

    _PAYMENTS_ROUTER = router
    return _PAYMENTS_ROUTER

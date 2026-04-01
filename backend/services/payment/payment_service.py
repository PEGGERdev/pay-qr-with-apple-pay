from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

try:
    import stripe
except ModuleNotFoundError:
    stripe = None

from core.config import app_config
from repositories.payment_repository import get_payment_attempt_repository
from services.payment.payment_runtime import (
    STATUS_BY_EVENT_TYPE,
    build_demo_intent_result,
    build_live_intent_result,
    build_payment_session_record,
    build_payment_status_update,
    sort_payment_history,
    user_id_from_payload,
)
from services.shared import as_text


class PaymentService:
    def __init__(self) -> None:
        self.demo_mode = app_config.demo_mode
        self.stripe_secret_key = app_config.stripe_secret_key
        self.stripe_webhook_secret = app_config.stripe_webhook_secret
        self.stripe_client = self._build_stripe_client()

    def _build_stripe_client(self):
        if not self.stripe_secret_key or stripe is None:
            return None
        return stripe.StripeClient(self.stripe_secret_key)

    def _record_session(self, *, invoice, current_user: dict[str, Any], result: dict[str, Any]) -> None:
        self._repository().insert_one(build_payment_session_record(invoice=invoice, current_user=current_user, result=result))

    @staticmethod
    def _repository():
        return get_payment_attempt_repository()

    def _build_demo_result(self, invoice) -> dict[str, Any]:
        return build_demo_intent_result(invoice)

    def _build_live_result(self, invoice, user_id: str) -> dict[str, Any]:
        if not self.stripe_client:
            return self._build_demo_result(invoice)
        return build_live_intent_result(self.stripe_client, invoice, user_id)

    def create_intent(self, payload, current_user: dict[str, Any]):
        invoice = payload.invoice
        user_id = user_id_from_payload(current_user)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

        result = self._build_demo_result(invoice) if self.demo_mode else self._build_live_result(invoice, user_id)
        self._record_session(invoice=invoice, current_user=current_user, result=result)
        return result

    def update_payment_status(self, *, payment_intent_id: str, status_value: str, stripe_event_id: str = "") -> bool:
        payment_intent_id = as_text(payment_intent_id)
        if not payment_intent_id:
            return False

        result = self._repository().update_fields(
            {"payment_intent_id": payment_intent_id},
            build_payment_status_update(status_value, stripe_event_id),
        )
        return bool(result.modified_count)

    def handle_stripe_webhook(self, payload: bytes, signature: str | None) -> dict[str, bool]:
        if stripe is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Stripe SDK is not installed")
        if not self.stripe_webhook_secret:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Stripe webhook signing secret is not configured")
        if not signature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Stripe-Signature header")

        try:
            event = stripe.Webhook.construct_event(payload=payload, sig_header=signature, secret=self.stripe_webhook_secret)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Stripe webhook signature: {exc}") from exc

        event_type = as_text(event.get("type"))
        status_value = STATUS_BY_EVENT_TYPE.get(event_type)
        if not status_value:
            return {"received": True}

        event_data = event.get("data") or {}
        event_object = event_data.get("object") or {}
        self.update_payment_status(
            payment_intent_id=str(event_object.get("id") or ""),
            status_value=status_value,
            stripe_event_id=str(event.get("id") or ""),
        )
        return {"received": True}

    def list_payment_history(self, current_user: dict[str, Any]):
        rows = self._repository().find_many({"user_id": str(current_user.get("id") or "")})
        return sort_payment_history(rows)


payment_service = PaymentService()

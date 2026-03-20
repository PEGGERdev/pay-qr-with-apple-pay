from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import HTTPException, status

try:
    import stripe
except ModuleNotFoundError:
    stripe = None

from core.config import app_config
from repositories.payment_repository import get_payment_attempt_repository


class PaymentService:
    STATUS_BY_EVENT_TYPE = {
        "payment_intent.succeeded": "succeeded",
        "payment_intent.payment_failed": "failed",
        "payment_intent.processing": "processing",
        "payment_intent.canceled": "canceled",
    }

    def __init__(self) -> None:
        self.demo_mode = app_config.demo_mode
        self.stripe_secret_key = app_config.stripe_secret_key
        self.stripe_webhook_secret = app_config.stripe_webhook_secret
        self.stripe_client = self._build_stripe_client()

    def _build_stripe_client(self):
        if not self.stripe_secret_key or stripe is None:
            return None
        return stripe.StripeClient(self.stripe_secret_key)

    @staticmethod
    def _user_id(current_user: dict[str, Any]) -> str:
        return str(current_user.get("id") or "").strip()

    def _record_session(self, *, invoice, current_user: dict[str, Any], result: dict[str, Any]) -> None:
        self._repository().insert_one(
            {
                "id": str(uuid4()),
                "user_id": self._user_id(current_user),
                "invoice_id": invoice.invoice_id,
                "merchant_name": invoice.merchant_name,
                "currency": invoice.currency,
                "amount_minor": invoice.amount_minor,
                "status": result["status"],
                "payment_intent_id": result["paymentIntentId"],
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
        )

    @staticmethod
    def _repository():
        return get_payment_attempt_repository()

    def _build_demo_result(self, invoice) -> dict[str, Any]:
        return {
            "status": "demo_ready",
            "clientSecret": f"pi_demo_secret_{uuid4().hex}",
            "paymentIntentId": f"pi_{uuid4().hex}",
            "demoMode": True,
            "merchantName": invoice.merchant_name,
        }

    def _build_live_result(self, invoice, user_id: str) -> dict[str, Any]:
        if not self.stripe_client:
            return self._build_demo_result(invoice)

        try:
            payment_intent = self.stripe_client.v1.payment_intents.create(
                amount=invoice.amount_minor,
                currency=invoice.currency.lower(),
                description=invoice.description,
                automatic_payment_methods={"enabled": True},
                metadata={
                    "invoice_id": invoice.invoice_id,
                    "merchant_name": invoice.merchant_name,
                    "user_id": user_id,
                },
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Stripe payment intent creation failed: {exc}",
            ) from exc

        return {
            "status": payment_intent.status or "requires_payment_method",
            "clientSecret": payment_intent.client_secret,
            "paymentIntentId": payment_intent.id,
            "demoMode": False,
            "merchantName": invoice.merchant_name,
        }

    def create_intent(self, payload, current_user: dict[str, Any]):
        invoice = payload.invoice
        user_id = self._user_id(current_user)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

        result = self._build_demo_result(invoice) if self.demo_mode else self._build_live_result(invoice, user_id)
        self._record_session(invoice=invoice, current_user=current_user, result=result)
        return result

    def update_payment_status(self, *, payment_intent_id: str, status_value: str, stripe_event_id: str = "") -> bool:
        payment_intent_id = str(payment_intent_id or "").strip()
        if not payment_intent_id:
            return False

        updated_fields = {
            "status": str(status_value or "unknown").strip() or "unknown",
            "updated_at": datetime.now(UTC),
        }
        if stripe_event_id:
            updated_fields["stripe_event_id"] = str(stripe_event_id).strip()

        result = self._repository().update_fields({"payment_intent_id": payment_intent_id}, updated_fields)
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

        event_type = str(event.get("type") or "").strip()
        status_value = self.STATUS_BY_EVENT_TYPE.get(event_type)
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
        rows.sort(key=lambda item: str(item.get("created_at") or ""), reverse=True)
        return rows


payment_service = PaymentService()

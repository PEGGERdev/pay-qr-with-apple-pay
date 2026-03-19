from __future__ import annotations

from datetime import UTC, datetime
import os
from typing import Any
from uuid import uuid4

from fastapi import HTTPException, status
import stripe

from repositories.payment_repository import get_payment_attempt_repository


class PaymentService:
    def __init__(self) -> None:
        self.demo_mode = str(os.getenv("DEMO_MODE") or "true").strip().lower() == "true"
        self.stripe_secret_key = str(os.getenv("STRIPE_SECRET_KEY") or "").strip()
        self.stripe_client = stripe.StripeClient(self.stripe_secret_key) if self.stripe_secret_key else None

    def _record_session(self, *, invoice, current_user: dict[str, Any], result: dict[str, Any]) -> None:
        repository = get_payment_attempt_repository()
        repository.insert_one(
            {
                "id": str(uuid4()),
                "user_id": str(current_user.get("id") or ""),
                "invoice_id": invoice.invoice_id,
                "merchant_name": invoice.merchant_name,
                "currency": invoice.currency,
                "amount_minor": invoice.amount_minor,
                "status": result["status"],
                "payment_intent_id": result["paymentIntentId"],
                "created_at": datetime.now(UTC),
            }
        )

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
        user_id = str(current_user.get("id") or "").strip()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

        result = self._build_demo_result(invoice) if self.demo_mode else self._build_live_result(invoice, user_id)
        self._record_session(invoice=invoice, current_user=current_user, result=result)
        return result

    def list_payment_history(self, current_user: dict[str, Any]):
        repository = get_payment_attempt_repository()
        rows = repository.find_many({"user_id": str(current_user.get("id") or "")})
        rows.sort(key=lambda item: str(item.get("created_at") or ""), reverse=True)
        return rows


payment_service = PaymentService()

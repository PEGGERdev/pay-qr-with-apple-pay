from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from services.shared import as_text, new_id, new_prefixed_id, utc_now

STATUS_BY_EVENT_TYPE = {
    "payment_intent.succeeded": "succeeded",
    "payment_intent.payment_failed": "failed",
    "payment_intent.processing": "processing",
    "payment_intent.canceled": "canceled",
}


def user_id_from_payload(current_user: dict[str, Any]) -> str:
    return as_text(current_user.get("id"))


def build_payment_session_record(*, invoice, current_user: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    timestamp = utc_now()
    return {
        "id": new_id(),
        "user_id": user_id_from_payload(current_user),
        "invoice_id": invoice.invoice_id,
        "merchant_name": invoice.merchant_name,
        "currency": invoice.currency,
        "amount_minor": invoice.amount_minor,
        "status": result["status"],
        "payment_intent_id": result["paymentIntentId"],
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def build_demo_intent_result(invoice) -> dict[str, Any]:
    return {
        "status": "demo_ready",
        "clientSecret": new_prefixed_id("pi_demo_secret_"),
        "paymentIntentId": new_prefixed_id("pi_"),
        "demoMode": True,
        "merchantName": invoice.merchant_name,
    }


def build_live_intent_result(stripe_client, invoice, user_id: str) -> dict[str, Any]:
    try:
        payment_intent = stripe_client.v1.payment_intents.create(
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


def build_payment_status_update(status_value: str, stripe_event_id: str = "") -> dict[str, Any]:
    updated_fields = {
        "status": as_text(status_value, "unknown") or "unknown",
        "updated_at": utc_now(),
    }
    if stripe_event_id:
        updated_fields["stripe_event_id"] = as_text(stripe_event_id)
    return updated_fields


def sort_payment_history(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows.sort(key=lambda item: str(item.get("created_at") or ""), reverse=True)
    return rows

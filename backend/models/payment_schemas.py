from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


def _to_minor_units(value: float) -> int:
    try:
        normalized = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValueError("Invalid invoice amount") from exc
    return int((normalized * 100).to_integral_value(rounding=ROUND_HALF_UP))


class InvoicePayload(BaseModel):
    invoice_id: str = Field(alias="invoiceId", min_length=1, max_length=120)
    merchant_name: str = Field(alias="merchantName", min_length=1, max_length=140)
    description: str = Field(default="QR invoice payment", max_length=500)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    country_code: str = Field(alias="countryCode", default="DE", min_length=2, max_length=2)
    amount: float = Field(gt=0)
    amount_minor: int = Field(alias="amountMinor", gt=0)
    raw_payload: str = Field(alias="rawPayload", default="", max_length=12000)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return str(value or "EUR").strip().upper()

    @field_validator("country_code")
    @classmethod
    def normalize_country_code(cls, value: str) -> str:
        return str(value or "DE").strip().upper()

    @model_validator(mode="after")
    def validate_amount_minor(self):
        expected_minor = _to_minor_units(self.amount)
        if self.amount_minor != expected_minor:
            raise ValueError("amountMinor must match amount in minor units")
        return self


class PaymentIntentCreateRequest(BaseModel):
    invoice: InvoicePayload


class PaymentIntentResponse(BaseModel):
    status: Literal["requires_payment_method", "succeeded", "demo_ready"]
    client_secret: str = Field(alias="clientSecret")
    payment_intent_id: str = Field(alias="paymentIntentId")
    demo_mode: bool = Field(alias="demoMode", default=False)
    merchant_name: str = Field(alias="merchantName")


class PaymentSessionRecord(BaseModel):
    id: str
    user_id: str
    invoice_id: str
    merchant_name: str
    currency: str
    amount_minor: int
    status: str
    payment_intent_id: str
    created_at: Optional[datetime] = None

    @field_validator("created_at")
    @classmethod
    def default_created_at(cls, value):
        return value or datetime.now(UTC)


class PaymentSessionSummary(BaseModel):
    id: str
    user_id: str
    invoice_id: str
    merchant_name: str
    currency: str
    amount_minor: int
    status: str
    payment_intent_id: str
    created_at: datetime

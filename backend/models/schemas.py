from __future__ import annotations

from datetime import UTC, datetime
import re
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


def _normalize_email(value: str) -> str:
    return str(value or "").strip().lower()


def _normalize_username(value: str) -> str:
    return str(value or "").strip().lower()


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    email: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=8, max_length=200)
    display_name: Optional[str] = Field(default=None, max_length=120)


class UserPublic(BaseModel):
    id: str
    username: str
    email: str
    display_name: str
    created_at: datetime


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class LoginRequest(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=200)
    password: str = Field(min_length=1, max_length=200)

    @field_validator("username_or_email")
    @classmethod
    def normalize_username_or_email(cls, value: str) -> str:
        return str(value or "").strip().lower()


class AuthUserRecord(BaseModel):
    id: str
    username: str = Field(min_length=3, max_length=40)
    email: str = Field(min_length=5, max_length=200)
    password_hash: str = Field(min_length=1, max_length=500)
    display_name: str = Field(min_length=1, max_length=120)
    created_at: Optional[datetime] = None

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        username = _normalize_username(value)
        if not re.fullmatch(r"[a-z0-9_.-]{3,40}", username):
            raise ValueError("Invalid username format")
        return username

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = _normalize_email(value)
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email

    @field_validator("created_at")
    @classmethod
    def default_created_at(cls, value):
        return value or datetime.now(UTC)


class InvoicePayload(BaseModel):
    invoice_id: str = Field(alias="invoiceId", min_length=1, max_length=120)
    merchant_name: str = Field(alias="merchantName", min_length=1, max_length=140)
    description: str = Field(default="QR invoice payment", max_length=500)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    country_code: str = Field(alias="countryCode", default="DE", min_length=2, max_length=2)
    amount: float = Field(gt=0)
    amount_minor: int = Field(alias="amountMinor", gt=0)
    raw_payload: str = Field(alias="rawPayload", default="", max_length=12000)


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

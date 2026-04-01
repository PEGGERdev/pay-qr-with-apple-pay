from __future__ import annotations

from datetime import datetime
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from services.shared import as_lower_text, utc_now


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
        return as_lower_text(value)


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
        username = as_lower_text(value)
        if not re.fullmatch(r"[a-z0-9_.-]{3,40}", username):
            raise ValueError("Invalid username format")
        return username

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = as_lower_text(value)
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email

    @field_validator("created_at")
    @classmethod
    def default_created_at(cls, value):
        return value or utc_now()

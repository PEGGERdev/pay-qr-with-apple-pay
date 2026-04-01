from __future__ import annotations

from dataclasses import dataclass
import os

from services.shared import as_lower_text, as_text


def _text(name: str, default: str = "") -> str:
    return as_text(os.getenv(name), default)


def _bool(name: str, default: bool = False) -> bool:
    return as_lower_text(_text(name, "true" if default else "false")) == "true"


def _int(name: str, default: int) -> int:
    return int(_text(name, str(default)))


def _csv(name: str, fallback: list[str]) -> list[str]:
    raw = [item.strip() for item in _text(name).split(",") if item.strip()]
    return raw or fallback


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    app_name: str
    app_host: str
    app_port: int
    cors_origins: list[str]
    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_minutes: int
    demo_mode: bool
    stripe_secret_key: str
    stripe_webhook_secret: str
    force_https: bool
    allowed_hosts: list[str]
    auth_rate_limit: int
    payments_rate_limit: int
    data_retention_days: int
    privacy_contact_email: str
    legal_company_name: str
    public_app_url: str

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    def validate(self) -> None:
        if self.jwt_expire_minutes <= 0:
            raise RuntimeError("JWT_EXPIRE_MINUTES must be greater than 0")
        if self.auth_rate_limit <= 0 or self.payments_rate_limit <= 0:
            raise RuntimeError("Rate limits must be greater than 0")
        if self.data_retention_days <= 0:
            raise RuntimeError("DATA_RETENTION_DAYS must be greater than 0")

        if self.is_production:
            if not self.public_app_url.startswith("https://"):
                raise RuntimeError("PUBLIC_APP_URL must use https in production")
            if self.demo_mode:
                raise RuntimeError("DEMO_MODE must be false in production")
            if self.jwt_secret in {"", "replace-me", "change-this-secret", "replace-with-a-long-random-secret"}:
                raise RuntimeError("JWT_SECRET must be changed in production")
            if len(self.jwt_secret) < 32:
                raise RuntimeError("JWT_SECRET must be at least 32 characters in production")
            if not self.stripe_secret_key.startswith("sk_"):
                raise RuntimeError("STRIPE_SECRET_KEY must be configured in production")
            if not self.stripe_webhook_secret.startswith("whsec_"):
                raise RuntimeError("STRIPE_WEBHOOK_SECRET must be configured in production")
            if any(origin.startswith("http://") for origin in self.cors_origins):
                raise RuntimeError("CORS_ORIGINS must use https in production")


def load_config() -> AppConfig:
    config = AppConfig(
        app_env=_text("APP_ENV", "development"),
        app_name=_text("APP_NAME", "Pay QR With Apple Pay"),
        app_host=_text("APP_HOST", "0.0.0.0"),
        app_port=_int("APP_PORT", 8000),
        cors_origins=_csv("CORS_ORIGINS", ["http://localhost:5173", "http://127.0.0.1:5173"]),
        jwt_secret=_text("JWT_SECRET", "change-this-secret"),
        jwt_algorithm=_text("JWT_ALGORITHM", "HS256"),
        jwt_expire_minutes=_int("JWT_EXPIRE_MINUTES", 60),
        demo_mode=_bool("DEMO_MODE", True),
        stripe_secret_key=_text("STRIPE_SECRET_KEY"),
        stripe_webhook_secret=_text("STRIPE_WEBHOOK_SECRET"),
        force_https=_bool("FORCE_HTTPS", False),
        allowed_hosts=_csv("ALLOWED_HOSTS", ["localhost", "127.0.0.1"]),
        auth_rate_limit=_int("AUTH_RATE_LIMIT", 20),
        payments_rate_limit=_int("PAYMENTS_RATE_LIMIT", 60),
        data_retention_days=_int("DATA_RETENTION_DAYS", 90),
        privacy_contact_email=_text("PRIVACY_CONTACT_EMAIL", "privacy@example.com"),
        legal_company_name=_text("LEGAL_COMPANY_NAME", "Your Company"),
        public_app_url=_text("PUBLIC_APP_URL", "http://localhost:5173"),
    )
    config.validate()
    return config


app_config = load_config()

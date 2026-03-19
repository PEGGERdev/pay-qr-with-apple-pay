from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def isolated_storage(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("APP_STORAGE_DIR", str(tmp_path / ".data"))
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("DEMO_MODE", "true")
    monkeypatch.setenv("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
    monkeypatch.setenv("PUBLIC_APP_URL", "http://testserver")

    from core import config as config_module
    from repositories import auth_repository, payment_repository
    from core import application
    from api.routes import auth as auth_routes
    from api.routes import payments as payment_routes
    from services.auth import token_service
    from services.payment import payment_service
    import main as main_module

    importlib.reload(config_module)
    importlib.reload(token_service)
    importlib.reload(payment_service)
    importlib.reload(auth_routes)
    importlib.reload(payment_routes)
    importlib.reload(application)
    importlib.reload(main_module)

    auth_repository._AUTH_REPOSITORY = None
    payment_repository._PAYMENT_REPOSITORY = None
    auth_routes._AUTH_ROUTER = None
    payment_routes._PAYMENTS_ROUTER = None
    token_service.token_service = token_service.TokenService()
    payment_service.payment_service = payment_service.PaymentService()
    application.get_auth_router = __import__("api.routes.auth", fromlist=["get_auth_router"]).get_auth_router
    application.get_payments_router = __import__("api.routes.payments", fromlist=["get_payments_router"]).get_payments_router


@pytest.fixture
def client() -> TestClient:
    from main import create_app

    return TestClient(create_app())


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def invoice_payload(reference: str = "INV-TEST") -> dict[str, object]:
    return {
        "invoice": {
            "invoiceId": reference,
            "merchantName": "Cafe Test",
            "description": "Test invoice",
            "currency": "EUR",
            "countryCode": "DE",
            "amount": 12.5,
            "amountMinor": 1250,
            "rawPayload": json.dumps({"reference": reference}),
        }
    }

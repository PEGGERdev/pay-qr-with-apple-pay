from __future__ import annotations

from services.payment import payment_service as payment_service_module
from tests.data.scenarios import invoice_payload
from tests.harness.api_helpers import auth_headers, register_user


def test_register_and_login(client):
    register = register_user(client)
    assert register.status_code == 200
    payload = register.json()
    assert payload["access_token"]
    assert payload["user"]["username"] == "demo-user"

    login = client.post(
        "/auth/login",
        json={"username_or_email": "demo@example.com", "password": "demo-pass-123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == "demo@example.com"


def test_duplicate_register_is_rejected(client):
    first = register_user(client)
    second = register_user(client)

    assert first.status_code == 200
    assert second.status_code == 409


def test_payments_require_authentication(client):
    create = client.post("/payments", json=invoice_payload())
    history = client.get("/payments/history")

    assert create.status_code == 401
    assert history.status_code == 401


def test_authenticated_payment_is_recorded_in_history(client):
    register = register_user(client, username="demo-user-2", email="demo2@example.com")
    token = register.json()["access_token"]

    create = client.post("/payments", json=invoice_payload("INV-200"), headers=auth_headers(token))
    history = client.get("/payments/history", headers=auth_headers(token))

    assert create.status_code == 200
    assert create.json()["demoMode"] is True
    assert history.status_code == 200
    rows = history.json()
    assert len(rows) == 1
    assert rows[0]["invoice_id"] == "INV-200"


def test_payment_rejects_mismatched_minor_amount(client):
    register = register_user(client, username="demo-user-3", email="demo3@example.com")
    token = register.json()["access_token"]
    payload = invoice_payload("INV-BAD-AMOUNT")
    payload["invoice"]["amountMinor"] = 1

    response = client.post("/payments", json=payload, headers=auth_headers(token))

    assert response.status_code == 422
    assert "amountMinor must match amount" in str(response.json())


def test_payment_status_updates_after_reconciliation(client):
    register = register_user(client, username="demo-user-4", email="demo4@example.com")
    token = register.json()["access_token"]

    create = client.post("/payments", json=invoice_payload("INV-RECON"), headers=auth_headers(token))
    payment_intent_id = create.json()["paymentIntentId"]

    updated = payment_service_module.payment_service.update_payment_status(
        payment_intent_id=payment_intent_id,
        status_value="succeeded",
        stripe_event_id="evt_test_123",
    )
    history = client.get("/payments/history", headers=auth_headers(token))

    assert updated is True
    assert history.status_code == 200
    assert history.json()[0]["status"] == "succeeded"

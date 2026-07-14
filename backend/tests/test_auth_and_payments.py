from __future__ import annotations

def register_user(client, username: str = "demo-user", email: str = "demo@example.com"):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "demo-pass-123",
            "display_name": "Demo User",
        },
    )


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
            "rawPayload": '{"reference": "%s"}' % reference,
        }
    }


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

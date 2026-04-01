from __future__ import annotations

from fastapi.testclient import TestClient

from tests.data.scenarios import auth_registration_payload


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register_user(client: TestClient, username: str = "demo-user", email: str = "demo@example.com"):
    return client.post("/auth/register", json=auth_registration_payload(username=username, email=email))

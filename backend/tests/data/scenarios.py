from __future__ import annotations

import json


def auth_registration_payload(username: str = "demo-user", email: str = "demo@example.com") -> dict[str, str]:
    return {
        "username": username,
        "email": email,
        "password": "demo-pass-123",
        "display_name": "Demo User",
    }


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

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from services.shared import as_lower_text, as_text, new_id, utc_now


def build_user_public_payload(user_doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": as_text(user_doc.get("id")),
        "username": as_text(user_doc.get("username")),
        "email": as_text(user_doc.get("email")),
        "display_name": as_text(user_doc.get("display_name") or user_doc.get("username")),
        "created_at": user_doc.get("created_at") or utc_now(),
    }


def issue_auth_response_payload(user_doc: dict[str, Any], token_extension) -> dict[str, Any]:
    user_id = as_text(user_doc.get("id"))
    username = as_text(user_doc.get("username"))
    return {
        "access_token": token_extension.issue_access_token(user_id=user_id, username=username),
        "token_type": "bearer",
        "user": build_user_public_payload(user_doc),
    }


def build_auth_user_document(req: BaseModel, password_hash: str) -> dict[str, Any]:
    username = as_lower_text(getattr(req, "username", ""))
    email = as_lower_text(getattr(req, "email", ""))
    display_name = as_text(getattr(req, "display_name", "")) or username
    return {
        "id": new_id(),
        "username": username,
        "email": email,
        "password_hash": as_text(password_hash),
        "display_name": display_name,
        "created_at": utc_now(),
    }


def find_user_by_login(repository, username_or_email: str) -> dict[str, Any] | None:
    login = as_lower_text(username_or_email)
    if not login:
        return None
    return repository.find_one({"$or": [{"username": login}, {"email": login}]})


def create_registered_user(repository, req: BaseModel, password_hash: str) -> dict[str, Any] | None:
    user_doc = build_auth_user_document(req, password_hash=password_hash)
    repository.insert_one(user_doc)
    return repository.find_one({"id": user_doc["id"]})

from __future__ import annotations

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from repositories.auth_repository import get_auth_user_repository
from services.shared import as_text
from . import token_service as token_service_module


bearer_scheme = HTTPBearer(auto_error=False)


def _find_user_by_id(user_id: str) -> dict[str, Any] | None:
    text = as_text(user_id)
    if not text:
        return None
    return get_auth_user_repository().find_one({"id": text})


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> dict[str, Any]:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = as_text(credentials.credentials) if credentials else ""
    if not token:
        raise credentials_error

    try:
        payload = token_service_module.token_service.decode_access_token(token)
    except JWTError as exc:
        raise credentials_error from exc

    user_id = as_text(payload.get("sub"))
    if not user_id:
        raise credentials_error

    user_doc = _find_user_by_id(user_id)
    if not user_doc:
        raise credentials_error

    return user_doc

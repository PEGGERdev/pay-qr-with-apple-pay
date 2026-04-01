from __future__ import annotations

from uuid import uuid4


def new_id() -> str:
    return str(uuid4())


def new_prefixed_id(prefix: str) -> str:
    return f"{prefix}{uuid4().hex}"

from __future__ import annotations

from typing import Any


def as_text(value: Any, default: str = "") -> str:
    return str(default if value is None else value).strip()


def as_lower_text(value: Any, default: str = "") -> str:
    return as_text(value, default).lower()


def as_upper_text(value: Any, default: str = "") -> str:
    return as_text(value, default).upper()

from __future__ import annotations

import json
from typing import Any

from pydantic import ValidationError


def validation_error_details(exc: ValidationError) -> list[dict[str, Any]]:
    return json.loads(exc.json())

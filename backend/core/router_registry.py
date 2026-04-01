from __future__ import annotations

from typing import Callable

from fastapi import APIRouter

from api.routes.auth import get_auth_router
from api.routes.payments import get_payments_router

ROUTER_BUILDERS: tuple[Callable[[], APIRouter], ...] = (
    get_auth_router,
    get_payments_router,
)


def get_registered_route_routers() -> list[APIRouter]:
    return [build_router() for build_router in ROUTER_BUILDERS]

from __future__ import annotations

from api.auth_session_router import AuthSessionRouter
from api.crud_authenticated import AuthenticatedCreateRouter, AuthenticatedCrudRouter
from api.crud_base import GenericCrudRouter
from api.crud_factories import router_create, router_create_auth_sessions, router_create_authenticated
from api.crud_types import CrudRouteConfig, CrudRouteConfigs, CrudRouteEnabled, CrudRouteWrappers
from api.crud_validation import validation_error_details

__all__ = [
    "AuthenticatedCreateRouter",
    "AuthenticatedCrudRouter",
    "AuthSessionRouter",
    "CrudRouteConfig",
    "CrudRouteConfigs",
    "CrudRouteEnabled",
    "CrudRouteWrappers",
    "GenericCrudRouter",
    "router_create",
    "router_create_authenticated",
    "router_create_auth_sessions",
    "validation_error_details",
]

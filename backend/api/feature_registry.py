from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from fastapi import APIRouter, status


@dataclass(frozen=True)
class FeatureRouteSpec:
    path: str
    method: str
    endpoint: Callable[..., Any]
    response_model: Any = None
    status_code: int = status.HTTP_200_OK


@dataclass(frozen=True)
class ApiFeatureSpec:
    feature_id: str
    test_targets: tuple[str, ...]
    tags: tuple[str, ...] = ()
    dependencies: tuple[Any, ...] = ()
    included_router_builders: tuple[Callable[[], APIRouter], ...] = ()
    route_specs: tuple[FeatureRouteSpec, ...] = ()


def build_feature_router(feature: ApiFeatureSpec) -> APIRouter:
    router = APIRouter(tags=list(feature.tags), dependencies=list(feature.dependencies))

    for router_builder in feature.included_router_builders:
        router.include_router(router_builder())

    for route in feature.route_specs:
        router.add_api_route(
            route.path,
            route.endpoint,
            methods=[route.method],
            response_model=route.response_model,
            status_code=route.status_code,
        )

    return router


def build_feature_routers(feature_specs: list[ApiFeatureSpec]) -> list[APIRouter]:
    return [build_feature_router(feature) for feature in feature_specs]

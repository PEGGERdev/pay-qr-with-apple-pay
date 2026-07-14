from __future__ import annotations

from typing import Any, Callable

from fastapi import Depends

from api.feature_registry import ApiFeatureSpec, FeatureRouteSpec


def build_rate_limited_feature_spec(*, feature_id: str, tags: tuple[str, ...], rate_limit_dependency: Any, included_router_builders: tuple[Callable, ...] = (), route_specs: tuple[FeatureRouteSpec, ...] = (), test_targets: tuple[str, ...]) -> ApiFeatureSpec:
    return ApiFeatureSpec(
        feature_id=feature_id,
        tags=tags,
        dependencies=(Depends(rate_limit_dependency),),
        included_router_builders=included_router_builders,
        route_specs=route_specs,
        test_targets=test_targets,
    )


def build_feature_route_spec(*, path: str, method: str, endpoint: Callable[..., Any], response_model: Any):
    return FeatureRouteSpec(
        path=path,
        method=method,
        endpoint=endpoint,
        response_model=response_model,
    )

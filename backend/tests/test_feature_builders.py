from fastapi.params import Depends as DependsParam

from api.feature_builders import build_feature_route_spec, build_rate_limited_feature_spec
from api.feature_registry import build_feature_router


def noop_dependency():
    return True


def test_build_feature_router_includes_declared_routes_and_dependencies():
    def ping_endpoint():
        return {"status": "ok"}

    feature = build_rate_limited_feature_spec(
        feature_id="test-feature",
        tags=("Test",),
        rate_limit_dependency=noop_dependency,
        route_specs=(
            build_feature_route_spec(
                path="/ping",
                method="GET",
                endpoint=ping_endpoint,
                response_model=None,
            ),
        ),
        test_targets=("backend/tests/test_feature_builders.py",),
    )

    router = build_feature_router(feature)

    assert len(router.routes) == 1
    assert router.routes[0].path == "/ping"
    assert isinstance(router.dependencies[0], DependsParam)

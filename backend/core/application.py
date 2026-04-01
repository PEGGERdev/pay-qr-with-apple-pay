from __future__ import annotations

import os

from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from core.config import app_config
from core.registry import get_routers
from core.router_registry import get_registered_route_routers
from repositories.mongo_repository import ping_mongo
from core.security import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Payment application booting...")
    yield
    print("[SHUTDOWN] Payment application shutting down...")


class Routing:
    def __init__(self) -> None:
        self._app = FastAPI(lifespan=lifespan)
        self._app.add_middleware(SecurityHeadersMiddleware)
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=app_config.cors_origins,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
        )
        self._app.add_middleware(TrustedHostMiddleware, allowed_hosts=app_config.allowed_hosts)
        if app_config.force_https:
            self._app.add_middleware(HTTPSRedirectMiddleware)

        for router in get_routers():
            self._app.include_router(router)

        for router in get_registered_route_routers():
            self._app.include_router(router)

        @self._app.get("/health", tags=["Health"])
        def healthcheck(response: Response) -> dict[str, object]:
            storage_ok = ping_mongo()
            response.status_code = status.HTTP_200_OK if storage_ok else status.HTTP_503_SERVICE_UNAVAILABLE
            return {
                "status": "ok" if storage_ok else "degraded",
                "environment": app_config.app_env,
                "services": {
                    "api": "ok",
                    "storage": "ok" if storage_ok else "unavailable",
                },
            }

    def get_app(self) -> FastAPI:
        return self._app

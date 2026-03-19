from __future__ import annotations

import os

from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from api.routes.auth import get_auth_router
from api.routes.payments import get_payments_router
from core.registry import get_routers
from repositories.mongo_repository import ping_mongo


def _cors_origins() -> list[str]:
    raw = str(os.getenv("CORS_ORIGINS") or "").strip()
    if not raw:
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["http://localhost:5173", "http://127.0.0.1:5173"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Payment application booting...")
    yield
    print("[SHUTDOWN] Payment application shutting down...")


class Routing:
    def __init__(self) -> None:
        self._app = FastAPI(lifespan=lifespan)
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=_cors_origins(),
            allow_methods=["*"],
            allow_headers=["*"],
        )

        for router in get_routers():
            self._app.include_router(router)

        self._app.include_router(get_auth_router())
        self._app.include_router(get_payments_router())

        @self._app.get("/health", tags=["Health"])
        def healthcheck(response: Response) -> dict[str, object]:
            storage_ok = ping_mongo()
            response.status_code = status.HTTP_200_OK if storage_ok else status.HTTP_503_SERVICE_UNAVAILABLE
            return {
                "status": "ok" if storage_ok else "degraded",
                "services": {
                    "api": "ok",
                    "storage": "ok" if storage_ok else "unavailable",
                },
            }

    def get_app(self) -> FastAPI:
        return self._app

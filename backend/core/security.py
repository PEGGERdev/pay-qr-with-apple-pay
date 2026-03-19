from __future__ import annotations

from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from threading import Lock
from typing import Callable

from fastapi import Depends, HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(self), microphone=(), geolocation=()"
        response.headers["Cache-Control"] = "no-store"
        return response


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._requests: dict[str, deque[datetime]] = defaultdict(deque)
        self._lock = Lock()

    def hit(self, key: str, limit: int, window_seconds: int) -> None:
        now = datetime.now(UTC)
        threshold = now - timedelta(seconds=window_seconds)

        with self._lock:
          queue = self._requests[key]
          while queue and queue[0] < threshold:
              queue.popleft()
          if len(queue) >= limit:
              raise HTTPException(
                  status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                  detail="Rate limit exceeded. Please try again later.",
              )
          queue.append(now)


rate_limiter = InMemoryRateLimiter()


def rate_limit_dependency(scope: str, limit: int, window_seconds: int = 60) -> Callable:
    async def dependency(request: Request):
        client_host = getattr(getattr(request, "client", None), "host", "unknown")
        rate_limiter.hit(f"{scope}:{client_host}", limit, window_seconds)

    return dependency

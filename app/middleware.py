"""FastAPI middleware for CORS and Prometheus metrics."""

import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config import settings
from app.utils.prometheus import http_request_duration, http_request_count


def setup_cors(app) -> None:
    """Setup CORS middleware.

    Args:
        app: FastAPI application instance.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and collect metrics."""
        if not settings.prometheus_enabled:
            return await call_next(request)

        # Skip metrics endpoint
        if request.url.path == "/metrics":
            return await call_next(request)

        method = request.method
        path = request.url.path

        # Track request
        http_request_count.labels(method=method, endpoint=path).inc()

        # Track duration
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        http_request_duration.labels(method=method, endpoint=path).observe(duration)

        return response


def setup_prometheus(app) -> None:
    """Setup Prometheus middleware.

    Args:
        app: FastAPI application instance.
    """
    if settings.prometheus_enabled:
        app.add_middleware(PrometheusMiddleware)

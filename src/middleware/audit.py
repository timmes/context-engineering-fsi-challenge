"""Audit logging middleware — mandatory for PCI-DSS compliance."""

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger()


class AuditMiddleware(BaseHTTPMiddleware):
    """Middleware that adds correlation IDs and logs all requests for audit trail.

    PCI-DSS Req 10: Track and monitor all access to network resources and cardholder data.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Generate correlation ID for tracing across services
        correlation_id = str(uuid.uuid4())
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        start_time = time.perf_counter()

        # Bind context for all logs within this request
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "unknown",
        )

        logger.info("request_started")

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                "request_failed",
                error=str(exc),
                duration_ms=round((time.perf_counter() - start_time) * 1000, 2),
            )
            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Add tracing headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response

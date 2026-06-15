"""
Custom Middleware

Request/response processing and error handling.
"""

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process request and log details.
        """
        start_time = time.time()
        
        # Log request
        logger.info(
            f"{request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown",
            }
        )

        response = await call_next(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": duration,
            }
        )
        
        response.headers["X-Process-Time"] = str(duration)
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for global error handling.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Handle errors globally.
        """
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"Unhandled error: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

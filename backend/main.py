#!/usr/bin/env python
"""
Busibot FastAPI Application Entry Point

Main application factory and configuration.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base
from app.api import api_router
from app.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting Busibot Application")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Database initialized")
    logger.info(f"🔧 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🌐 API URL: {settings.API_URL}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Busibot Application")
    await engine.dispose()
    logger.info("✅ Database connection closed")


def create_app() -> FastAPI:
    """
    Application factory function.
    Creates and configures the FastAPI application.
    """
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # ============================================
    # CORS Middleware
    # ============================================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Page"],
    )

    # ============================================
    # Security Middleware
    # ============================================
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS,
    )

    # ============================================
    # Compression Middleware
    # ============================================
    app.add_middleware(
        GZIPMiddleware,
        minimum_size=1000,
    )

    # ============================================
    # Custom Middleware
    # ============================================
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)

    # ============================================
    # Routes
    # ============================================
    app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")

    # ============================================
    # Health Check Endpoint
    # ============================================
    @app.get("/api/v1/health", tags=["Health"])
    async def health_check():
        """Health check endpoint for container orchestration."""
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "version": "1.0.0",
        }

    # ============================================
    # Root Endpoint
    # ============================================
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "message": "Welcome to Busibot API",
            "title": settings.API_TITLE,
            "description": settings.API_DESCRIPTION,
            "version": "1.0.0",
            "docs": "/api/docs",
            "redoc": "/api/redoc",
        }

    # ============================================
    # Exception Handlers
    # ============================================
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )

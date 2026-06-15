"""
API Routes Package

All API endpoint definitions and routing.
"""

from fastapi import APIRouter

# Import routers
from app.api.v1 import (
    auth_router,
    ideas_router,
    plans_router,
    market_research_router,
    forecasts_router,
    investors_router,
    chat_router,
    users_router,
)

# Create main API router
api_router = APIRouter()

# Include version 1 routers
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    ideas_router,
    prefix="/ideas",
    tags=["Ideas"],
)

api_router.include_router(
    plans_router,
    prefix="/plans",
    tags=["Business Plans"],
)

api_router.include_router(
    market_research_router,
    prefix="/market-research",
    tags=["Market Research"],
)

api_router.include_router(
    forecasts_router,
    prefix="/forecasts",
    tags=["Financial Forecasts"],
)

api_router.include_router(
    investors_router,
    prefix="/investors",
    tags=["Investors"],
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)

__all__ = ["api_router"]

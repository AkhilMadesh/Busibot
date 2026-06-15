"""
API V1 Routes

Version 1 API endpoint definitions.
"""

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.ideas import router as ideas_router
from app.api.v1.plans import router as plans_router
from app.api.v1.market_research import router as market_research_router
from app.api.v1.forecasts import router as forecasts_router
from app.api.v1.investors import router as investors_router
from app.api.v1.chat import router as chat_router

__all__ = [
    "auth_router",
    "users_router",
    "ideas_router",
    "plans_router",
    "market_research_router",
    "forecasts_router",
    "investors_router",
    "chat_router",
]

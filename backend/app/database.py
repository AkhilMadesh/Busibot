"""
Database Configuration and Session Management

SQLAlchemy setup with async support.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.config import settings

# ============================================
# Database Engine
# ============================================
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_pre_ping=True,
    future=True,
)

# ============================================
# Session Factory
# ============================================
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ============================================
# Declarative Base
# ============================================
Base = declarative_base()


# ============================================
# Database Dependency
# ============================================
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

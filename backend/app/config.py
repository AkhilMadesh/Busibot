"""
Application Configuration

Settings management using pydantic-settings.
"""

from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings and environment variables.
    """

    # ============================================
    # API Configuration
    # ============================================
    API_TITLE: str = "Busibot API"
    API_DESCRIPTION: str = "AI-Powered Business Administration Platform"
    API_VERSION: str = "v1"
    API_URL: str = "http://localhost:8000"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    RELOAD: bool = False

    # ============================================
    # Security
    # ============================================
    SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 30
    BCRYPT_ROUNDS: int = 12

    # ============================================
    # CORS Configuration
    # ============================================
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5050",
    ]
    TRUSTED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "*.busibot.io",
    ]

    # ============================================
    # Database Configuration
    # ============================================
    DATABASE_URL: str = Field(
        "postgresql://user:password@localhost:5432/busibot_db"
    )
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_RECYCLE: int = 3600
    DATABASE_POOL_TIMEOUT: int = 30

    # ============================================
    # Redis Configuration
    # ============================================
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""
    REDIS_TIMEOUT: int = 5

    # ============================================
    # Email Configuration
    # ============================================
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@busibot.io"
    SMTP_FROM_NAME: str = "Busibot"

    # ============================================
    # LLM Configuration
    # ============================================
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = "gpt-4-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000

    ANTHROPIC_API_KEY: str = Field(default="")
    ANTHROPIC_MODEL: str = "claude-3-sonnet-20240229"

    LANGCHAIN_API_KEY: str = Field(default="")
    LANGCHAIN_TRACING_V2: bool = True

    # ============================================
    # Vector Database Configuration
    # ============================================
    VECTOR_DB_TYPE: str = "pinecone"  # or "supabase-pgvector"
    PINECONE_API_KEY: str = Field(default="")
    PINECONE_ENVIRONMENT: str = "gcp-starter"
    PINECONE_INDEX_NAME: str = "busibot-embeddings"

    # ============================================
    # AWS Configuration
    # ============================================
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = Field(default="")
    AWS_SECRET_ACCESS_KEY: str = Field(default="")
    S3_BUCKET_NAME: str = "busibot-files"

    # ============================================
    # Stripe Configuration
    # ============================================
    STRIPE_SECRET_KEY: str = Field(default="")
    STRIPE_PUBLIC_KEY: str = Field(default="")
    STRIPE_WEBHOOK_SECRET: str = Field(default="")

    # ============================================
    # Logging Configuration
    # ============================================
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str = Field(default="")

    # ============================================
    # Feature Flags
    # ============================================
    FEATURE_PITCH_DECK_GENERATION: bool = True
    FEATURE_INVESTOR_MATCHING: bool = True
    FEATURE_FINANCIAL_FORECASTS: bool = True
    FEATURE_MARKET_RESEARCH: bool = True
    FEATURE_ADVANCED_ANALYTICS: bool = True

    # ============================================
    # Rate Limiting
    # ============================================
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # ============================================
    # Pagination
    # ============================================
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

    @validator("DATABASE_URL")
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL."""
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key length."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v


@lru_cache()
def get_settings() -> Settings:
    """
    Get settings instance (cached).
    """
    return Settings()


# Create settings instance
settings = get_settings()

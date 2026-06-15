"""
Authentication Schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignupRequest(BaseModel):
    """User signup request schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)

    class Config:
        example = {
            "email": "user@busibot.io",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe",
        }


class LoginRequest(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str

    class Config:
        example = {
            "email": "user@busibot.io",
            "password": "securepassword123",
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        example = {
            "access_token": "eyJhbGc...",
            "refresh_token": "eyJhbGc...",
            "token_type": "bearer",
        }

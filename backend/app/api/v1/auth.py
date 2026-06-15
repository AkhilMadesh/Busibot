"""
Authentication Endpoints

User registration, login, token refresh, and logout.
"""

from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from app.services.auth import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    User registration endpoint.
    
    Creates a new user account.
    """
    try:
        user, access_token, refresh_token = await auth_service.signup(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            db=db,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    User login endpoint.
    
    Authenticates user and returns JWT tokens.
    """
    try:
        user, access_token, refresh_token = await auth_service.login(
            email=request.email,
            password=request.password,
            db=db,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh JWT token endpoint.
    
    Returns new access token using refresh token.
    """
    try:
        access_token = await auth_service.refresh_token(
            refresh_token=request.refresh_token,
            db=db,
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=request.refresh_token,
            token_type="bearer",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.post("/logout")
async def logout(
    token: str = Depends(lambda: None),
):
    """
    Logout endpoint.
    
    Invalidates the user's session.
    """
    return {"message": "Successfully logged out"}

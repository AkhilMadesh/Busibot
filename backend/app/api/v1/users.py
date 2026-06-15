"""
Users Endpoints

User profile management and settings.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.users import UserResponse, UserUpdateRequest
from app.services.users import UserService
from app.auth.dependencies import get_current_user

router = APIRouter()
user_service = UserService()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get current user profile.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    request: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Update user profile.
    """
    try:
        user = await user_service.update_user(
            user_id=current_user.id,
            **request.dict(exclude_unset=True),
            db=db,
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

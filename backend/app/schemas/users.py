"""
User Schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """User update request schema."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None

    class Config:
        from_attributes = True

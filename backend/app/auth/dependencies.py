"""
Authentication Dependencies

Dependencies for route protection.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.auth.jwt_handler import verify_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
):
    """
    Get current authenticated user from JWT token.
    """
    try:
        token = credentials.credentials
        user_id = verify_token(token)
        return {"id": user_id}  # Simplified for now
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

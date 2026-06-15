"""
Investor Matching Endpoints

Investor recommendation and matching.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.investors import InvestorMatchResponse
from app.services.investors import InvestorService
from app.auth.dependencies import get_current_user

router = APIRouter()
investor_service = InvestorService()


@router.get("/match/{idea_id}", response_model=List[InvestorMatchResponse])
async def get_investor_matches(
    idea_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get matching investors for an idea.
    """
    try:
        matches = await investor_service.find_matches(
            idea_id=idea_id,
            user_id=current_user.id,
            db=db,
        )
        return matches
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )

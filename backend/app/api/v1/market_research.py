"""
Market Research Endpoints

Market analysis and research data.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.market_research import MarketResearchResponse
from app.services.market_research import MarketResearchService
from app.auth.dependencies import get_current_user

router = APIRouter()
research_service = MarketResearchService()


@router.get("/{idea_id}", response_model=MarketResearchResponse)
async def get_market_research(
    idea_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get market research for an idea.
    """
    try:
        research = await research_service.get_research(
            idea_id=idea_id,
            user_id=current_user.id,
            db=db,
        )
        return research
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research not found",
        )

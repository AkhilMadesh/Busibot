"""
Business Ideas Endpoints

Idea generation, validation, and management.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.ideas import (
    IdeaGenerateRequest,
    IdeaValidateRequest,
    IdeaResponse,
)
from app.services.ideas import IdeaService
from app.auth.dependencies import get_current_user

router = APIRouter()
idea_service = IdeaService()


@router.post("/generate", response_model=IdeaResponse)
async def generate_idea(
    request: IdeaGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Generate business ideas.
    
    Uses AI to generate innovative business ideas based on industry and preferences.
    """
    try:
        idea = await idea_service.generate_idea(
            user_id=current_user.id,
            industry=request.industry,
            interests=request.interests,
            budget=request.budget,
            db=db,
        )
        return idea
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate idea",
        )


@router.post("/{idea_id}/validate", response_model=dict)
async def validate_idea(
    idea_id: str,
    request: IdeaValidateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Validate a business idea.
    
    Performs comprehensive validation including market analysis, competition, risk assessment.
    """
    try:
        validation_result = await idea_service.validate_idea(
            idea_id=idea_id,
            user_id=current_user.id,
            db=db,
        )
        return validation_result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )


@router.get("/", response_model=List[IdeaResponse])
async def list_ideas(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    List user's business ideas.
    """
    ideas = await idea_service.list_ideas(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        db=db,
    )
    return ideas


@router.get("/{idea_id}", response_model=IdeaResponse)
async def get_idea(
    idea_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get specific business idea details.
    """
    idea = await idea_service.get_idea(
        idea_id=idea_id,
        user_id=current_user.id,
        db=db,
    )
    if not idea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found",
        )
    return idea

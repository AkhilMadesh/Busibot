"""
Business Plans Endpoints

Business plan generation and management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.plans import (
    BusinessPlanGenerateRequest,
    BusinessPlanResponse,
)
from app.services.plans import BusinessPlanService
from app.auth.dependencies import get_current_user

router = APIRouter()
plan_service = BusinessPlanService()


@router.post("/generate", response_model=BusinessPlanResponse)
async def generate_business_plan(
    request: BusinessPlanGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Generate business plan.
    """
    try:
        plan = await plan_service.generate_plan(
            user_id=current_user.id,
            idea_id=request.idea_id,
            db=db,
        )
        return plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate business plan",
        )


@router.get("/", response_model=List[BusinessPlanResponse])
async def list_business_plans(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    List user's business plans.
    """
    plans = await plan_service.list_plans(
        user_id=current_user.id,
        db=db,
    )
    return plans

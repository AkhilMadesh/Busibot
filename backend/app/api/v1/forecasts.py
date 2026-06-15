"""
Financial Forecasts Endpoints

Financial projections and forecasting.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.forecasts import (
    ForecastGenerateRequest,
    ForecastResponse,
)
from app.services.forecasts import ForecastService
from app.auth.dependencies import get_current_user

router = APIRouter()
forecast_service = ForecastService()


@router.post("/generate", response_model=ForecastResponse)
async def generate_forecast(
    request: ForecastGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Generate financial forecast.
    """
    try:
        forecast = await forecast_service.generate_forecast(
            user_id=current_user.id,
            idea_id=request.idea_id,
            db=db,
        )
        return forecast
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate forecast",
        )

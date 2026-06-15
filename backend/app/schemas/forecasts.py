"""
Financial Forecasts Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime


class ForecastGenerateRequest(BaseModel):
    """Generate forecast request."""
    idea_id: str
    initial_investment: Optional[float] = None
    monthly_burn_rate: Optional[float] = None


class FinancialProjection(BaseModel):
    """Financial projection for a period."""
    period: str
    revenue: float
    expenses: float
    profit: float
    cash_flow: float


class ForecastResponse(BaseModel):
    """Forecast response schema."""
    id: str
    idea_id: str
    break_even_month: int
    runway_months: float
    projections: List[FinancialProjection]
    assumptions: Dict[str, str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

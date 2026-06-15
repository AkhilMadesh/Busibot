"""
Business Plans Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BusinessPlanGenerateRequest(BaseModel):
    """Generate business plan request."""
    idea_id: str
    company_name: Optional[str] = None
    target_market: Optional[str] = None


class BusinessPlanResponse(BaseModel):
    """Business plan response schema."""
    id: str
    idea_id: str
    title: str
    executive_summary: str
    market_analysis: str
    business_model: str
    go_to_market_strategy: str
    financial_projections: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

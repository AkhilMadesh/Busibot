"""
Market Research Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CompetitorInfo(BaseModel):
    """Competitor information."""
    name: str
    market_share: Optional[float] = None
    strengths: List[str]
    weaknesses: List[str]


class MarketResearchResponse(BaseModel):
    """Market research response schema."""
    id: str
    idea_id: str
    market_size: str
    growth_rate: float
    market_trends: List[str]
    competitors: List[CompetitorInfo]
    customer_segments: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

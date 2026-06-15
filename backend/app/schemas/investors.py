"""
Investor Schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class InvestorMatchResponse(BaseModel):
    """Investor match response schema."""
    id: str
    name: str
    type: str  # VC, Angel, Accelerator
    industry_focus: List[str]
    investment_range: str
    match_score: float
    reasoning: str
    contact_email: Optional[EmailStr] = None
    website: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

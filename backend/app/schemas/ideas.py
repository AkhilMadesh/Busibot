"""
Business Ideas Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class IdeaGenerateRequest(BaseModel):
    """Generate idea request schema."""
    industry: str
    interests: List[str]
    budget: float
    target_market: Optional[str] = None


class IdeaValidationResult(BaseModel):
    """Idea validation result."""
    market_size: str
    competition_level: str
    feasibility_score: float
    recommendation: str


class IdeaResponse(BaseModel):
    """Idea response schema."""
    id: str
    title: str
    description: str
    industry: str
    problem: str
    solution: str
    market_size: Optional[str] = None
    validation: Optional[IdeaValidationResult] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IdeaValidateRequest(BaseModel):
    """Validate idea request schema."""
    market_focus: Optional[str] = None

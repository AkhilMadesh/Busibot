"""
Chat Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatMessageRequest(BaseModel):
    """Chat message request."""
    conversation_id: Optional[str] = None
    message: str


class ChatMessageResponse(BaseModel):
    """Chat message response."""
    id: str
    conversation_id: str
    user_message: str
    assistant_response: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Conversation response schema."""
    id: str
    title: str
    messages: List[ChatMessageResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

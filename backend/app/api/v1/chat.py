"""
Chat Endpoints

Conversational AI and chat interface.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationResponse,
)
from app.services.chat import ChatService
from app.auth.dependencies import get_current_user

router = APIRouter()
chat_service = ChatService()


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Send a chat message.
    """
    try:
        message = await chat_service.process_message(
            user_id=current_user.id,
            conversation_id=request.conversation_id,
            message=request.message,
            db=db,
        )
        return message
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    List user's conversations.
    """
    conversations = await chat_service.list_conversations(
        user_id=current_user.id,
        db=db,
    )
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Get conversation with messages.
    """
    conversation = await chat_service.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user.id,
        db=db,
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation

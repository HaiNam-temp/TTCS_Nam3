"""Conversation routes layer (HTTP only)."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List

try:
    from logger_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from ..auth import get_current_user
from ..schemas import ChatRequest, ChatResponse, ConversationCreate, ConversationDTO, MessageDTO
from ..services.container import conversation_service

router = APIRouter()

@router.post("/conversations/", response_model=ConversationDTO, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new conversation"""
    logger.info("[conversation_routes.py][create_conversation] Start route call")
    try:
        result = conversation_service.create_conversation(conversation.title or "New Conversation", current_user)
        logger.info("[conversation_routes.py][create_conversation] End status=success conversation_id=%s", result.id)
        return result
    except HTTPException:
        logger.error("[conversation_routes.py][create_conversation] End status=error type=http_exception")
        raise
    except Exception:
        logger.exception("[conversation_routes.py][create_conversation] End status=error")
        raise

@router.get("/conversations/", response_model=List[ConversationDTO])
async def get_conversations(current_user: Dict = Depends(get_current_user)):
    """Get all conversations for current user"""
    logger.info("[conversation_routes.py][get_conversations] Start route call")
    try:
        result = conversation_service.get_conversations(current_user)
        logger.info("[conversation_routes.py][get_conversations] End status=success count=%s", len(result))
        return result
    except HTTPException:
        logger.error("[conversation_routes.py][get_conversations] End status=error type=http_exception")
        raise
    except Exception:
        logger.exception("[conversation_routes.py][get_conversations] End status=error")
        raise

@router.get("/conversations/{conversation_id}", response_model=ConversationDTO)
async def get_conversation(
    conversation_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get a specific conversation"""
    logger.info("[conversation_routes.py][get_conversation] Start route call conversation_id=%s", conversation_id)
    try:
        result = conversation_service.get_conversation(conversation_id, current_user)
        logger.info("[conversation_routes.py][get_conversation] End status=success conversation_id=%s", conversation_id)
        return result
    except HTTPException:
        logger.error("[conversation_routes.py][get_conversation] End status=error type=http_exception conversation_id=%s", conversation_id)
        raise
    except Exception:
        logger.exception("[conversation_routes.py][get_conversation] End status=error conversation_id=%s", conversation_id)
        raise

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a conversation"""
    logger.info("[conversation_routes.py][delete_conversation] Start route call conversation_id=%s", conversation_id)
    try:
        conversation_service.delete_conversation(conversation_id, current_user)
        logger.info("[conversation_routes.py][delete_conversation] End status=success conversation_id=%s", conversation_id)
        return None
    except HTTPException:
        logger.error("[conversation_routes.py][delete_conversation] End status=error type=http_exception conversation_id=%s", conversation_id)
        raise
    except Exception:
        logger.exception("[conversation_routes.py][delete_conversation] End status=error conversation_id=%s", conversation_id)
        raise

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageDTO])
async def get_messages(
    conversation_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get all messages in a conversation"""
    logger.info("[conversation_routes.py][get_messages] Start route call conversation_id=%s", conversation_id)
    try:
        result = conversation_service.get_messages(conversation_id, current_user)
        logger.info("[conversation_routes.py][get_messages] End status=success count=%s conversation_id=%s", len(result), conversation_id)
        return result
    except HTTPException:
        logger.error("[conversation_routes.py][get_messages] End status=error type=http_exception conversation_id=%s", conversation_id)
        raise
    except Exception:
        logger.exception("[conversation_routes.py][get_messages] End status=error conversation_id=%s", conversation_id)
        raise

@router.post("/conversations/{conversation_id}/chat", response_model=ChatResponse)
async def chat(
    conversation_id: str,
    chat_request: ChatRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Send a message and get AI response"""
    logger.info("[conversation_routes.py][chat] Start route call conversation_id=%s", conversation_id)
    try:
        result = conversation_service.chat(conversation_id, chat_request, current_user)
        logger.info("[conversation_routes.py][chat] End status=success conversation_id=%s message_id=%s", conversation_id, result.message_id)
        return result
    except HTTPException:
        logger.error("[conversation_routes.py][chat] End status=error type=http_exception conversation_id=%s", conversation_id)
        raise
    except Exception:
        logger.exception("[conversation_routes.py][chat] End status=error conversation_id=%s", conversation_id)
        raise

"""
Chat Router
Handles chat API endpoints for the Todo AI Chatbot.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.services.tool_execution_handler import ToolExecutionHandler
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
conversation_service = ConversationService()
message_service = MessageService()
tool_handler = ToolExecutionHandler()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to continue existing conversation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    tool_executed: bool = Field(False, description="Whether a tool was executed")
    tool_name: Optional[str] = Field(None, description="Name of executed tool")
    intent: Optional[str] = Field(None, description="Detected intent")


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(user_id: str, request: ChatRequest):
    """
    Stateless chat endpoint.

    Flow:
    1. Fetch or create conversation
    2. Retrieve conversation history
    3. Detect intent and execute tools
    4. Store messages
    5. Return response

    Args:
        user_id: The ID of the user
        request: Chat request with message and optional conversation_id

    Returns:
        ChatResponse with assistant's response and metadata
    """
    try:
        # Validate user_id
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required"
            )

        # Validate message
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="message is required"
            )

        # Step 1: Get or create conversation
        conversation_id = request.conversation_id

        if conversation_id:
            # Verify conversation exists
            conv_result = await conversation_service.get_conversation(
                conversation_id,
                user_id
            )

            if not conv_result.get("success"):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversation not found: {conv_result.get('error')}"
                )
        else:
            # Create new conversation
            conv_result = await conversation_service.create_conversation(user_id)

            if not conv_result.get("success"):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create conversation: {conv_result.get('error')}"
                )

            conversation_id = conv_result["conversation"]["id"]

        # Step 2: Retrieve conversation history
        history_result = await conversation_service.get_conversation_history(
            conversation_id,
            user_id
        )

        conversation_history = []
        if history_result.get("success"):
            conversation_history = history_result.get("messages", [])

        # Step 3: Store user message
        user_msg_result = await message_service.store_message(
            conversation_id,
            user_id,
            "user",
            request.message
        )

        if not user_msg_result.get("success"):
            logger.error(f"Failed to store user message: {user_msg_result.get('error')}")

        # Step 4: Execute tool based on intent
        execution_result = await tool_handler.execute_from_message(
            user_id,
            request.message,
            conversation_history
        )

        # Step 5: Generate response
        response_text = execution_result.get("response", "I'm not sure how to help with that.")
        tool_executed = execution_result.get("tool_executed", False)
        tool_name = execution_result.get("tool_name")
        intent = execution_result.get("intent")

        # Step 6: Store assistant message
        assistant_msg_result = await message_service.store_message(
            conversation_id,
            user_id,
            "assistant",
            response_text
        )

        if not assistant_msg_result.get("success"):
            logger.error(f"Failed to store assistant message: {assistant_msg_result.get('error')}")

        # Step 7: Return response
        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            tool_executed=tool_executed,
            tool_name=tool_name,
            intent=intent
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}/history")
async def get_history(user_id: str, conversation_id: str):
    """
    Get conversation history.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation

    Returns:
        Conversation history with messages
    """
    try:
        result = await conversation_service.get_conversation_history(
            conversation_id,
            user_id
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.get("error", "Conversation not found")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get history error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

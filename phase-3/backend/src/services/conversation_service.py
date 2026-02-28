"""
Conversation Service
Handles conversation creation, message storage, and history retrieval.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.models.conversation import Conversation
from src.models.message import Message
from src.db_context import get_db_session


class ConversationService:
    """
    Service for managing conversations and messages.
    Provides stateless operations for conversation lifecycle.
    """

    async def create_conversation(self, user_id: str) -> Dict[str, Any]:
        """
        Create a new conversation for a user.

        Args:
            user_id: The ID of the user

        Returns:
            Dict containing the created conversation details
        """
        try:
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required and cannot be empty"
                }

            async with get_db_session() as session:
                # Create new conversation
                new_conversation = Conversation(user_id=user_id.strip())

                session.add(new_conversation)
                await session.flush()
                await session.refresh(new_conversation)

                return {
                    "success": True,
                    "conversation": {
                        "id": str(new_conversation.id),
                        "user_id": new_conversation.user_id,
                        "created_at": new_conversation.created_at.isoformat() if new_conversation.created_at else None
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create conversation: {str(e)}"
            }

    async def get_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get a conversation by ID.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user (for authorization)

        Returns:
            Dict containing the conversation details
        """
        try:
            if not conversation_id or not conversation_id.strip():
                return {
                    "success": False,
                    "error": "conversation_id is required and cannot be empty"
                }

            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required and cannot be empty"
                }

            # Validate UUID format
            try:
                conv_uuid = UUID(conversation_id.strip())
            except ValueError:
                return {
                    "success": False,
                    "error": "conversation_id must be a valid UUID"
                }

            async with get_db_session() as session:
                # Find the conversation
                query = select(Conversation).where(
                    Conversation.id == conv_uuid,
                    Conversation.user_id == user_id.strip()
                )
                result = await session.execute(query)
                conversation = result.scalar_one_or_none()

                if not conversation:
                    return {
                        "success": False,
                        "error": f"Conversation {conversation_id} not found for user {user_id}"
                    }

                return {
                    "success": True,
                    "conversation": {
                        "id": str(conversation.id),
                        "user_id": conversation.user_id,
                        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
                        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get conversation: {str(e)}"
            }

    async def get_conversation_history(
        self,
        conversation_id: str,
        user_id: str,
        limit: Optional[int] = 50
    ) -> Dict[str, Any]:
        """
        Get conversation history (all messages in a conversation).

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user (for authorization)
            limit: Maximum number of messages to retrieve

        Returns:
            Dict containing list of messages
        """
        try:
            if not conversation_id or not conversation_id.strip():
                return {
                    "success": False,
                    "error": "conversation_id is required and cannot be empty"
                }

            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required and cannot be empty"
                }

            # Validate UUID format
            try:
                conv_uuid = UUID(conversation_id.strip())
            except ValueError:
                return {
                    "success": False,
                    "error": "conversation_id must be a valid UUID"
                }

            async with get_db_session() as session:
                # Verify conversation exists and belongs to user
                conv_query = select(Conversation).where(
                    Conversation.id == conv_uuid,
                    Conversation.user_id == user_id.strip()
                )
                conv_result = await session.execute(conv_query)
                conversation = conv_result.scalar_one_or_none()

                if not conversation:
                    return {
                        "success": False,
                        "error": f"Conversation {conversation_id} not found for user {user_id}"
                    }

                # Get messages
                msg_query = select(Message).where(
                    Message.conversation_id == conv_uuid
                ).order_by(Message.created_at.asc()).limit(limit)

                msg_result = await session.execute(msg_query)
                messages = msg_result.scalars().all()

                # Format messages
                message_list = [
                    {
                        "id": str(msg.id),
                        "role": msg.role,
                        "content": msg.content,
                        "created_at": msg.created_at.isoformat() if msg.created_at else None
                    }
                    for msg in messages
                ]

                return {
                    "success": True,
                    "conversation_id": str(conversation.id),
                    "messages": message_list,
                    "count": len(message_list)
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get conversation history: {str(e)}"
            }

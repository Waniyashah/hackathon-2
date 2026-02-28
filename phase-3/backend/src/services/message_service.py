"""
Message Service
Handles message storage and retrieval operations.
"""

from typing import Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.models.message import Message
from src.models.conversation import Conversation
from src.db_context import get_db_session


class MessageService:
    """
    Service for managing messages within conversations.
    Provides stateless operations for message storage and retrieval.
    """

    async def store_message(
        self,
        conversation_id: str,
        user_id: str,
        role: str,
        content: str
    ) -> Dict[str, Any]:
        """
        Store a new message in a conversation.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            role: The role of the message sender ('user' or 'assistant')
            content: The content of the message

        Returns:
            Dict containing the stored message details
        """
        try:
            # Validate inputs
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

            if role not in ["user", "assistant", "system"]:
                return {
                    "success": False,
                    "error": "role must be 'user', 'assistant', or 'system'"
                }

            if not content or not content.strip():
                return {
                    "success": False,
                    "error": "content is required and cannot be empty"
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

                # Create new message
                new_message = Message(
                    conversation_id=conv_uuid,
                    user_id=user_id.strip(),
                    role=role,
                    content=content.strip()
                )

                session.add(new_message)
                await session.flush()
                await session.refresh(new_message)

                return {
                    "success": True,
                    "message": {
                        "id": str(new_message.id),
                        "conversation_id": str(new_message.conversation_id),
                        "user_id": new_message.user_id,
                        "role": new_message.role,
                        "content": new_message.content,
                        "created_at": new_message.created_at.isoformat() if new_message.created_at else None
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to store message: {str(e)}"
            }

    async def store_messages_batch(
        self,
        conversation_id: str,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Store multiple messages in a conversation at once.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            Dict containing the stored messages details
        """
        try:
            # Validate inputs
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

            if not messages or len(messages) == 0:
                return {
                    "success": False,
                    "error": "messages list cannot be empty"
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

                # Create messages
                stored_messages = []
                for msg_data in messages:
                    role = msg_data.get("role")
                    content = msg_data.get("content")

                    if role not in ["user", "assistant", "system"]:
                        continue

                    if not content or not content.strip():
                        continue

                    new_message = Message(
                        conversation_id=conv_uuid,
                        user_id=user_id.strip(),
                        role=role,
                        content=content.strip()
                    )

                    session.add(new_message)
                    await session.flush()
                    await session.refresh(new_message)

                    stored_messages.append({
                        "id": str(new_message.id),
                        "role": new_message.role,
                        "content": new_message.content,
                        "created_at": new_message.created_at.isoformat() if new_message.created_at else None
                    })

                return {
                    "success": True,
                    "messages": stored_messages,
                    "count": len(stored_messages)
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to store messages: {str(e)}"
            }

    async def get_message(
        self,
        message_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get a specific message by ID.

        Args:
            message_id: The ID of the message
            user_id: The ID of the user (for authorization)

        Returns:
            Dict containing the message details
        """
        try:
            if not message_id or not message_id.strip():
                return {
                    "success": False,
                    "error": "message_id is required and cannot be empty"
                }

            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required and cannot be empty"
                }

            # Validate UUID format
            try:
                msg_uuid = UUID(message_id.strip())
            except ValueError:
                return {
                    "success": False,
                    "error": "message_id must be a valid UUID"
                }

            async with get_db_session() as session:
                # Find the message
                query = select(Message).where(
                    Message.id == msg_uuid,
                    Message.user_id == user_id.strip()
                )
                result = await session.execute(query)
                message = result.scalar_one_or_none()

                if not message:
                    return {
                        "success": False,
                        "error": f"Message {message_id} not found for user {user_id}"
                    }

                return {
                    "success": True,
                    "message": {
                        "id": str(message.id),
                        "conversation_id": str(message.conversation_id),
                        "user_id": message.user_id,
                        "role": message.role,
                        "content": message.content,
                        "created_at": message.created_at.isoformat() if message.created_at else None
                    }
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get message: {str(e)}"
            }

import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """
    Service layer for interacting with Google Gemini API.
    Handles conversation context, tool calling, and response generation.
    """

    def __init__(self):
        """Initialize the Gemini API client."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response from Gemini based on conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            tools: Optional list of tool definitions for function calling

        Returns:
            Dict containing response text and any tool calls
        """
        try:
            # Build conversation context
            context = self._build_context(messages)

            # Generate response
            if tools:
                # TODO: Implement tool calling when Gemini supports it
                response = self.model.generate_content(context)
            else:
                response = self.model.generate_content(context)

            return {
                "content": response.text,
                "tool_calls": [],  # Will be populated when tool calling is implemented
                "finish_reason": "stop"
            }

        except Exception as e:
            raise Exception(f"Error generating response from Gemini: {str(e)}")

    def _build_context(self, messages: List[Dict[str, str]]) -> str:
        """
        Build conversation context from message history.

        Args:
            messages: List of message dicts with 'role' and 'content' keys

        Returns:
            Formatted context string
        """
        context_parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "user":
                context_parts.append(f"User: {content}")
            elif role == "assistant":
                context_parts.append(f"Assistant: {content}")
            elif role == "system":
                context_parts.append(f"System: {content}")

        return "\n\n".join(context_parts)

    async def detect_intent(self, user_message: str) -> Dict[str, Any]:
        """
        Detect user intent from natural language message.

        Args:
            user_message: The user's message

        Returns:
            Dict containing detected intent and parameters
        """
        # Intent detection prompt
        intent_prompt = f"""
        Analyze the following user message and determine the intent.
        Possible intents: add_task, list_tasks, complete_task, delete_task, update_task, general_chat

        User message: "{user_message}"

        Respond with just the intent name and any relevant parameters in JSON format.
        Example: {{"intent": "add_task", "title": "Buy groceries", "description": "Get milk and bread"}}
        """

        try:
            response = self.model.generate_content(intent_prompt)
            # TODO: Parse JSON response properly
            return {
                "intent": "general_chat",
                "raw_response": response.text
            }
        except Exception as e:
            return {
                "intent": "general_chat",
                "error": str(e)
            }

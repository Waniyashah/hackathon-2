"""
Intent Service
Handles intent detection from natural language and mapping to MCP tools.
"""

from typing import Dict, Any, List, Optional
import re
import json
from src.services.gemini_service import GeminiService


class IntentService:
    """
    Service for detecting user intent from natural language messages
    and mapping them to appropriate MCP tool calls.
    """

    def __init__(self):
        """Initialize the intent service with Gemini."""
        self.gemini_service = GeminiService()

        # Intent patterns for comprehensive natural language understanding
        self.intent_patterns = {
            "add_task": [
                # Direct add/create patterns
                r"add\s+(?:a\s+)?tasks?\s+to",
                r"create\s+(?:a\s+)?tasks?\s+to",
                r"new\s+tasks?\s+to",
                # Remember patterns
                r"remember\s+to",
                r"i\s+need\s+to\s+remember\s+to",
                r"remind\s+me\s+to",
                # Need patterns
                r"i\s+need\s+to",
                r"i\s+have\s+to",
                r"i\s+should",
                r"i\s+must",
                # Todo patterns
                r"todo:",
                r"to\s+do:",
            ],
            "list_tasks": [
                # Show/list all tasks
                r"show\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?(?:tasks?|taks?)",
                r"list\s+(?:all\s+)?(?:my\s+)?(?:tasks?|taks?)",
                r"see\s+(?:all\s+)?(?:my\s+)?(?:tasks?|taks?)",
                r"view\s+(?:all\s+)?(?:my\s+)?(?:tasks?|taks?)",
                r"get\s+(?:all\s+)?(?:my\s+)?(?:tasks?|taks?)",
                r"display\s+(?:all\s+)?(?:my\s+)?(?:tasks?|taks?)",
                # What patterns
                r"what\s+(?:are\s+)?(?:my\s+)?(?:tasks?|taks?)",
                r"what'?s?\s+(?:my\s+)?(?:tasks?|taks?)",
                # Pending patterns
                r"what'?s?\s+pending",
                r"show\s+(?:me\s+)?pending",
                r"list\s+pending",
                # Completed patterns
                r"what\s+have\s+i\s+completed",
                r"show\s+(?:me\s+)?completed",
                r"list\s+completed",
                # Simple patterns
                r"^(?:list|show|tasks?|taks?)$",
                r"my\s+(?:tasks?|taks?)$",
            ],
            "complete_task": [
                # Mark as complete/done
                r"mark\s+(?:the\s+)?tasks?\s+\d+\s+(?:as\s+)?(?:done|complete|completed|finished)",
                r"mark\s+tasks?\s+\d+",
                # Complete/finish patterns
                r"complete\s+(?:the\s+)?tasks?\s+\d+",
                r"finish\s+(?:the\s+)?tasks?\s+\d+",
                r"done\s+(?:with\s+)?(?:the\s+)?tasks?\s+\d+",
                # Task X is done
                r"tasks?\s+\d+\s+(?:is\s+)?(?:done|complete|completed|finished)",
                # Update/change to complete
                r"(?:update|change)\s+tasks?\s+\d+\s+(?:as|to)\s+(?:complete|completed|done)",
            ],
            "delete_task": [
                # Delete/remove patterns
                r"delete\s+(?:the\s+)?tasks?\s+\d+",
                r"remove\s+(?:the\s+)?tasks?\s+\d+",
                r"cancel\s+(?:the\s+)?tasks?\s+\d+",
                r"get\s+rid\s+of\s+(?:the\s+)?tasks?\s+\d+",
                # Delete by name (will need special handling)
                r"delete\s+the\s+\w+\s+tasks?",
                r"remove\s+the\s+\w+\s+tasks?",
            ],
            "update_task": [
                # Change/update patterns
                r"change\s+(?:the\s+)?tasks?\s+\d+\s+to",
                r"update\s+(?:the\s+)?tasks?\s+\d+\s+to",
                r"modify\s+(?:the\s+)?tasks?\s+\d+\s+to",
                r"edit\s+(?:the\s+)?tasks?\s+\d+\s+to",
                r"rename\s+(?:the\s+)?tasks?\s+\d+\s+to",
            ],
        }

    async def detect_intent(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Detect user intent from natural language message.

        Args:
            user_message: The user's message
            conversation_history: Optional conversation history for context

        Returns:
            Dict containing detected intent, confidence, and extracted parameters
        """
        try:
            # First try pattern matching for quick detection
            pattern_result = self._pattern_match_intent(user_message)

            if pattern_result["confidence"] > 0.7:
                # High confidence from pattern matching
                return pattern_result

            # Fall back to AI-based intent detection
            ai_result = await self._ai_detect_intent(user_message, conversation_history)

            return ai_result

        except Exception as e:
            return {
                "intent": "general_chat",
                "confidence": 0.0,
                "parameters": {},
                "error": str(e)
            }

    def _pattern_match_intent(self, user_message: str) -> Dict[str, Any]:
        """
        Use regex patterns to quickly match common intents.

        Args:
            user_message: The user's message

        Returns:
            Dict containing matched intent and confidence
        """
        message_lower = user_message.lower()

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    # Extract parameters based on intent
                    parameters = self._extract_parameters(intent, user_message)

                    return {
                        "intent": intent,
                        "confidence": 0.8,
                        "parameters": parameters,
                        "method": "pattern_match"
                    }

        return {
            "intent": "general_chat",
            "confidence": 0.3,
            "parameters": {},
            "method": "pattern_match"
        }

    def _extract_parameters(self, intent: str, message: str) -> Dict[str, Any]:
        """
        Extract parameters from message based on intent.

        Args:
            intent: The detected intent
            message: The user's message

        Returns:
            Dict containing extracted parameters
        """
        parameters = {}

        if intent == "add_task":
            # Extract task title and description
            # Look for patterns like "add task: title" or "remember to title"
            patterns = [
                r"(?:add|create|new)\s+(?:a\s+)?task[:\s]+(.+)",
                r"remember\s+to\s+(.+)",
                r"i\s+need\s+to\s+(.+)",
                r"todo:\s*(.+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    parameters["title"] = title
                    break

        elif intent == "complete_task":
            # Extract task ID or title
            # Look for patterns like "complete task #1" or "mark task 1 as done"
            id_match = re.search(r"(?:task\s+)?(?:#|id\s+)?(\d+)", message, re.IGNORECASE)
            if id_match:
                parameters["task_id"] = id_match.group(1)
            else:
                # Try to extract task title
                title_match = re.search(r"(?:complete|mark|finish)\s+(?:task\s+)?['\"]?(.+?)['\"]?\s+(?:as\s+)?(?:done|completed)", message, re.IGNORECASE)
                if title_match:
                    parameters["task_title"] = title_match.group(1).strip()

        elif intent == "delete_task":
            # Extract task ID or title
            id_match = re.search(r"(?:task\s+)?(?:#|id\s+)?(\d+)", message, re.IGNORECASE)
            if id_match:
                parameters["task_id"] = id_match.group(1)
            else:
                title_match = re.search(r"(?:delete|remove|cancel)\s+(?:task\s+)?['\"]?(.+?)['\"]?", message, re.IGNORECASE)
                if title_match:
                    parameters["task_title"] = title_match.group(1).strip()

        elif intent == "update_task":
            # Extract task ID and new values
            id_match = re.search(r"(?:task\s+)?(?:#|id\s+)?(\d+)", message, re.IGNORECASE)
            if id_match:
                parameters["task_id"] = id_match.group(1)

            # Try to extract new title
            title_match = re.search(r"(?:to|as)\s+['\"]?(.+?)['\"]?$", message, re.IGNORECASE)
            if title_match:
                parameters["title"] = title_match.group(1).strip()

        elif intent == "list_tasks":
            # Check for status filter
            if re.search(r"completed|done|finished", message, re.IGNORECASE):
                parameters["status"] = "completed"
            elif re.search(r"incomplete|pending|active|todo", message, re.IGNORECASE):
                parameters["status"] = "incomplete"
            else:
                parameters["status"] = "all"

        return parameters

    async def _ai_detect_intent(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Use AI (Gemini) to detect intent when pattern matching fails.

        Args:
            user_message: The user's message
            conversation_history: Optional conversation history for context

        Returns:
            Dict containing detected intent and parameters
        """
        prompt = f"""
You are an intent classifier for a todo management chatbot. Analyze the user's message and determine their intent.

Available intents:
- add_task: User wants to create a new task
- list_tasks: User wants to see their tasks
- complete_task: User wants to mark a task as done
- delete_task: User wants to remove a task
- update_task: User wants to modify a task
- general_chat: General conversation or unclear intent

User message: "{user_message}"

Respond with ONLY a JSON object in this exact format:
{{
  "intent": "intent_name",
  "confidence": 0.0-1.0,
  "parameters": {{}}
}}

For add_task, extract: {{"title": "task title", "description": "optional description"}}
For complete_task/delete_task/update_task, extract: {{"task_id": "id"}} or {{"task_title": "title"}}
For list_tasks, extract: {{"status": "all|completed|incomplete"}}
"""

        try:
            result = await self.gemini_service.detect_intent(prompt)

            # Try to parse JSON from response
            response_text = result.get("raw_response", "")

            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', response_text)
            if json_match:
                intent_data = json.loads(json_match.group(0))
                return {
                    "intent": intent_data.get("intent", "general_chat"),
                    "confidence": intent_data.get("confidence", 0.5),
                    "parameters": intent_data.get("parameters", {}),
                    "method": "ai_detection"
                }

            return {
                "intent": "general_chat",
                "confidence": 0.3,
                "parameters": {},
                "method": "ai_detection"
            }

        except Exception as e:
            return {
                "intent": "general_chat",
                "confidence": 0.0,
                "parameters": {},
                "error": str(e),
                "method": "ai_detection"
            }

    def map_intent_to_tool(self, intent: str) -> Optional[str]:
        """
        Map detected intent to MCP tool name.

        Args:
            intent: The detected intent

        Returns:
            MCP tool name or None if no mapping exists
        """
        intent_to_tool_map = {
            "add_task": "add_task",
            "list_tasks": "list_tasks",
            "complete_task": "complete_task",
            "delete_task": "delete_task",
            "update_task": "update_task",
        }

        return intent_to_tool_map.get(intent)

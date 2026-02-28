"""
Tool Execution Handler
Handles execution of MCP tools based on detected intent and parameters.
"""

from typing import Dict, Any, Optional
from src.mcp_server import MCPServer
from src.tools.task_tools import TaskTools
from src.services.intent_service import IntentService


class ToolExecutionHandler:
    """
    Handler for executing MCP tools based on user intent.
    Coordinates between intent detection and tool execution.
    """

    def __init__(self):
        """Initialize the tool execution handler."""
        self.mcp_server = MCPServer()
        self.task_tools = TaskTools()
        self.intent_service = IntentService()

    async def execute_from_message(
        self,
        user_id: str,
        user_message: str,
        conversation_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Execute appropriate tool based on user message.

        Args:
            user_id: The ID of the user
            user_message: The user's natural language message
            conversation_history: Optional conversation history for context

        Returns:
            Dict containing execution result and response
        """
        try:
            # Detect intent from message
            intent_result = await self.intent_service.detect_intent(
                user_message,
                conversation_history
            )

            intent = intent_result.get("intent")
            parameters = intent_result.get("parameters", {})
            confidence = intent_result.get("confidence", 0.0)

            # If general chat or low confidence, return conversational response
            if intent == "general_chat" or confidence < 0.5:
                return {
                    "success": True,
                    "intent": "general_chat",
                    "response": "I'm here to help you manage your tasks. You can ask me to add, list, complete, delete, or update tasks.",
                    "tool_executed": False
                }

            # Map intent to tool
            tool_name = self.intent_service.map_intent_to_tool(intent)

            if not tool_name:
                return {
                    "success": False,
                    "error": f"No tool mapping found for intent: {intent}",
                    "intent": intent,
                    "tool_executed": False
                }

            # Add user_id to parameters
            parameters["user_id"] = user_id

            # Execute the tool
            result = await self.execute_tool(tool_name, parameters)

            # Format response
            response = self._format_response(tool_name, result, parameters)

            return {
                "success": result.get("success", False),
                "intent": intent,
                "tool_name": tool_name,
                "tool_result": result,
                "response": response,
                "tool_executed": True,
                "confidence": confidence
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to execute tool: {str(e)}",
                "tool_executed": False
            }

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a specific MCP tool with given parameters.

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool

        Returns:
            Dict containing tool execution result
        """
        try:
            # Execute via MCP server
            result = await self.mcp_server.execute_tool(
                tool_name,
                parameters,
                self.task_tools
            )

            return result

        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }

    def _format_response(
        self,
        tool_name: str,
        result: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> str:
        """
        Format tool execution result into a natural language response.

        Args:
            tool_name: Name of the executed tool
            result: Tool execution result
            parameters: Parameters used for execution

        Returns:
            Natural language response string
        """
        if not result.get("success"):
            error = result.get("error", "Unknown error")
            return f"Sorry, I couldn't complete that action. Error: {error}"

        # Format response based on tool
        if tool_name == "add_task":
            task = result.get("result", {}).get("task", {})
            title = task.get("title", "the task")
            return f"✓ Added task: {title}"

        elif tool_name == "list_tasks":
            tasks = result.get("result", {}).get("tasks", [])
            count = len(tasks)

            if count == 0:
                status = parameters.get("status", "all")
                if status == "completed":
                    return "You have no completed tasks."
                elif status == "incomplete":
                    return "You have no incomplete tasks."
                else:
                    return "You have no tasks yet."

            # Format task list
            status = parameters.get("status", "all")
            response_lines = []

            if status == "all":
                response_lines.append(f"You have {count} task(s):")
            elif status == "completed":
                response_lines.append(f"You have {count} completed task(s):")
            else:
                response_lines.append(f"You have {count} incomplete task(s):")

            for i, task in enumerate(tasks, 1):
                title = task.get("title", "Untitled")
                completed = task.get("completed", False)
                status_icon = "✓" if completed else "○"
                response_lines.append(f"{i}. {status_icon} {title}")

            return "\n".join(response_lines)

        elif tool_name == "complete_task":
            task = result.get("result", {}).get("task", {})
            title = task.get("title", "the task")
            return f"✓ Completed task: {title}"

        elif tool_name == "delete_task":
            message = result.get("result", {}).get("message", "Task deleted")
            return f"✓ {message}"

        elif tool_name == "update_task":
            task = result.get("result", {}).get("task", {})
            title = task.get("title", "the task")
            return f"✓ Updated task: {title}"

        else:
            return "Action completed successfully."

    async def execute_tool_chain(
        self,
        user_id: str,
        tool_calls: list
    ) -> list:
        """
        Execute multiple tools in sequence.

        Args:
            user_id: The ID of the user
            tool_calls: List of tool call dicts with 'tool_name' and 'parameters'

        Returns:
            List of execution results
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("tool_name")
            parameters = tool_call.get("parameters", {})

            # Add user_id to parameters
            parameters["user_id"] = user_id

            # Execute tool
            result = await self.execute_tool(tool_name, parameters)
            results.append({
                "tool_name": tool_name,
                "result": result,
                "response": self._format_response(tool_name, result, parameters)
            })

        return results

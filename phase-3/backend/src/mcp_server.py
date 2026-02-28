"""
MCP Server for Todo Chatbot
Exposes task management tools via the Model Context Protocol.
"""

from typing import Any, Dict, List
import json

class MCPServer:
    """
    MCP Server that exposes task management tools.
    All tools are stateless and interact with the database for persistence.
    """

    def __init__(self):
        """Initialize the MCP server with available tools."""
        self.tools = {
            "add_task": {
                "name": "add_task",
                "description": "Add a new task for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional description of the task"
                        }
                    },
                    "required": ["user_id", "title"]
                }
            },
            "list_tasks": {
                "name": "list_tasks",
                "description": "List all tasks for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["all", "completed", "incomplete"],
                            "description": "Filter tasks by status"
                        }
                    },
                    "required": ["user_id"]
                }
            },
            "complete_task": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to complete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "delete_task": {
                "name": "delete_task",
                "description": "Delete a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "update_task": {
                "name": "update_task",
                "description": "Update a task's title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the task"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools.

        Returns:
            List of tool definitions
        """
        return list(self.tools.values())

    def get_tool(self, tool_name: str) -> Dict[str, Any]:
        """
        Get a specific tool definition.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool definition or None if not found
        """
        return self.tools.get(tool_name)

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        tool_handler: Any
    ) -> Dict[str, Any]:
        """
        Execute a tool with given parameters.

        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            tool_handler: Handler object with tool implementation methods

        Returns:
            Result of tool execution
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }

        try:
            # Validate parameters
            self._validate_parameters(tool_name, parameters)

            # Execute the tool via handler
            if hasattr(tool_handler, tool_name):
                method = getattr(tool_handler, tool_name)
                result = await method(**parameters)
                return {
                    "success": True,
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": f"Handler method '{tool_name}' not implemented"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _validate_parameters(self, tool_name: str, parameters: Dict[str, Any]) -> None:
        """
        Validate tool parameters against schema.

        Args:
            tool_name: Name of the tool
            parameters: Parameters to validate

        Raises:
            ValueError: If parameters are invalid
        """
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found")

        required = tool["parameters"].get("required", [])
        for param in required:
            if param not in parameters:
                raise ValueError(f"Missing required parameter: {param}")

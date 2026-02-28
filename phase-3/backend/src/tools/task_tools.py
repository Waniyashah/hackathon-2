"""
Task Tools for MCP Server
Implements stateless task management operations.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.models.task import Task
from src.db_context import get_db_session


class TaskTools:
    """
    Stateless task management tools for MCP server.
    All operations persist state through database interactions.
    """

    async def add_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a new task for a user.

        Args:
            user_id: The ID of the user
            title: The title of the task
            description: Optional description of the task

        Returns:
            Dict containing task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required and cannot be empty"
                }

            if not title or not title.strip():
                return {
                    "success": False,
                    "error": "title is required and cannot be empty"
                }

            async with get_db_session() as session:
                # Create new task
                new_task = Task(
                    user_id=user_id.strip(),
                    title=title.strip(),
                    description=description.strip() if description else None,
                    completed=False
                )

                session.add(new_task)
                await session.flush()
                await session.refresh(new_task)

                return {
                    "task_id": new_task.id,
                    "status": "created",
                    "title": new_task.title
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add task: {str(e)}"
            }

    async def list_tasks(
        self,
        user_id: str,
        status: str = "all"
    ) -> List[Dict[str, Any]]:
        """
        List all tasks for a user, optionally filtered by status.

        Args:
            user_id: The ID of the user
            status: Filter by status ('all', 'pending', 'completed')

        Returns:
            Array of task objects
        """
        try:
            # Validate inputs
            if not user_id or not user_id.strip():
                return []

            if status not in ["all", "pending", "completed"]:
                status = "all"

            async with get_db_session() as session:
                # Build query
                query = select(Task).where(Task.user_id == user_id.strip())

                if status == "completed":
                    query = query.where(Task.completed == True)
                elif status == "pending":
                    query = query.where(Task.completed == False)

                # Execute query
                result = await session.execute(query)
                tasks = result.scalars().all()

                # Format response
                task_list = [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed
                    }
                    for task in tasks
                ]

                return task_list

        except Exception as e:
            return []

    async def complete_task(
        self,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to complete

        Returns:
            Dict containing task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required"
                }

            # Convert task_id to int if it's a string
            if isinstance(task_id, str):
                try:
                    task_id = int(task_id)
                except ValueError:
                    return {
                        "success": False,
                        "error": "task_id must be a valid integer"
                    }

            async with get_db_session() as session:
                # Find the task
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id.strip()
                )
                result = await session.execute(query)
                task = result.scalar_one_or_none()

                if not task:
                    return {
                        "success": False,
                        "error": f"Task with id {task_id} not found"
                    }

                # Update task
                task.completed = True
                task.updated_at = datetime.utcnow()
                await session.flush()
                await session.refresh(task)

                return {
                    "task_id": task.id,
                    "status": "completed",
                    "title": task.title
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to complete task: {str(e)}"
            }

    async def delete_task(
        self,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to delete

        Returns:
            Dict containing task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required"
                }

            # Convert task_id to int if it's a string
            if isinstance(task_id, str):
                try:
                    task_id = int(task_id)
                except ValueError:
                    return {
                        "success": False,
                        "error": "task_id must be a valid integer"
                    }

            async with get_db_session() as session:
                # Find the task
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id.strip()
                )
                result = await session.execute(query)
                task = result.scalar_one_or_none()

                if not task:
                    return {
                        "success": False,
                        "error": f"Task with id {task_id} not found"
                    }

                task_title = task.title

                # Delete task
                await session.delete(task)

                return {
                    "task_id": task_id,
                    "status": "deleted",
                    "title": task_title
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete task: {str(e)}"
            }

    async def update_task(
        self,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a task's title or description.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            Dict containing task_id, status, and title
        """
        try:
            # Validate inputs
            if not user_id or not user_id.strip():
                return {
                    "success": False,
                    "error": "user_id is required"
                }

            if not title and description is None:
                return {
                    "success": False,
                    "error": "At least one of title or description must be provided"
                }

            # Convert task_id to int if it's a string
            if isinstance(task_id, str):
                try:
                    task_id = int(task_id)
                except ValueError:
                    return {
                        "success": False,
                        "error": "task_id must be a valid integer"
                    }

            async with get_db_session() as session:
                # Find the task
                query = select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id.strip()
                )
                result = await session.execute(query)
                task = result.scalar_one_or_none()

                if not task:
                    return {
                        "success": False,
                        "error": f"Task with id {task_id} not found"
                    }

                # Update task fields
                if title:
                    task.title = title.strip()
                if description is not None:
                    task.description = description.strip() if description else None

                task.updated_at = datetime.utcnow()
                await session.flush()
                await session.refresh(task)

                return {
                    "task_id": task.id,
                    "status": "updated",
                    "title": task.title
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update task: {str(e)}"
            }

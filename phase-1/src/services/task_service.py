"""
Task service layer for the Todo CLI application.
Handles all business logic for task management.
"""

from typing import Dict, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'models'))
from task import Task


class TaskService:
    """
    Service layer for managing tasks in memory with CRUD operations.
    """

    def __init__(self):
        """Initialize the task service with empty task storage."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task to the collection.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)

        Returns:
            ID of the newly created task

        Raises:
            ValueError: If title is empty
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip()
        )
        self.tasks[self.next_id] = task

        task_id = self.next_id
        self.next_id += 1

        return task_id

    def list_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection.

        Returns:
            List of all tasks ordered by ID
        """
        return sorted(self.tasks.values(), key=lambda x: x.id)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            True if update was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        # Update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Task title cannot be empty")
            task.title = title

        # Update description if provided
        if description is not None:
            task.description = description.strip()

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if deletion was successful, False if task not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            True if toggle was successful, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.completed = not task.completed
        return True

    def get_next_id(self) -> int:
        """
        Get the next available task ID without incrementing the counter.

        Returns:
            The next available ID
        """
        return self.next_id
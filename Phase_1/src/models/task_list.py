"""
TaskList Model

This module defines the TaskList data model for the todo application.
TaskList manages a collection of Task objects in memory.
"""

from typing import List, Optional
from .task import Task


class TaskList:
    """
    Collection of Task objects stored in memory.

    Attributes:
        tasks (dict): Dictionary mapping task IDs to Task objects
        _next_id (int): The next available ID for new tasks
    """

    def __init__(self):
        """Initialize an empty TaskList."""
        self.tasks = {}
        self._next_id = 1

    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task to the list.

        Args:
            title (str): Title of the task
            description (str, optional): Description of the task. Defaults to "".

        Returns:
            int: The ID of the newly created task
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        task_id = self._next_id
        self._next_id += 1

        task = Task(task_id, title, description, completed=False)
        self.tasks[task_id] = task

        return task_id

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task with the given ID, or None if not found
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if the task was updated, False if task was not found
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self.get_task(task_id)
        if task is None:
            return False

        task.update(title, description)
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the list.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if task was not found
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def list_tasks(self) -> List[Task]:
        """
        Get all tasks in the list.

        Returns:
            List[Task]: List of all tasks in the collection
        """
        return list(self.tasks.values())

    def toggle_task_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            bool: True if the task status was toggled, False if task was not found
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self.get_task(task_id)
        if task is None:
            return False

        task.toggle_completion()
        return True

    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID
        """
        return self._next_id
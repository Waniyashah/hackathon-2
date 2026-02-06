"""
Task Service

This module implements the business logic for task management operations.
It acts as an interface between the CLI layer and the data models.
"""

from typing import List, Dict, Optional
from models.task_list import TaskList
from models.task import Task


class TaskService:
    """
    Service layer for managing tasks.

    Handles all business logic related to task management operations.
    Provides a clean interface for CRUD operations on tasks.
    """

    def __init__(self):
        """Initialize the TaskService with an empty TaskList."""
        self.task_list = TaskList()

    def add_task(self, title: str, description: str = "") -> int:
        """
        Create a new task with the provided title and description.

        Args:
            title (str): Required string representing the task title
            description (str, optional): Optional string representing the task description (defaults to empty string)

        Returns:
            int: Integer representing the unique ID of the created task

        Post-condition: New task exists in the TaskList with completed=False
        """
        return self.task_list.add_task(title, description)

    def delete_task(self, task_id: int) -> bool:
        """
        Remove the task with the specified ID.

        Args:
            task_id (int): Integer representing the unique ID of the task to delete

        Returns:
            bool: Boolean indicating success (True) or failure (False) of the deletion

        Post-condition: Task no longer exists in the TaskList
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        return self.task_list.delete_task(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update the task with the specified ID.

        Args:
            task_id (int): Integer representing the unique ID of the task to update
            title (str, optional): Optional string for new title (if provided)
            description (str, optional): Optional string for new description (if provided)

        Returns:
            bool: Boolean indicating success (True) or failure (False) of the update

        Post-condition: Task in TaskList has updated properties
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        return self.task_list.update_task(task_id, title, description)

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of the task with the specified ID.

        Args:
            task_id (int): Integer representing the unique ID of the task to update

        Returns:
            bool: Boolean indicating success (True) or failure (False) of the toggle

        Post-condition: Task's completed property is inverted
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        return self.task_list.toggle_task_completion(task_id)

    def list_tasks(self) -> List[Dict]:
        """
        Return all tasks in the TaskList.

        Returns:
            List[Dict]: List of dictionaries containing all task properties

        Post-condition: No change to TaskList state
        """
        tasks = self.task_list.list_tasks()
        return [task.to_dict() for task in tasks]

    def get_task(self, task_id: int) -> Optional[Dict]:
        """
        Return the task with the specified ID.

        Args:
            task_id (int): Integer representing the unique ID of the task to retrieve

        Returns:
            Dict or None: Dictionary containing task properties or None if not found

        Post-condition: No change to TaskList state
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        task = self.task_list.get_task(task_id)
        if task:
            return task.to_dict()
        return None

    def get_next_task_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID
        """
        return self.task_list.get_next_id()
"""
Task Model

This module defines the Task data model for the todo application.
Each task has an ID, title, description, and completion status.
"""


class Task:
    """
    Represents a single todo item in the application.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Task title
        description (str): Optional task description
        completed (bool): Task completion status (default: False)
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title
            description (str, optional): Task description. Defaults to "".
            completed (bool, optional): Task completion status. Defaults to False.
        """
        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")
        if not isinstance(description, str):
            raise ValueError("Task description must be a string")
        if not isinstance(completed, bool):
            raise ValueError("Task completion status must be a boolean")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.completed = completed

    def __repr__(self):
        """Return string representation of the task."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.title}"

    def __eq__(self, other):
        """Compare tasks by ID."""
        if isinstance(other, Task):
            return self.id == other.id
        return False

    def to_dict(self):
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    def update(self, title=None, description=None):
        """
        Update task title and/or description.

        Args:
            title (str, optional): New title for the task
            description (str, optional): New description for the task
        """
        if title is not None:
            if not isinstance(title, str) or not title.strip():
                raise ValueError("Task title must be a non-empty string")
            self.title = title.strip()

        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Task description must be a string")
            self.description = description.strip()

    def toggle_completion(self):
        """Toggle the completion status of the task."""
        self.completed = not self.completed
"""
Task model for the Todo CLI application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo task.

    Attributes:
        id: Unique identifier for the task
        title: Task title (non-empty string)
        description: Task description (optional string)
        completed: Boolean indicating if task is completed
        created_at: Timestamp of when the task was created
    """
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        """Initialize the created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def __str__(self) -> str:
        """
        Return a string representation of the task for display purposes.

        Returns:
            Formatted string with task details
        """
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}: {self.title} - {self.description}"

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.

        Returns:
            Dictionary with task attributes
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Task instance from a dictionary.

        Args:
            data: Dictionary with task attributes

        Returns:
            Task instance
        """
        task = cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False)
        )
        if "created_at" in data:
            task.created_at = datetime.fromisoformat(data["created_at"])
        return task
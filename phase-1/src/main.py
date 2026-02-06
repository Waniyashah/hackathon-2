"""
Main entry point for the Todo CLI application.
This version avoids complex imports by implementing the core functionality directly.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import sys
import re


@dataclass
class Task:
    """
    Represents a single todo task.
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
        """
        status = "[x]" if self.completed else "[ ]"
        return f"{status} {self.id}: {self.title} - {self.description}"

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }


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
        """
        return sorted(self.tasks.values(), key=lambda x: x.id)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        """
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task's title and/or description.
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
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        task.completed = not task.completed
        return True


class CLIInterface:
    """
    Handles command-line interactions for the Todo application.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI interface with a task service.
        """
        self.task_service = task_service

    def display_menu(self):
        """Display available commands to the user."""
        print("\nAvailable commands:")
        print("  add <title> [description]    - Add a new task")
        print("  list                         - List all tasks")
        print("  update <id> <title> [desc]   - Update a task")
        print("  delete <id>                  - Delete a task")
        print("  complete <id>                - Mark task as complete")
        print("  incomplete <id>              - Mark task as incomplete")
        print("  help                         - Show this help message")
        print("  quit/exit                    - Exit the application")
        print()

    def display_tasks(self):
        """Display all tasks in a formatted table."""
        tasks = self.task_service.list_tasks()

        if not tasks:
            print("\nNo tasks found.")
            return

        # Print header
        print(f"\n{'ID':<4} {'Status':<8} {'Title':<20} {'Description':<30}")
        print("-" * 65)

        # Print each task
        for task in tasks:
            status = "[x]" if task.completed else "[ ]"
            title = task.title[:17] + "..." if len(task.title) > 20 else task.title
            description = task.description[:27] + "..." if len(task.description) > 30 else task.description
            print(f"{task.id:<4} {status:<8} {title:<20} {description:<30}")
        print()

    def parse_command(self, input_str: str) -> List[str]:
        """
        Parse command string handling quoted arguments.
        """
        # Regex to match quoted strings or individual words
        pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
        matches = re.findall(pattern, input_str.strip())

        # Extract the actual matched text from the three groups
        args = [match[0] or match[1] or match[2] for match in matches]
        return args

    def handle_command(self, command_input: str) -> bool:
        """
        Process a single command from the user.
        """
        args = self.parse_command(command_input)

        if not args:
            return True

        command = args[0].lower()

        try:
            if command == "add":
                self._handle_add(args)
            elif command == "list":
                self.display_tasks()
            elif command == "update":
                self._handle_update(args)
            elif command == "delete":
                self._handle_delete(args)
            elif command in ["complete", "incomplete"]:
                self._handle_toggle_completion(command, args)
            elif command == "help":
                self.display_menu()
            elif command in ["quit", "exit"]:
                print("Goodbye!")
                return False
            else:
                print(f"Unknown command '{command}'. Type 'help' for available commands.")
        except Exception as e:
            print(f"Error: {e}")

        return True

    def _handle_add(self, args: List[str]):
        """Handle the add command."""
        if len(args) < 2:
            print("Usage: add <title> [description]")
            return

        title = args[1]
        description = " ".join(args[2:]) if len(args) > 2 else ""

        task_id = self.task_service.add_task(title, description)
        print(f"Added task with ID: {task_id}")

    def _handle_update(self, args: List[str]):
        """Handle the update command."""
        if len(args) < 3:
            print("Usage: update <id> <title> [description]")
            return

        try:
            task_id = int(args[1])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        title = args[2]
        description = " ".join(args[3:]) if len(args) > 3 else ""

        success = self.task_service.update_task(task_id, title, description)
        if success:
            print(f"Updated task with ID: {task_id}")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _handle_delete(self, args: List[str]):
        """Handle the delete command."""
        if len(args) != 2:
            print("Usage: delete <id>")
            return

        try:
            task_id = int(args[1])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        success = self.task_service.delete_task(task_id)
        if success:
            print(f"Deleted task with ID: {task_id}")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _handle_toggle_completion(self, command: str, args: List[str]):
        """Handle the complete/incomplete commands."""
        if len(args) != 2:
            if command == "complete":
                print("Usage: complete <id]")
            else:
                print("Usage: incomplete <id>")
            return

        try:
            task_id = int(args[1])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        success = self.task_service.toggle_complete(task_id)
        if success:
            if command == "complete":
                print(f"Marked task {task_id} as complete")
            else:
                print(f"Marked task {task_id} as incomplete")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def run(self):
        """Run the main command loop."""
        print("Welcome to the Todo CLI Application!")
        print("Type 'help' for available commands.")

        while True:
            try:
                command = input("\n> ").strip()
                if not command:
                    continue

                if not self.handle_command(command):
                    break
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break


def main():
    """Main function to run the Todo CLI application."""
    # Create the task service and CLI interface
    task_service = TaskService()
    cli_interface = CLIInterface(task_service)

    # Run the application
    cli_interface.run()


if __name__ == "__main__":
    main()
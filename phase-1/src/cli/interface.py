"""
Command-line interface for the Todo CLI application.
"""

import sys
import os
from typing import List
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services'))
from task_service import TaskService


class CLIInterface:
    """
    Handles command-line interactions for the Todo application.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI interface with a task service.

        Args:
            task_service: Instance of TaskService to operate on
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

        Args:
            input_str: Raw input string from user

        Returns:
            List of parsed command and arguments
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

        Args:
            command_input: Command string from user input

        Returns:
            True to continue running, False to quit
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
                print("Usage: complete <id>")
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
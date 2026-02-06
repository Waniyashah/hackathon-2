"""
CLI Interface

This module implements the command-line interface for the todo application.
It handles user input, displays information, and coordinates with the service layer.
"""

from services.task_service import TaskService


class CLIInterface:
    """
    Command-line interface for the todo application.

    Handles all user interactions through the console, including:
    - Displaying menus
    - Processing user input
    - Formatting and displaying output
    - Error handling and validation
    """

    def __init__(self):
        """Initialize the CLI interface with a task service."""
        self.service = TaskService()

    def display_menu(self):
        """Display the main menu of available commands."""
        print("\n" + "="*40)
        print("TODO APPLICATION - MAIN MENU")
        print("="*40)
        print("1. Add Task")
        print("2. View Task List")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("-"*40)

    def get_valid_task_id(self, prompt: str) -> int:
        """
        Get a valid task ID from user input.

        Args:
            prompt (str): The prompt to display to the user

        Returns:
            int: The valid task ID entered by the user
        """
        while True:
            try:
                task_id_str = input(prompt).strip()
                if not task_id_str.isdigit():
                    print("Error: Task ID must be a number.")
                    continue
                task_id = int(task_id_str)
                if task_id <= 0:
                    print("Error: Task ID must be a positive number.")
                    continue
                return task_id
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None

    def get_user_choice(self):
        """Get the user's menu choice."""
        try:
            choice = input("Enter your choice (1-6): ").strip()
            return choice
        except EOFError:
            # Handle Ctrl+D or similar
            return "6"
        except KeyboardInterrupt:
            # Handle Ctrl+C
            return "6"

    def add_task_command(self):
        """Handle the add task command."""
        print("\n--- ADD TASK ---")
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.")
                return

            description = input("Enter task description (optional): ").strip()

            task_id = self.service.add_task(title, description)
            print(f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_tasks_command(self):
        """Handle the view tasks command."""
        print("\n--- VIEW TASKS ---")
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"Total tasks: {len(tasks)}")
        print("-" * 50)
        for task in tasks:
            status = "✓ COMPLETED" if task['completed'] else "○ PENDING"
            print(f"ID: {task['id']}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description'] or '[No description]'}")
            print(f"Status: {status}")
            print("-" * 30)

    def update_task_command(self):
        """Handle the update task command."""
        print("\n--- UPDATE TASK ---")

        task_id = self.get_valid_task_id("Enter task ID to update: ")
        if task_id is None:
            return

        try:
            # Check if task exists
            task = self.service.get_task(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Updating task: {task['title']}")

            # Get new values (empty string means don't change)
            new_title = input(f"Enter new title (leave blank to keep '{task['title']}'): ").strip()
            new_desc = input(f"Enter new description (leave blank to keep '{task['description']}'): ").strip()

            # Prepare update parameters
            update_params = {}
            if new_title:
                update_params['title'] = new_title
            if new_desc:
                update_params['description'] = new_desc

            # Perform update
            if update_params:
                success = self.service.update_task(task_id, **update_params)
                if success:
                    print("Task updated successfully.")
                else:
                    print("Failed to update task.")
            else:
                print("No changes made.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_task_command(self):
        """Handle the delete task command."""
        print("\n--- DELETE TASK ---")

        task_id = self.get_valid_task_id("Enter task ID to delete: ")
        if task_id is None:
            return

        try:
            # Confirm deletion
            task = self.service.get_task(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"You are about to delete: {task['title']}")
            confirm = input("Are you sure? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                success = self.service.delete_task(task_id)
                if success:
                    print("Task deleted successfully.")
                else:
                    print("Failed to delete task.")
            else:
                print("Deletion cancelled.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def toggle_task_command(self):
        """Handle the toggle task completion command."""
        print("\n--- MARK TASK COMPLETE/INCOMPLETE ---")

        task_id = self.get_valid_task_id("Enter task ID to toggle: ")
        if task_id is None:
            return

        try:
            # Check if task exists
            task = self.service.get_task(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            success = self.service.toggle_complete(task_id)
            if success:
                new_status = "completed" if task['completed'] else "incomplete"
                print(f"Task marked as {new_status}.")
            else:
                print("Failed to update task status.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Application!")

        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task_command()
            elif choice == "2":
                self.view_tasks_command()
            elif choice == "3":
                self.update_task_command()
            elif choice == "4":
                self.delete_task_command()
            elif choice == "5":
                self.toggle_task_command()
            elif choice == "6":
                print("\nThank you for using the Todo Application!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")

            # Pause to let user see results before showing menu again
            input("\nPress Enter to continue...")
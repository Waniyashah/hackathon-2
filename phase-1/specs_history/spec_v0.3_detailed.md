# Todo Application Specification v0.3 (Detailed Implementation)

## Project Overview
A command-line todo application that stores tasks in memory using Python 3.13+. The application follows spec-driven development principles with no manual coding allowed. Implementation will be generated via Claude Code using Spec-Kit Plus.

## Architecture
- Language: Python 3.13+
- Environment: UV
- Application Type: Console/CLI
- Data Storage: In-memory only (no persistent storage)
- Project Structure:
  - `/src/todo_app/` → Python source code
    - `models.py` - Task data model
    - `manager.py` - Task management logic
    - `cli.py` - Command-line interface
    - `main.py` - Application entry point
  - `/specs_history/` → All specification versions
  - `README.md` → Setup and usage instructions
  - `CLAUDE.md` → Claude Code usage instructions

## Class Design

### Task Class (in models.py)
```python
class Task:
    def __init__(self, task_id: int, title: str, description: str = ""):
        # Initialize task properties

    def __str__(self) -> str:
        # Return string representation for display

    def to_dict(self) -> dict:
        # Return dictionary representation
```

Properties:
- `id`: Integer, unique identifier
- `title`: String, non-empty task title
- `description`: String, optional task description
- `completed`: Boolean, completion status (default: False)
- `created_at`: datetime, timestamp of creation

### TaskManager Class (in manager.py)
```python
class TaskManager:
    def __init__(self):
        # Initialize in-memory storage

    def add_task(self, title: str, description: str = "") -> int:
        # Add a new task and return its ID

    def get_all_tasks(self) -> list:
        # Return all tasks

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        # Update task details and return success status

    def delete_task(self, task_id: int) -> bool:
        # Delete task by ID and return success status

    def toggle_completion(self, task_id: int) -> bool:
        # Toggle task completion status and return success status

    def get_task_by_id(self, task_id: int) -> Task or None:
        # Retrieve task by ID
```

### CLIHandler Class (in cli.py)
```python
class CLIHandler:
    def __init__(self, task_manager: TaskManager):
        # Initialize with task manager

    def display_menu(self):
        # Show available commands

    def handle_command(self, command: str) -> bool:
        # Process user command, return False to quit

    def run(self):
        # Main command loop
```

## Functional Requirements Implementation Details

### 1. Add Task
- Method: `TaskManager.add_task(title: str, description: str = "") -> int`
- Implementation:
  - Validates that title is not empty/None
  - Generates next available ID based on current highest ID
  - Creates new Task instance with completed=False
  - Stores task in internal collection (dictionary with ID as key)
  - Returns the new task's ID
- Error handling: Raises ValueError if title is empty

### 2. View Task List
- Method: `CLIHandler.display_tasks() -> None`
- Implementation:
  - Gets all tasks from TaskManager
  - Formats output in aligned columns
  - Uses clear visual indicators ([ ] for incomplete, [x] for complete)
  - Shows appropriate message if no tasks exist
  - Aligns columns properly with headers

### 3. Update Task
- Method: `TaskManager.update_task(task_id: int, title: str = None, description: str = None) -> bool`
- Implementation:
  - Verifies task with given ID exists
  - Updates provided fields, leaves others unchanged
  - Returns True on success, False if task not found
  - Validates that title is not set to empty string

### 4. Delete Task
- Method: `TaskManager.delete_task(task_id: int) -> bool`
- Implementation:
  - Checks if task with ID exists
  - Removes task from storage if found
  - Returns True on success, False if task not found
  - Handles case where task doesn't exist gracefully

### 5. Mark as Complete/Incomplete
- Method: `TaskManager.toggle_completion(task_id: int) -> bool`
- Implementation:
  - Verifies task with given ID exists
  - Toggles the completed property from True to False or vice versa
  - Returns True on success, False if task not found

## CLI Command Processing
- Command format: `<command> <arg1> <arg2> ...`
- Supported commands:
  - `add "Buy groceries" "Milk, eggs, bread"` - Add with quoted multi-word strings
  - `add "Buy groceries"` - Add with single word title
  - `list` - Show all tasks
  - `update 1 "Updated title" "Updated description"` - Update specific task
  - `update 1 "Updated title"` - Update only title
  - `delete 1` - Delete task with ID 1
  - `complete 1` - Mark task 1 as complete
  - `incomplete 1` - Mark task 1 as incomplete
  - `help` - Show command reference
  - `quit` or `exit` - Close application

## Input Parsing
- Parse command and arguments using split()
- Handle quoted strings as single arguments
- Validate number of arguments for each command
- Show appropriate error messages for malformed commands

## Error Messages
- "Error: Task title cannot be empty." - When trying to create task with empty title
- "Error: Task with ID {id} not found." - When operating on non-existent task
- "Error: Invalid command format." - When command arguments don't match expectations
- "Unknown command '{command}'. Type 'help' for available commands." - For unknown commands

## Display Formatting
- Table-style output for task list with aligned columns
- Header row with column names
- Consistent spacing and alignment
- Status indicators using brackets [ ] and [x]

## Dependencies
- Only standard Python library modules (no external dependencies)
- Use datetime module for timestamps
- Use json module only if needed for debugging (not for persistence)

## Testing Considerations
- Functions should be unit-testable
- Separate business logic from UI concerns
- Clear return values for success/failure indication
- Predictable behavior for all operations

## Performance Considerations
- Efficient data structures for task storage
- Reasonable performance with up to 1000 tasks
- Memory usage proportional to number of tasks only
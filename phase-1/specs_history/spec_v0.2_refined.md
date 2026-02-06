# Todo Application Specification v0.2 (Refined)

## Project Overview
A command-line todo application that stores tasks in memory using Python 3.13+. The application follows spec-driven development principles with no manual coding allowed. Implementation will be generated via Claude Code using Spec-Kit Plus.

## Architecture
- Language: Python 3.13+
- Environment: UV
- Application Type: Console/CLI
- Data Storage: In-memory only (no persistent storage)
- Project Structure:
  - `/src` → Python source code
  - `/specs_history` → All specification versions
  - `README.md` → Setup and usage instructions
  - `CLAUDE.md` → Claude Code usage instructions

## Core Components
1. **Task Model**: Represents individual todo items
2. **Task Manager**: Handles CRUD operations for tasks
3. **CLI Interface**: Command-line user interaction
4. **Main Application**: Orchestrates the components

## Functional Requirements

### 1. Add Task
- Function: `add_task(title: str, description: str = "") -> int`
- Parameters:
  - `title` (required): Task title (string)
  - `description` (optional): Task description (string)
- Behavior:
  - Creates new task with auto-generated unique ID
  - Sets completion status to False (incomplete) by default
  - Stores task in memory
  - Returns the ID of the created task
- Validation:
  - Title must not be empty or None
  - Empty titles should trigger error message

### 2. View Task List
- Function: `view_tasks() -> None`
- Behavior:
  - Displays all tasks in console with clear formatting
  - Shows unique ID, title, description, and completion status
  - Uses visual indicators for completion status (e.g., [ ] for incomplete, [x] for complete)
  - If no tasks exist, displays "No tasks found" message
  - Lists tasks in order of creation

### 3. Update Task
- Function: `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- Parameters:
  - `task_id` (required): Unique identifier of the task to update
  - `title` (optional): New title for the task
  - `description` (optional): New description for the task
- Behavior:
  - Updates specified task with new values if provided
  - Preserves original values if None passed for specific field
  - Returns True if update successful, False if task not found
  - Validates task ID exists before attempting update

### 4. Delete Task
- Function: `delete_task(task_id: int) -> bool`
- Parameters:
  - `task_id` (required): Unique identifier of the task to delete
- Behavior:
  - Removes task from memory storage
  - Returns True if deletion successful, False if task not found
  - Validates task ID exists before attempting deletion

### 5. Mark as Complete/Incomplete
- Function: `toggle_completion(task_id: int) -> bool`
- Parameters:
  - `task_id` (required): Unique identifier of the task to toggle
- Behavior:
  - Toggles completion status of the specified task
  - If task is incomplete, marks it as complete
  - If task is complete, marks it as incomplete
  - Returns True if toggle successful, False if task not found
  - Validates task ID exists before attempting toggle

## Task Model Properties
- `id`: Integer, unique identifier (auto-generated, sequential)
- `title`: String, task title (required, non-empty)
- `description`: String, task description (optional, may be empty)
- `completed`: Boolean, completion status (default: False)
- `created_at`: String/Timestamp, timestamp of creation (auto-generated)

## Task Manager Responsibilities
- Maintain in-memory collection of tasks (using a dictionary or list)
- Generate unique sequential IDs for new tasks
- Validate task IDs exist before operations
- Implement all five core functions
- Return appropriate success/failure indicators
- Handle operations safely without crashing

## CLI Commands Interface
- `add <title> [description]` - Add a new task with title and optional description
- `list` - Show all tasks with status indicators
- `update <id> <title> [description]` - Update task with new title/description
- `delete <id>` - Remove task by ID
- `complete <id>` - Toggle task completion status
- `help` - Show available commands and usage examples
- `quit` or `exit` - Exit the application
- Input parsing should handle missing parameters gracefully

## Error Handling Requirements
- Invalid commands should show "Unknown command. Type 'help' for available commands."
- Invalid task IDs should show "Task with ID <id> not found."
- Missing required parameters should show usage instructions for the command
- Empty titles should show "Error: Task title cannot be empty."
- Unhandled exceptions should be caught and show user-friendly error messages

## Display Formatting Requirements
- Task list should show ID, status indicator, title, and description in a readable format
- Example format:
```
ID  Status  Title                Description
1   [ ]     Buy groceries        Milk, eggs, bread
2   [x]     Finish report        Complete quarterly analysis
3   [ ]     Call client          Schedule meeting for next week
```
- Status indicators: `[ ]` for incomplete, `[x]` for complete
- Help command should show command syntax and brief explanation

## System Behavior Requirements
- Tasks exist only in memory during runtime
- When application closes, tasks are lost (no persistence)
- Console interaction should be responsive and intuitive
- Clear separation between input processing and business logic
- Minimal dependencies, focused on core functionality

## Success Criteria
- Application runs in console without crashing
- All five functional requirements work correctly
- Clear, readable console output
- Proper error handling for edge cases
- Code follows modular design principles
- Implementation traceable to specification

## Technology Stack
- Python 3.13+
- Standard library only (no external dependencies)
- Console input/output for user interaction
- In-memory data structures (lists, dictionaries)

## Out of Scope
- Database connectivity
- File persistence
- Web interface
- Graphical user interface
- Network functionality
- Advanced task features (due dates, priorities, tags)
- Multi-user functionality
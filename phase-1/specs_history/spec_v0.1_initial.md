# Todo Application Specification v0.1 (Initial)

## Project Overview
A command-line todo application that stores tasks in memory using Python 3.13+. The application follows spec-driven development principles with no manual coding allowed.

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
1. **Add Task**: Create new todo items with title and description
2. **View Tasks**: Display all tasks with status indicators
3. **Update Task**: Modify existing task information
4. **Delete Task**: Remove tasks using unique task ID
5. **Mark Complete**: Toggle task completion status

## Task Model Properties
- `id`: Unique identifier (auto-generated)
- `title`: Task title (required string)
- `description`: Task description (optional string)
- `completed`: Boolean status (default: False)
- `created_at`: Timestamp of creation (auto-generated)

## Task Manager Responsibilities
- Store tasks in memory
- Generate unique IDs
- Provide CRUD operations
- Handle task completion toggling

## CLI Commands
- `add <title> [description]` - Add a new task
- `list` - Show all tasks
- `update <id> <title> [description]` - Update a task
- `delete <id>` - Remove a task
- `complete <id>` - Mark task as complete
- `incomplete <id>` - Mark task as incomplete
- `help` - Show available commands
- `quit` - Exit the application

## Error Handling
- Invalid commands should show helpful error messages
- Invalid task IDs should be handled gracefully
- Missing required parameters should show usage instructions

## Success Criteria
- Application runs in console
- All functional requirements work correctly
- Clean, readable output
- Proper error handling
# Todo Application - Phase I

This is a command-line todo application that runs entirely in memory and demonstrates core task management functionality. The application was developed following a spec-driven, agentic development workflow using Claude Code and Spec-Kit Plus.

## Features

- Add tasks with title and description
- View all tasks with clear status indicators
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- In-memory storage (no persistent storage)
- Clean console-based interface

## Requirements

- Python 3.13+

## Setup

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies (if any) - this project uses only standard Python library

## Usage

Run the application with:
```bash
python src/main.py
```

The application will present a menu-driven interface:
1. Add Task - Create a new todo item with title and description
2. View Task List - Display all tasks with status indicators
3. Update Task - Modify existing task title or description
4. Delete Task - Remove a task by ID
5. Mark Task Complete/Incomplete - Toggle task completion status
6. Exit - Quit the application

## Project Structure

```
src/
├── main.py                 # Application entry point
├── models/
│   ├── task.py            # Task data model
│   └── task_list.py       # Task collection model
├── services/
│   └── task_service.py    # Business logic layer
└── cli/
    └── cli_interface.py   # Command-line interface
```

## Development

This application was developed following the agentic development workflow:
1. Specification → Plan → Tasks → Implementation
2. No manual coding was performed - all code generated via Claude Code
3. Clean, modular architecture with separation of concerns
4. Proper error handling and input validation
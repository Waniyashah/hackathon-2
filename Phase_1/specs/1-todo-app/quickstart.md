# Todo App Quickstart Guide

## Overview
This guide provides quick instructions for setting up and running the Todo CLI application.

## Prerequisites
- Python 3.13+ installed
- UV package manager (if using UV environment)

## Setup
1. Clone or create the project structure:
```
src/
├── main.py
├── models/
│   └── task.py
├── services/
│   └── task_service.py
└── cli/
    └── cli_interface.py
```

2. Ensure Python 3.13+ is available in your environment

## Running the Application
1. Navigate to the project root
2. Execute: `python src/main.py`
3. The application will start and present a menu of available commands

## Basic Usage
Once the application is running:
1. Use numbered menu options to select operations
2. Follow the prompts to provide required information
3. View results or error messages displayed in the console

## Available Commands
- Add Task: Create a new todo item
- View Tasks: Display all tasks with status
- Update Task: Modify an existing task
- Delete Task: Remove a task by ID
- Mark Complete: Toggle task completion status

## Development
To run tests (when implemented):
`pytest tests/`

To run the application in development mode:
`python src/main.py`
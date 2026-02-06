# Todo Application

A command-line todo application that stores tasks in memory using Python 3.13+.

## Setup

1. Ensure you have Python 3.13+ installed
2. Install UV package manager
3. Clone this repository
4. Navigate to the project directory
5. Install dependencies using UV

## Installation

```bash
# Install UV if you don't have it
pip install uv

# Install project dependencies
uv pip install -r requirements.txt
```

## Usage

Run the application using:

```bash
python src/main.py
```

## Available Commands

- `add <title> [description]` - Add a new task
- `list` - Show all tasks with status
- `update <id> <title> [description]` - Update a task
- `delete <id>` - Remove a task
- `complete <id>` - Mark task as complete
- `incomplete <id>` - Mark task as incomplete
- `help` - Show available commands
- `quit` - Exit the application

## Features

- Add, update, delete, and view todo tasks
- Mark tasks as complete/incomplete
- In-memory storage (no persistence)
- Clean console interface
- Error handling for invalid inputs

## Project Structure

- `/src` - Python source code
- `/specs_history` - Specification documents
- `README.md` - This file
- `CLAUDE.md` - Claude Code usage instructions
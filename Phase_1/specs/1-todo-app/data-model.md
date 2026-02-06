# Data Model: Todo App

## Overview
This document describes the data model for the Todo CLI application based on the feature specification.

## Entity: Task
Represents a single todo item in the application

### Attributes
- **id**: integer (unique identifier, auto-generated)
- **title**: string (required, task title)
- **description**: string (optional, task description)
- **completed**: boolean (task completion status, default: False)

### Relationships
- Part of a single TaskList collection

### State Transitions
- Initial state: completed = False
- Transition: completed → !completed (via toggle_complete operation)

### Validation Rules
- title: Required, non-empty string
- id: Unique within the TaskList, auto-incrementing integer
- completed: Boolean value only (True/False)

## Entity: TaskList
Collection of Task entities stored in memory

### Attributes
- **tasks**: List/Dictionary of Task objects indexed by ID

### Operations Supported
- Add new Task
- Retrieve Task by ID
- Update Task by ID
- Delete Task by ID
- List all Tasks
- Toggle Task completion status by ID

### Constraints
- All Task IDs must be unique within the collection
- No persistent storage - exists only in memory during runtime
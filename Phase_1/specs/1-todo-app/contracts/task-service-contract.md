# Task Service API Contract

## Overview
This contract defines the interface for the Task Service layer in the Todo CLI application.

## Service Interface: TaskService

### Methods

#### `add_task(title: str, description: str = "") -> int`
**Description**: Creates a new task with the provided title and description
**Parameters**:
- title: Required string representing the task title
- description: Optional string representing the task description (defaults to empty string)
**Returns**: Integer representing the unique ID of the created task
**Post-condition**: New task exists in the TaskList with completed=False

#### `delete_task(task_id: int) -> bool`
**Description**: Removes the task with the specified ID
**Parameters**:
- task_id: Integer representing the unique ID of the task to delete
**Returns**: Boolean indicating success (True) or failure (False) of the deletion
**Post-condition**: Task no longer exists in the TaskList

#### `update_task(task_id: int, title: str = None, description: str = None) -> bool`
**Description**: Updates the task with the specified ID
**Parameters**:
- task_id: Integer representing the unique ID of the task to update
- title: Optional string for new title (if provided)
- description: Optional string for new description (if provided)
**Returns**: Boolean indicating success (True) or failure (False) of the update
**Post-condition**: Task in TaskList has updated properties

#### `toggle_complete(task_id: int) -> bool`
**Description**: Toggles the completion status of the task with the specified ID
**Parameters**:
- task_id: Integer representing the unique ID of the task to update
**Returns**: Boolean indicating success (True) or failure (False) of the toggle
**Post-condition**: Task's completed property is inverted

#### `list_tasks() -> List[dict]`
**Description**: Returns all tasks in the TaskList
**Returns**: List of dictionaries containing all task properties
**Post-condition**: No change to TaskList state

#### `get_task(task_id: int) -> dict`
**Description**: Returns the task with the specified ID
**Parameters**:
- task_id: Integer representing the unique ID of the task to retrieve
**Returns**: Dictionary containing task properties or None if not found
**Post-condition**: No change to TaskList state
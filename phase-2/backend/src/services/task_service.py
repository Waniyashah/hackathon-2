from sqlmodel import Session, select
from typing import List
import uuid
from datetime import datetime

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


async def create_task(session: Session, user_id: str, task_data: TaskCreate) -> Task:
    """
    Create a new task for the specified user
    """
    # Validate that user_id is a valid UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Create the task object
    db_task = Task(
        id=uuid.uuid4(),
        user_id=user_uuid,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed or False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add to session and commit
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


async def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    """
    Get all tasks for the specified user
    """
    # Validate that user_id is a valid UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise ValueError("Invalid user ID format")

    # Query tasks for the specified user
    statement = select(Task).where(Task.user_id == user_uuid)
    results = session.exec(statement)
    tasks = results.all()

    return tasks


async def get_task_by_id(session: Session, task_id: str) -> Task:
    """
    Get a task by its ID
    """
    # Validate that task_id is a valid UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise ValueError("Invalid task ID format")

    # Query task by ID
    db_task = session.get(Task, task_uuid)

    if not db_task:
        raise ValueError("Task not found")

    return db_task


async def update_task(session: Session, task_id: str, task_data: TaskUpdate) -> Task:
    """
    Update a task with the provided data
    """
    # Validate that task_id is a valid UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise ValueError("Invalid task ID format")

    # Get the existing task
    db_task = await get_task_by_id(session, task_id)

    # Update the task with provided data
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update timestamp
    db_task.updated_at = datetime.utcnow()

    # Commit changes
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


async def delete_task(session: Session, task_id: str) -> bool:
    """
    Delete a task by its ID
    """
    # Validate that task_id is a valid UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise ValueError("Invalid task ID format")

    # Get the existing task
    db_task = await get_task_by_id(session, task_id)

    # Delete the task
    session.delete(db_task)
    session.commit()

    return True


async def toggle_task_completion(session: Session, task_id: str, completed: bool) -> Task:
    """
    Toggle the completion status of a task
    """
    # Validate that task_id is a valid UUID
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise ValueError("Invalid task ID format")

    # Get the existing task
    db_task = await get_task_by_id(session, task_id)

    # Update the completion status
    db_task.completed = completed
    db_task.updated_at = datetime.utcnow()

    # Commit changes
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task
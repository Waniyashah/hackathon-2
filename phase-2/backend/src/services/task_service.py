from sqlmodel import Session, select
from typing import List, Optional
import uuid
from datetime import datetime

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


async def create_task(task_data: TaskCreate, user_id: uuid.UUID, session: Session) -> Task:
    """
    Create a new task for the specified user
    """
    # Create the task object
    db_task = Task(
        id=uuid.uuid4(),
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add to session and commit
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


async def get_user_tasks(user_id: uuid.UUID, session: Session) -> List[Task]:
    """
    Get all tasks for the specified user
    """
    # Query tasks for the specified user
    statement = select(Task).where(Task.user_id == user_id)
    results = session.exec(statement)
    tasks = results.all()

    return tasks


async def get_task_by_id(task_id: uuid.UUID, user_id: uuid.UUID, session: Session) -> Optional[Task]:
    """
    Get a task by its ID, ensuring it belongs to the specified user
    """
    # Query task by ID and user_id
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = session.exec(statement)
    db_task = result.first()

    return db_task


async def update_task(task_id: uuid.UUID, task_data: TaskUpdate, user_id: uuid.UUID, session: Session) -> Optional[Task]:
    """
    Update a task with the provided data
    """
    # Get the existing task
    db_task = await get_task_by_id(task_id, user_id, session)

    if not db_task:
        return None

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


async def delete_task(task_id: uuid.UUID, user_id: uuid.UUID, session: Session) -> bool:
    """
    Delete a task by its ID
    """
    # Get the existing task
    db_task = await get_task_by_id(task_id, user_id, session)

    if not db_task:
        return False

    # Delete the task
    session.delete(db_task)
    session.commit()

    return True


async def toggle_task_completion(task_id: uuid.UUID, user_id: uuid.UUID, session: Session) -> Optional[Task]:
    """
    Toggle the completion status of a task
    """
    # Get the existing task
    db_task = await get_task_by_id(task_id, user_id, session)

    if not db_task:
        return None

    # Toggle the completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()

    # Commit changes
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

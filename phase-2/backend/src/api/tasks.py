from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import uuid

from ..models.user import User
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..database.session import get_session
from ..middleware.auth import get_current_user
from ..api.utils import handle_error
from ..services.task_service import create_task, get_user_tasks, get_task_by_id, update_task, delete_task, toggle_task_completion

router = APIRouter(prefix="/users/{user_id}", tags=["Tasks"])


@router.get("/tasks", response_model=List[TaskResponse])
async def list_user_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to view tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        user_uuid = uuid.UUID(user_id)
        tasks = await get_user_tasks(user_uuid, session)
        return [TaskResponse.model_validate(task) for task in tasks]
    except HTTPException:
        raise
    except Exception as e:
        handle_error(f"Failed to retrieve tasks: {str(e)}")


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to create tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        user_uuid = uuid.UUID(user_id)
        db_task = await create_task(task_data, user_uuid, session)
        return TaskResponse.model_validate(db_task)
    except HTTPException:
        raise
    except Exception as e:
        handle_error(f"Failed to create task: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_single_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to access tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
        db_task = await get_task_by_id(task_uuid, user_uuid, session)

        if not db_task:
            handle_error("Task not found", status.HTTP_404_NOT_FOUND)

        return TaskResponse.model_validate(db_task)
    except HTTPException:
        raise
    except Exception as e:
        handle_error(f"Failed to retrieve task: {str(e)}")


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to update tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
        updated_task = await update_task(task_uuid, task_data, user_uuid, session)

        if not updated_task:
            handle_error("Task not found", status.HTTP_404_NOT_FOUND)

        return TaskResponse.model_validate(updated_task)
    except HTTPException:
        raise
    except Exception as e:
        handle_error(f"Failed to update task: {str(e)}")


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to delete tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
        result = await delete_task(task_uuid, user_uuid, session)

        if not result:
            handle_error("Task not found", status.HTTP_404_NOT_FOUND)

        return
    except HTTPException:
        raise
    except Exception as e:
        handle_error(f"Failed to delete task: {str(e)}")


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete_status(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to update tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
        updated_task = await toggle_task_completion(task_uuid, user_uuid, session)

        if not updated_task:
            handle_error("Task not found", status.HTTP_404_NOT_FOUND)

        return TaskResponse.model_validate(updated_task)
    except HTTPException:
        raise
    except Exception as e:
        handle_error(f"Failed to update task completion status: {str(e)}")

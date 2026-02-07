from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import uuid
from pydantic import UUID4

from ..models.user import User
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskToggle
from ..database.session import get_session
from ..middleware.auth import get_current_user
from ..api.utils import handle_error, check_user_owns_resource, validate_task_exists
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
        tasks = await get_user_tasks(session, user_id)
        return [TaskResponse.model_validate(task) for task in tasks]
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
        db_task = await create_task(session, user_id, task_data)
        return TaskResponse.model_validate(db_task)
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
        db_task = await get_task_by_id(session, task_id)

        # Verify the task belongs to the specified user
        if str(db_task.user_id) != user_id:
            handle_error("Task does not belong to the specified user", status.HTTP_403_FORBIDDEN)

        return TaskResponse.model_validate(db_task)
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
        # Verify the task exists and belongs to the user
        db_task = await get_task_by_id(session, task_id)
        if str(db_task.user_id) != user_id:
            handle_error("Task does not belong to the specified user", status.HTTP_403_FORBIDDEN)

        updated_task = await update_task(session, task_id, task_data)
        return TaskResponse.model_validate(updated_task)
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
        # Verify the task exists and belongs to the user
        db_task = await get_task_by_id(session, task_id)
        if str(db_task.user_id) != user_id:
            handle_error("Task does not belong to the specified user", status.HTTP_403_FORBIDDEN)

        await delete_task(session, task_id)
        return
    except Exception as e:
        handle_error(f"Failed to delete task: {str(e)}")


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_complete_status(
    user_id: str,
    task_id: str,
    toggle_data: TaskToggle,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task
    """
    if str(current_user.id) != user_id:
        handle_error("Not authorized to update tasks for this user", status.HTTP_403_FORBIDDEN)

    try:
        # Verify the task exists and belongs to the user
        db_task = await get_task_by_id(session, task_id)
        if str(db_task.user_id) != user_id:
            handle_error("Task does not belong to the specified user", status.HTTP_403_FORBIDDEN)

        updated_task = await toggle_task_completion(session, task_id, toggle_data.completed)
        return TaskResponse.model_validate(updated_task)
    except Exception as e:
        handle_error(f"Failed to update task completion status: {str(e)}")
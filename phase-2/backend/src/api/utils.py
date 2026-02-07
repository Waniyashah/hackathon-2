from fastapi import HTTPException, status
from typing import Any, Dict, Optional
from sqlmodel import Session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ServiceException(Exception):
    """Base exception for service errors"""
    pass


def handle_error(detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """
    Helper function to handle and log errors consistently
    """
    logger.error(detail)
    raise HTTPException(status_code=status_code, detail=detail)


def create_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict:
    """
    Helper function to create consistent response format
    """
    response = {
        "success": status_code < 400,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def check_user_owns_resource(user_id: str, resource_user_id: str):
    """
    Helper function to check if a user owns a specific resource
    """
    if user_id != resource_user_id:
        handle_error("User does not have permission to access this resource", status.HTTP_403_FORBIDDEN)


def validate_user_exists(session: Session, user_id: str):
    """
    Helper function to validate that a user exists
    """
    from ..models.user import User
    user = session.get(User, user_id)
    if not user:
        handle_error("User not found", status.HTTP_404_NOT_FOUND)
    return user


def validate_task_exists(session: Session, task_id: str):
    """
    Helper function to validate that a task exists
    """
    from ..models.task import Task
    task = session.get(Task, task_id)
    if not task:
        handle_error("Task not found", status.HTTP_404_NOT_FOUND)
    return task
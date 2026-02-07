from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime


# Base schema for task data
class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = False


# Schema for creating a new task
class TaskCreate(TaskBase):
    title: str = Field(min_length=1, max_length=255)


# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


# Schema for task response
class TaskResponse(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for toggling task completion
class TaskToggle(BaseModel):
    completed: bool
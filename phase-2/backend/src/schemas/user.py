from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid
from datetime import datetime


# Base schema for user data
class UserBase(BaseModel):
    email: EmailStr


# Schema for creating a new user
class UserCreate(UserBase):
    password: str = Field(min_length=6)


# Schema for user registration
class UserRegister(UserCreate):
    confirmPassword: str


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


# Schema for user response (without password)
class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Schema for updating user
class UserUpdate(BaseModel):
    email: Optional[str] = None
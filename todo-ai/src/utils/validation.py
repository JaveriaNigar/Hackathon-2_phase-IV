"""Validation utilities for the Todo AI Chatbot API"""

import re
from typing import Optional
from pydantic import BaseModel, validator, Field
from sqlmodel import Session, select
from ..models.user import User
from ..models.task import Task
from ..models.conversation import Conversation


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


def validate_task_title(title: str) -> tuple[bool, str]:
    """
    Validate task title
    Returns (is_valid, message)
    """
    if not title or not title.strip():
        return False, "Task title cannot be empty"
    
    if len(title.strip()) > 255:
        return False, "Task title cannot exceed 255 characters"
    
    return True, "Title is valid"


def validate_user_exists(session: Session, user_id: str) -> bool:
    """Check if a user exists in the database"""
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user is not None


def validate_task_belongs_to_user(session: Session, task_id: str, user_id: str) -> bool:
    """Check if a task belongs to the specified user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task is not None


def validate_conversation_belongs_to_user(session: Session, conversation_id: str, user_id: str) -> bool:
    """Check if a conversation belongs to the specified user"""
    statement = select(Conversation).where(
        Conversation.id == conversation_id, 
        Conversation.user_id == user_id
    )
    conversation = session.exec(statement).first()
    return conversation is not None


class TaskValidationModel(BaseModel):
    """Pydantic model for validating task data"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
    
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Task title cannot be empty')
        return v.strip()


class UserValidationModel(BaseModel):
    """Pydantic model for validating user data"""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1)
    
    @validator('email')
    def validate_email_format(cls, v):
        if not validate_email(v):
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
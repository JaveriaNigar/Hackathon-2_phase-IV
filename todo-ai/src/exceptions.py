"""Custom exceptions for the Todo AI Chatbot API"""

from typing import Optional
from fastapi import HTTPException, status


class BaseTodoException(Exception):
    """Base exception class for todo-related errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code or status.HTTP_500_INTERNAL_SERVER_ERROR


class TaskNotFoundException(BaseTodoException):
    """Raised when a task is not found"""
    def __init__(self, task_id: str):
        super().__init__(
            message=f"Task with ID {task_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class TaskAccessDeniedException(BaseTodoException):
    """Raised when a user tries to access a task that doesn't belong to them"""
    def __init__(self, task_id: str, user_id: str):
        super().__init__(
            message=f"Access denied: Task {task_id} does not belong to user {user_id}",
            status_code=status.HTTP_403_FORBIDDEN
        )


class ConversationNotFoundException(BaseTodoException):
    """Raised when a conversation is not found"""
    def __init__(self, conversation_id: str):
        super().__init__(
            message=f"Conversation with ID {conversation_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class UserNotFoundException(BaseTodoException):
    """Raised when a user is not found"""
    def __init__(self, user_id: str):
        super().__init__(
            message=f"User with ID {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationErrorException(BaseTodoException):
    """Raised when validation fails"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class DatabaseOperationException(BaseTodoException):
    """Raised when a database operation fails"""
    def __init__(self, message: str):
        super().__init__(
            message=f"Database operation failed: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def handle_exception_as_http_error(exception: BaseTodoException) -> HTTPException:
    """Convert custom exceptions to HTTPException for FastAPI"""
    return HTTPException(
        status_code=exception.status_code,
        detail=exception.message
    )
"""Logging utilities for the Todo AI Chatbot API"""

import logging
import sys
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler


def setup_logger(
    name: str = "todo_ai_chatbot",
    log_file: Optional[str] = "logs/todo_app.log",
    level: int = logging.INFO
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        import os
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def log_api_call(
    logger: logging.Logger,
    endpoint: str,
    method: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    response_time: Optional[float] = None
):
    """Log API call details"""
    logger.info(
        f"API_CALL - Method: {method}, Endpoint: {endpoint}, "
        f"User: {user_id or 'Anonymous'}, IP: {ip_address or 'Unknown'}, "
        f"ResponseTime: {response_time or 'N/A'}ms"
    )


def log_error(
    logger: logging.Logger,
    error: Exception,
    context: Optional[str] = None,
    user_id: Optional[str] = None
):
    """Log error details with context"""
    logger.error(
        f"ERROR - Context: {context or 'Unknown'}, "
        f"User: {user_id or 'Anonymous'}, "
        f"Error: {str(error)}, "
        f"Type: {type(error).__name__}",
        exc_info=True  # Include traceback
    )


def log_task_operation(
    logger: logging.Logger,
    operation: str,  # 'create', 'update', 'delete', 'complete', etc.
    user_id: str,
    task_id: Optional[str] = None,
    details: Optional[str] = None
):
    """Log task-related operations"""
    logger.info(
        f"TASK_OPERATION - Operation: {operation}, "
        f"User: {user_id}, Task: {task_id or 'N/A'}, "
        f"Details: {details or 'N/A'}"
    )


def log_agent_interaction(
    logger: logging.Logger,
    user_id: str,
    conversation_id: str,
    input_text: str,
    response_text: str,
    tools_used: list = None
):
    """Log AI agent interactions"""
    logger.info(
        f"AGENT_INTERACTION - User: {user_id}, "
        f"Conversation: {conversation_id}, "
        f"Input: {input_text[:100]}..., "
        f"Response: {response_text[:100]}..., "
        f"Tools: {tools_used or 'None'}"
    )
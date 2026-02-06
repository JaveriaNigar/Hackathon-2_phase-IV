from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import logging
from src.database.session import get_session
from src.api.deps import verify_user_access
from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import TaskService
from src.utils.validation import validate_task_title
from src.utils.logging import log_error, log_task_operation
from src.exceptions import ValidationErrorException, TaskNotFoundException, TaskAccessDeniedException

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    try:
        # Validate task title
        is_valid, msg = validate_task_title(task_data.title)
        if not is_valid:
            raise ValidationErrorException(msg)

        # Create the task using the service
        task = TaskService.create_task(
            session=session,
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority
        )
        session.commit()
        session.refresh(task)

        # Log the task creation
        log_task_operation(
            logger=logger,
            operation="create",
            user_id=user_id,
            task_id=task.id,
            details=f"Created task: {task.title}"
        )

        return task
    except ValidationErrorException as ve:
        logger.error(f"Validation error in create_task: {ve.message}")
        raise HTTPException(status_code=ve.status_code, detail=ve.message)
    except Exception as e:
        log_error(logger, e, "create_task", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/tasks", response_model=List[TaskRead])
async def get_user_tasks(
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    try:
        # Get tasks for the user
        tasks = TaskService.get_user_tasks(session=session, user_id=user_id)
        return tasks
    except Exception as e:
        log_error(logger, e, "get_user_tasks", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to get user tasks: {str(e)}")


@router.get("/tasks/{id}", response_model=TaskRead)
async def get_task(
    id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    try:
        # Get the specific task
        task = TaskService.get_task_by_id(session=session, task_id=id, user_id=user_id)

        if not task:
            raise TaskNotFoundException(id)

        return task
    except TaskNotFoundException as tnfe:
        logger.error(f"Task not found in get_task: {tnfe.message}")
        raise HTTPException(status_code=tnfe.status_code, detail=tnfe.message)
    except Exception as e:
        log_error(logger, e, "get_task", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to get task: {str(e)}")


@router.put("/tasks/{id}", response_model=TaskRead)
async def update_task(
    id: str,
    task_update: TaskUpdate,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    try:
        logger.info(f"PUT /tasks/{id} - Request for user {user_id}")

        # Validate task title if it's being updated
        if task_update.title is not None:
            is_valid, msg = validate_task_title(task_update.title)
            if not is_valid:
                raise ValidationErrorException(msg)

        # Update the task
        updated_task = TaskService.update_task(
            session=session,
            task_id=id,
            user_id=user_id,
            task_update=task_update
        )
        if updated_task:
            session.commit()
            session.refresh(updated_task)

        if not updated_task:
            logger.warning(f"PUT /tasks/{id} - Task not found for user {user_id}")
            raise TaskNotFoundException(id)

        logger.info(f"PUT /tasks/{id} - Task updated successfully for user {user_id}")

        # Log the task update
        log_task_operation(
            logger=logger,
            operation="update",
            user_id=user_id,
            task_id=updated_task.id,
            details=f"Updated task: {updated_task.title}"
        )

        return updated_task
    except ValidationErrorException as ve:
        logger.error(f"Validation error in update_task: {ve.message}")
        raise HTTPException(status_code=ve.status_code, detail=ve.message)
    except TaskNotFoundException as tnfe:
        logger.error(f"Task not found in update_task: {tnfe.message}")
        raise HTTPException(status_code=tnfe.status_code, detail=tnfe.message)
    except Exception as e:
        log_error(logger, e, "update_task", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    try:
        logger.info(f"DELETE /tasks/{id} - Request for user {user_id}")

        # Delete the task
        deleted = TaskService.delete_task(session=session, task_id=id, user_id=user_id)
        if deleted:
            session.commit()

        if not deleted:
            logger.warning(f"DELETE /tasks/{id} - Task not found for user {user_id}")
            raise TaskNotFoundException(id)

        logger.info(f"DELETE /tasks/{id} - Task deleted successfully for user {user_id}")

        # Log the task deletion
        log_task_operation(
            logger=logger,
            operation="delete",
            user_id=user_id,
            task_id=id,
            details="Task deleted"
        )

        return {"message": "Task deleted successfully"}
    except TaskNotFoundException as tnfe:
        logger.error(f"Task not found in delete_task: {tnfe.message}")
        raise HTTPException(status_code=tnfe.status_code, detail=tnfe.message)
    except Exception as e:
        log_error(logger, e, "delete_task", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@router.patch("/tasks/{id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the authenticated user.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    try:
        logger.info(f"PATCH /tasks/{id}/complete - Request for user {user_id}")

        # Toggle task completion
        task = TaskService.toggle_completion(session=session, task_id=id, user_id=user_id)
        if task:
            session.commit()
            session.refresh(task)

        if not task:
            logger.warning(f"PATCH /tasks/{id}/complete - Task not found for user {user_id}")
            raise TaskNotFoundException(id)

        logger.info(f"PATCH /tasks/{id}/complete - Task completion toggled successfully for user {user_id}")

        # Log the task completion toggle
        log_task_operation(
            logger=logger,
            operation="toggle_completion",
            user_id=user_id,
            task_id=task.id,
            details=f"Toggled completion status to {task.completed}"
        )

        return task
    except TaskNotFoundException as tnfe:
        logger.error(f"Task not found in toggle_task_completion: {tnfe.message}")
        raise HTTPException(status_code=tnfe.status_code, detail=tnfe.message)
    except Exception as e:
        log_error(logger, e, "toggle_task_completion", user_id)
        raise HTTPException(status_code=500, detail=f"Failed to toggle task completion: {str(e)}")

@router.get("/pending-tasks", response_model=dict)
async def get_pending_tasks_count(
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Get the count of pending tasks for the authenticated user.
    Pending tasks are tasks that are not completed.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    logger.info(f"GET /pending-tasks - Request for user {user_id}")

    # Get the count of pending tasks
    pending_count = TaskService.get_pending_tasks_count(session=session, user_id=user_id)

    logger.info(f"GET /pending-tasks - Returning count: {pending_count} for user {user_id}")

    return {"pending": pending_count}

@router.get("/completed-tasks", response_model=dict)
async def get_completed_tasks_count(
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Get the count of completed tasks for the authenticated user.
    Completed tasks are tasks where completed = True.
    """
    # Get user_id from the verified JWT token (now verified against URL param)
    user_id = payload.get("userId") or payload.get("sub")

    logger.info(f"GET /completed-tasks - Request for user {user_id}")

    # Get the count of completed tasks
    completed_count = TaskService.get_completed_tasks_count(session=session, user_id=user_id)

    logger.info(f"GET /completed-tasks - Returning count: {completed_count} for user {user_id}")

    return {"completed": completed_count}
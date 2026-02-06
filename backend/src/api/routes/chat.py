from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from ...agents.todo_agent import TodoAgent
from ...tools.task_tools import TaskTools
from ...api.deps import verify_user_access
from ...database.session import get_session
from ...utils.validation import validate_task_title
from ...utils.logging import log_agent_interaction, log_error
from ...exceptions import ValidationErrorException, DatabaseOperationException
from sqlmodel import Session, select, desc
import logging
import os

# Setup logger
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic models for request/response
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[ToolCall] = []


class ConversationRead(BaseModel):
    id: UUID
    user_id: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class MessageRead(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime


# Removed local get_db to use src.database.session.get_session


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that processes natural language and returns AI response
    along with any tool calls that need to be executed.
    """
    try:
        # Validate input
        if not request.message or not request.message.strip():
            raise ValidationErrorException("Message cannot be empty")

        # Get database URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise HTTPException(status_code=500, detail="DATABASE_URL not configured")

        if request.conversation_id:
            try:
                conv_uuid = UUID(request.conversation_id)
            except ValueError:
                # Handle non-UUID temp IDs
                conv_uuid = None
        else:
            conv_uuid = None

        from ...models.conversation import Conversation
        from ...models.message import Message as DBMessage

        # Ensure conversation exists or create one if requested/needed
        if conv_uuid:
            conversation = session.get(Conversation, conv_uuid)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conv_uuid = conversation.id

        # Initialize the agent
        agent = TodoAgent(database_url=database_url)

        # Save user message
        user_msg = DBMessage(
            user_id=user_id,
            conversation_id=conv_uuid,
            role="user",
            content=request.message
        )
        session.add(user_msg)
        session.commit()

        # Process the user message with the agent
        result = agent.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=str(conv_uuid)
        )

        # Update conversation title if new and agent provided one
        if not conversation.title and result.get("chat_title"):
            conversation.title = result.get("chat_title")
            session.add(conversation)
            session.commit()

        # EXECUTE TOOLS FIRST
        from ...services.task_service import TaskService
        from ...models.task import TaskUpdate

        execution_errors = []

        for tool_call in result.get("tool_calls", []):
            name = tool_call.get("name")
            args = tool_call.get("arguments", {})

            try:
                if name == "add_task":
                    # Validate task title before creating
                    title = args.get("title")
                    is_valid, msg = validate_task_title(title) if title else (False, "Task title is required")
                    if not is_valid:
                        error_msg = f"add_task failed: {msg}"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)
                        continue

                    TaskService.create_task(
                        session=session,
                        user_id=user_id,
                        title=title,
                        description=args.get("description")
                    )
                elif name == "delete_task":
                    task_id = args.get("task_id") or args.get("title")
                    if not task_id:
                        error_msg = "delete_task failed: Task ID or title is required"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)
                        continue

                    task, status = TaskService.resolve_task(session, user_id, task_id)
                    if status == "FOUND":
                        TaskService.delete_task(
                            session=session,
                            user_id=user_id,
                            task_id=task.id
                        )
                    else:
                        error_msg = f"delete_task failed: Task '{task_id}' not found ({status})"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)

                elif name == "complete_task":
                    task_id = args.get("task_id") or args.get("title")
                    if not task_id:
                        error_msg = "complete_task failed: Task ID or title is required"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)
                        continue

                    task, status = TaskService.resolve_task(session, user_id, task_id)
                    if status == "FOUND":
                        TaskService.complete_task(
                            session=session,
                            user_id=user_id,
                            task_id=task.id
                        )
                    else:
                         error_msg = f"complete_task failed: Task '{task_id}' not found ({status})"
                         logger.warning(error_msg)
                         execution_errors.append(error_msg)

                elif name == "update_task":
                    task_id = args.get("task_id") or args.get("old_title") or args.get("title")
                    new_title = args.get("new_title") or args.get("title")

                    if not task_id:
                        error_msg = "update_task failed: Task ID or title is required"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)
                        continue

                    if not new_title:
                        error_msg = "update_task failed: New title is required"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)
                        continue

                    # Validate new title
                    is_valid, msg = validate_task_title(new_title)
                    if not is_valid:
                        error_msg = f"update_task failed: {msg}"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)
                        continue

                    task, status = TaskService.resolve_task(session, user_id, task_id)
                    if status == "FOUND":
                        # Construct update payload dynamically to avoid resetting fields to None
                        update_payload = {}
                        if new_title:
                            update_payload["title"] = new_title
                        if "description" in args:
                            update_payload["description"] = args["description"]
                        if "completed" in args:
                            update_payload["completed"] = args["completed"]

                        task_update = TaskUpdate(**update_payload)

                        TaskService.update_task(
                            session=session,
                            user_id=user_id,
                            task_id=task.id,
                            task_update=task_update
                        )
                    else:
                        error_msg = f"update_task failed: Task '{task_id}' not found ({status})"
                        logger.warning(error_msg)
                        execution_errors.append(error_msg)

                elif name == "list_tasks":
                    # This tool call is mainly a signal for the UI to refresh or for the agent's context
                    # in the NEXT turn. For now, it doesn't return data to the user in this response
                    # because the response text was already generated.
                    TaskService.get_user_tasks(session=session, user_id=user_id, status=args.get("status", "all"))

                logger.info(f"Successfully executed tool: {name} for user {user_id}")
            except Exception as tool_err:
                error_msg = f"Error executing {name}: {str(tool_err)}"
                logger.error(error_msg)
                execution_errors.append(error_msg)

        # Explicitly commit all changes made by tools
        session.commit()

        # Update response text if there were errors
        final_response_text = result.get("response", "I processed your request.")
        if execution_errors:
            final_response_text += "\n\n(Note: Some actions encountered errors: " + "; ".join(execution_errors) + ")"

        # Save assistant response AFTER tools are executed
        assistant_msg = DBMessage(
            user_id=user_id,
            conversation_id=conv_uuid,
            role="assistant",
            content=final_response_text
        )
        session.add(assistant_msg)
        session.commit()

        # Log the agent interaction
        log_agent_interaction(
            logger=logger,
            user_id=user_id,
            conversation_id=str(conv_uuid),
            input_text=request.message,
            response_text=final_response_text,
            tools_used=[tc.get("name") for tc in result.get("tool_calls", [])]
        )

        # Format the response
        response = ChatResponse(
            conversation_id=str(conv_uuid),
            response=final_response_text,
            tool_calls=result.get("tool_calls", [])
        )

        return response
    except ValidationErrorException as ve:
        logger.error(f"Validation error in chat endpoint: {ve.message}")
        raise HTTPException(status_code=ve.status_code, detail=ve.message)
    except HTTPException:
        raise
    except Exception as e:
        log_error(logger, e, "chat_endpoint", user_id)
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.get("/conversations", response_model=List[ConversationRead])
async def list_conversations(
    user_id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    from ...models.conversation import Conversation
    
    statement = select(Conversation).where(Conversation.user_id == user_id).order_by(desc(Conversation.updated_at))
    results = session.exec(statement).all()
    return results


@router.post("/conversations", response_model=ConversationRead)
async def create_conversation(
    user_id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    from ...models.conversation import Conversation
    
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
async def list_conversation_messages(
    user_id: str,
    conversation_id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    from ...models.message import Message as DBMessage
    
    try:
        conv_uuid = UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID")

    statement = select(DBMessage).where(
        DBMessage.user_id == user_id,
        DBMessage.conversation_id == conv_uuid
    ).order_by(DBMessage.created_at)
    
    results = session.exec(statement).all()
    return results


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_id: str,
    payload: dict = Depends(verify_user_access),
    session: Session = Depends(get_session)
):
    from ...models.conversation import Conversation
    from ...models.message import Message as DBMessage
    
    try:
        conv_uuid = UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation ID")

    # Use explicit join or check to ensure user owns it
    conversation = session.get(Conversation, conv_uuid)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Delete all messages first (if no cascade)
    statement = select(DBMessage).where(DBMessage.conversation_id == conv_uuid)
    messages = session.exec(statement).all()
    for msg in messages:
        session.delete(msg)

    session.delete(conversation)
    session.commit()
    
    return {"success": True, "message": "Conversation deleted"}

# Note: Task management endpoints...
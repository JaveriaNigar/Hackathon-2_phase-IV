from typing import Dict, Any
from sqlmodel import Session, create_engine, SQLModel
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..models.task import TaskBase
import uuid


class TaskTools:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        # Create tables if they don't exist
        SQLModel.metadata.create_all(self.engine)
        self.task_service = TaskService()
        self.conversation_service = ConversationService()
        self.message_service = MessageService()

    def get_db_session(self) -> Session:
        """Get a database session"""
        db = Session(bind=self.engine)
        try:
            return db
        except Exception:
            db.close()
            raise

    def add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Add a new task for the user"""
        db = self.get_db_session()
        try:
            task = self.task_service.create_task(db, user_id, title, description)
            return {
                "success": True,
                "task_id": str(task.id),
                "message": f"Task '{task.title}' has been added successfully."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to add task: {str(e)}"
            }
        finally:
            db.close()

    def list_tasks(self, user_id: str, status: str = "all") -> Dict[str, Any]:
        """List tasks for the user based on status"""
        db = self.get_db_session()
        try:
            tasks = self.task_service.get_user_tasks(db, user_id, status)
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                })
            
            status_display = "all" if status == "all" else status
            return {
                "success": True,
                "message": f"Found {len(task_list)} {status_display} tasks.",
                "tasks": task_list
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to list tasks: {str(e)}"
            }
        finally:
            db.close()

    def update_task(self, user_id: str, task_id: str, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
        """Update an existing task"""
        db = self.get_db_session()
        try:
            # Get the current task
            current_task = self.task_service.get_task_by_id(db, user_id, task_id)
            if not current_task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found."
                }
            
            # Prepare update data
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if completed is not None:
                update_data["completed"] = completed
            
            # Perform the update
            # We need to bridge TaskUpdate pydantic model IF update_task expects it
            # From TaskService.update_task: update_data = task_update.model_dump(exclude_unset=True)
            # but we are passing a dict or pydantic? Let's check TaskService again.
            # TaskService.update_task expects 'task_update' to have model_dump.
            from ..models.task import TaskUpdate
            task_update = TaskUpdate(
                title=title,
                description=description,
                completed=completed
            )
            
            updated_task = self.task_service.update_task(db, task_id, user_id, task_update)
            if updated_task:
                return {
                    "success": True,
                    "message": f"Task '{updated_task.title}' has been updated successfully."
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to update task with ID {task_id}."
                }
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid task ID format: {task_id}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update task: {str(e)}"
            }
        finally:
            db.close()

    def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Mark a task as completed"""
        db = self.get_db_session()
        try:
            completed_task = self.task_service.complete_task(db, user_id, task_id)
            if completed_task:
                return {
                    "success": True,
                    "message": f"Task '{completed_task.title}' has been marked as completed."
                }
            else:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or could not be completed."
                }
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid task ID format: {task_id}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to complete task: {str(e)}"
            }
        finally:
            db.close()

    def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Delete a task"""
        db = self.get_db_session()
        try:
            success = self.task_service.delete_task(db, user_id, task_id)
            if success:
                return {
                    "success": True,
                    "message": f"Task with ID {task_id} has been deleted successfully."
                }
            else:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found or could not be deleted."
                }
        except ValueError:
            return {
                "success": False,
                "message": f"Invalid task ID format: {task_id}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}"
            }
        finally:
            db.close()

    def search_tasks(self, user_id: str, query: str) -> Dict[str, Any]:
        """Search for tasks by title"""
        db = self.get_db_session()
        try:
            tasks = self.task_service.search_user_tasks(db, user_id, query)
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "completed": task.completed
                })
            return {
                "success": True,
                "tasks": task_list
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to search tasks: {str(e)}"
            }
        finally:
            db.close()
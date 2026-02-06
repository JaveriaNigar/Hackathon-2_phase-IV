from typing import List, Optional
from sqlmodel import Session, select, func
from ..models.task import Task, TaskBase


class TaskService:
    @staticmethod
    def create_task(session: Session, user_id: str, title: str, description: str = None,
                    due_date=None, priority: str = None) -> Task:
        """Create a new task for a user"""
        import uuid

        # Generate the ID first
        task_id = str(uuid.uuid4()).replace('-', '')[:32]

        # Create task with all the fields that are known to exist in the database
        # The due_date and priority fields may not exist in the current database schema
        task_data = {
            'id': task_id,
            'user_id': user_id,
            'title': title,
            'description': description,
            'completed': False  # Default to not completed
        }

        # Only add due_date and priority if they're not None to avoid inserting NULL unnecessarily
        if due_date is not None:
            task_data['due_date'] = due_date
        if priority is not None:
            task_data['priority'] = priority

        task = Task(**task_data)
        session.add(task)
        # session.commit() is now handled by the caller
        return task

    @staticmethod
    def get_user_tasks(session: Session, user_id: str, status: Optional[str] = None) -> List[Task]:
        """Get all tasks for a user, optionally filtered by status"""
        query = select(Task).where(Task.user_id == user_id)

        if status:
            if status.lower() == "pending":
                query = query.where(Task.completed == False)
            elif status.lower() == "completed":
                query = query.where(Task.completed == True)

        return session.exec(query).all()

    @staticmethod
    def get_task_by_id(session: Session, user_id: str, task_id: str) -> Optional[Task]:
        """Get a specific task by ID for a user"""
        query = select(Task).where(Task.user_id == user_id, Task.id == task_id)
        return session.exec(query).first()

    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: str) -> bool:
        """Delete a specific task for a user"""
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if not task:
            return False

        session.delete(task)
        # session.commit() is now handled by the caller
        return True

    @staticmethod
    def complete_task(session: Session, user_id: str, task_id: str) -> Optional[Task]:
        """Mark a task as completed"""
        task = TaskService.get_task_by_id(session, user_id, task_id)
        if not task:
            return None

        task.completed = True
        task.updated_at = func.now()
        session.add(task)
        # session.commit() is now handled by the caller
        return task

    @staticmethod
    def toggle_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Toggle the completion status of a task"""
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()

        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = func.now()
        session.add(task)
        # session.commit() is now handled by the caller
        return task

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, task_update) -> Optional[Task]:
        """Update a specific task for a user"""
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()

        if not task:
            return None

        # Update task attributes with values from task_update
        # Convert the Pydantic model to a dictionary
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        task.updated_at = func.now()
        session.add(task)
        # session.commit() is now handled by the caller
        return task

    @staticmethod
    def get_pending_tasks_count(session: Session, user_id: str) -> int:
        """Get the count of pending tasks for a user"""
        query = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == False
        )
        return session.exec(query).one()

    @staticmethod
    def get_completed_tasks_count(session: Session, user_id: str) -> int:
        """Get the count of completed tasks for a user"""
        query = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == True
        )
        return session.exec(query).one()

    @staticmethod
    def search_user_tasks(session: Session, user_id: str, query_str: str) -> List[Task]:
        """Search tasks for a user by title (case-insensitive)"""
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.title.ilike(f"%{query_str}%")
        )
        return session.exec(statement).all()

    @staticmethod
    def resolve_task(session: Session, user_id: str, identifier: str):
        """
        Resolve a task by ID or Title.
        Returns (task, status) where status is 'FOUND', 'AMBIGUOUS', or 'NOT_FOUND'.
        """
        if not identifier:
            return None, "NOT_FOUND"

        # Normalization: Trim whitespace and strip surrounding quotes/brackets
        identifier = identifier.strip().strip('"').strip("'").strip('[]').strip('()').strip('{}').strip()
        
        if not identifier:
            return None, "NOT_FOUND"
        # IDs are 32 chars long (without hyphens) in this project
        if len(identifier) >= 30:
            task = TaskService.get_task_by_id(session, user_id, identifier)
            if task:
                return task, "FOUND"

        # 2. Try Exact Title match
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.title.ilike(identifier)
        )
        exact_matches = session.exec(statement).all()
        if len(exact_matches) == 1:
            return exact_matches[0], "FOUND"
        elif len(exact_matches) > 1:
            return None, "AMBIGUOUS"

        # 3. Try Partial Title match
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.title.ilike(f"%{identifier}%")
        )
        partial_matches = session.exec(statement).all()
        if len(partial_matches) == 1:
            return partial_matches[0], "FOUND"
        elif len(partial_matches) > 1:
            return None, "AMBIGUOUS"

        return None, "NOT_FOUND"
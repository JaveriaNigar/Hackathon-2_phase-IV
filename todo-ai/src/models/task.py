from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)
    priority: Optional[str] = Field(default=None, max_length=20)


def generate_task_id():
    import uuid
    return str(uuid.uuid4()).replace('-', '')[:32]


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: str = Field(default_factory=generate_task_id, primary_key=True, sa_column_kwargs={"default": None})
    user_id: str = Field(index=True)
    due_date: Optional[datetime] = Field(default=None)
    priority: Optional[str] = Field(default=None, max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Pydantic models for API requests/responses
class TaskCreate(TaskBase):
    # Don't redefine fields that are already in TaskBase
    # Just inherit them as they are
    pass


class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None


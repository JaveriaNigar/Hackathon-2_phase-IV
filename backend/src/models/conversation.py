from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)
    title: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    # Additional field to track context if needed
    context_data: Optional[str] = Field(default=None, max_length=5000)
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(regex="^(user|assistant)$")  # Either "user" or "assistant"
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
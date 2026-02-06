from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


def generate_user_id():
    return str(uuid.uuid4())


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str = Field(nullable=False)


class User(UserBase, table=True):
    id: str = Field(default_factory=generate_user_id, primary_key=True)
    password_hash: str = Field(nullable=False)   # ✅ FIXED (was password)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str   # ✅ form se password yahin ayega


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None

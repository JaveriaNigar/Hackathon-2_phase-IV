from typing import List, Optional
from sqlmodel import Session, select, func
from ..models.message import Message
import uuid


class MessageService:
    def create_message(self, session: Session, user_id: str, conversation_id: uuid.UUID, role: str, content: str) -> Message:
        """Create a new message in a conversation"""
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_messages_by_conversation(self, session: Session, user_id: str, conversation_id: uuid.UUID) -> List[Message]:
        """Get all messages in a specific conversation for a user"""
        query = select(Message).where(
            Message.user_id == user_id,
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
        return session.exec(query).all()

    def get_message_by_id(self, session: Session, user_id: str, message_id: uuid.UUID) -> Optional[Message]:
        """Get a specific message by ID for a user"""
        query = select(Message).where(
            Message.user_id == user_id,
            Message.id == message_id
        )
        return session.exec(query).first()

    def update_message(self, session: Session, user_id: str, message_id: uuid.UUID, message_data: dict) -> Optional[Message]:
        """Update a specific message for a user"""
        message = self.get_message_by_id(session, user_id, message_id)
        if not message:
            return None
            
        for key, value in message_data.items():
            if hasattr(message, key):
                setattr(message, key, value)
                
        message.updated_at = func.now()
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def delete_message(self, session: Session, user_id: str, message_id: uuid.UUID) -> bool:
        """Delete a specific message for a user"""
        message = self.get_message_by_id(session, user_id, message_id)
        if not message:
            return False
            
        session.delete(message)
        session.commit()
        return True
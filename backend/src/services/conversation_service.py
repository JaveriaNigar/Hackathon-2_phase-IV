from typing import List, Optional
from sqlmodel import Session, select, func
from ..models.conversation import Conversation
import uuid


class ConversationService:
    def create_conversation(self, session: Session, user_id: str) -> Conversation:
        """Create a new conversation for a user"""
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_user_conversations(self, session: Session, user_id: str) -> List[Conversation]:
        """Get all conversations for a user"""
        query = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(query).all()

    def get_conversation_by_id(self, session: Session, user_id: str, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """Get a specific conversation by ID for a user"""
        query = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.id == conversation_id
        )
        return session.exec(query).first()

    def update_conversation(self, session: Session, user_id: str, conversation_id: uuid.UUID, conversation_data: dict) -> Optional[Conversation]:
        """Update a specific conversation for a user"""
        conversation = self.get_conversation_by_id(session, user_id, conversation_id)
        if not conversation:
            return None

        for key, value in conversation_data.items():
            if hasattr(conversation, key):
                setattr(conversation, key, value)

        conversation.updated_at = func.now()
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def delete_conversation(self, session: Session, user_id: str, conversation_id: uuid.UUID) -> bool:
        """Delete a specific conversation for a user"""
        conversation = self.get_conversation_by_id(session, user_id, conversation_id)
        if not conversation:
            return False

        session.delete(conversation)
        session.commit()
        return True
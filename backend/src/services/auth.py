import logging
from sqlmodel import Session, select
from typing import Optional
from src.models.user import User, UserCreate
from src.utils.jwt_util import create_access_token
from passlib.context import CryptContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """
    Auth service with secure password hashing.
    """

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        try:
            # Normalize email: strip whitespace and convert to lower case
            normalized_email = email.strip().lower()
            
            user = session.exec(
                select(User).where(User.email == normalized_email)
            ).first()

            if not user:
                return None

            # Verify the password (hashed or plain-text fallback)
            is_valid = False
            try:
                is_valid = pwd_context.verify(password, user.password_hash)
            except Exception:
                # Fallback for legacy plain-text passwords
                is_valid = (user.password_hash == password)

            if not is_valid:
                return None

            return user

        except Exception as e:
            logger.error(f"Login error: {e}")
            return None

    @staticmethod
    def register_user(session: Session, user_create: UserCreate) -> User:
        try:
            # Normalize email: strip whitespace and convert to lower case
            normalized_email = user_create.email.strip().lower()
            
            existing_user = session.exec(
                select(User).where(User.email == normalized_email)
            ).first()

            if existing_user:
                raise ValueError("Email already registered. Please login.")

            # Hash the password before storing
            hashed_password = pwd_context.hash(user_create.password)

            user = User(
                email=normalized_email,
                name=user_create.name.strip(),
                password_hash=hashed_password
            )

            session.add(user)
            session.flush()  # This ensures the ID is generated without committing
            # Note: session commit is handled by FastAPI dependency system

            return user

        except Exception as e:
            logger.error(f"Signup error: {e}")
            raise

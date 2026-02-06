from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database.session import get_session
from src.models.user import UserCreate
from src.services.auth import AuthService
from src.utils.jwt_util import create_access_token
from pydantic import BaseModel
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")

# Define request models for login
class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: str
    email: str
    token: str

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user with plain text password.
    """
    try:
        # Register the user - this will commit the transaction
        user = AuthService.register_user(session, user_create)

        # Create access token after successful user creation
        access_token_expires = timedelta(minutes=30)
        token_data = {"sub": user.id, "userId": user.id}
        access_token = create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        # Return success response with token
        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": user.id,
            "email": user.email,
            "token": access_token
        }
    except ValueError as e:
        # User already exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # General error
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login", response_model=AuthResponse)
def login(login_request: LoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user with plain text password.
    """
    try:
        user = AuthService.authenticate_user(session, login_request.email, login_request.password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Create access token after successful authentication
        access_token_expires = timedelta(minutes=30)
        token_data = {"sub": user.id, "userId": user.id}
        access_token = create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        # Return success response with token
        return {
            "success": True,
            "message": "Login successful",
            "user_id": user.id,
            "email": user.email,
            "token": access_token
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )
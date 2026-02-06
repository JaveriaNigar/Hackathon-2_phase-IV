from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database.session import get_session
from src.api.deps import verify_jwt_token
from src.models.user import UserRead
from src.models.user import User

router = APIRouter(prefix="/user")

@router.get("/", response_model=UserRead)
def get_current_user(
    payload: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Get the current authenticated user's profile information.
    """
    user_id = payload.get("userId") or payload.get("sub")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    # Fetch the user from the database
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Get JWT secret from environment variable
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def create_test_token(user_id: str, expires_delta: timedelta = None):
    """
    Create a test JWT token for the given user_id.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)  # Token valid for 15 minutes
    
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
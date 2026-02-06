from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging
from dotenv import load_dotenv
from jose import jwt, JWTError
from typing import Optional

print("DEBUG: deps.py is being loaded")

# Setup logger
logger = logging.getLogger(__name__)

# Load environment variables explicitly from the backend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

# Get JWT secret from environment variable
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    # Try local directory as fallback
    load_dotenv(dotenv_path='.env', override=True)
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

print(f"DEBUG: SECRET_KEY loaded: {'Yes' if SECRET_KEY else 'No'}")

ALGORITHM = "HS256"

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify the JWT token and return the payload if valid.
    """
    print(f"\n[JWT DEBUG] verify_jwt_token called with credentials present")
    token = credentials.credentials

    if not SECRET_KEY:
        print("[JWT ERROR] BETTER_AUTH_SECRET is not set!")
        raise HTTPException(status_code=500, detail="Authentication secret not configured")

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"[JWT SUCCESS] Decoded payload: {payload}")
        return payload
    except JWTError as e:
        print(f"[JWT FAILURE] Verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")
    except Exception as e:
        print(f"[JWT FAILURE] Token validation error: {str(e)}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def verify_user_access(user_id: str, request: Request, payload: dict = Depends(verify_jwt_token)):
    """
    Verify that the authenticated user matches the user_id in the URL path.
    """
    # Extract user_id from JWT payload
    token_user_id = payload.get("userId") or payload.get("sub")

    # Extract user_id from the URL path (parameter user_id is injected by FastAPI)
    path_user_id = user_id

    # Log with absolute visibility to terminal
    print(f"\n[AUTH DEBUG] TokenID: {repr(token_user_id)} | PathID: {repr(path_user_id)}")
    print(f"[AUTH DEBUG] Path Params: {request.path_params}\n")

    if not token_user_id or not path_user_id:
        print(f"[AUTH ERROR] Missing IDs. Token={repr(token_user_id)}, Path={repr(path_user_id)}")
        raise HTTPException(status_code=403, detail="Access forbidden: Missing identifying information")

    # Convert to string and strip
    token_user_id = str(token_user_id).strip()
    path_user_id = str(path_user_id).strip()

    # Verify that the authenticated user matches the requested user_id
    if token_user_id != path_user_id:
        detail_msg = f"Access forbidden: User ID mismatch. Token ID: {token_user_id}, Path ID: {path_user_id}"
        print(f"[AUTH MISMATCH] {detail_msg}")
        raise HTTPException(status_code=403, detail=detail_msg)

    return payload
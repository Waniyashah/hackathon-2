from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt

# Get secret key and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with expiration
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 30 minutes if no expiration is provided
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify the JWT token and return the payload if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Log the error for debugging (in production, use proper logging)
        print(f"JWT verification failed for token: {token[:10]}...")
        return None


def decode_token(token: str) -> Optional[dict]:
    """
    Decode the JWT token without verification (for non-sensitive operations)
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from token payload
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None
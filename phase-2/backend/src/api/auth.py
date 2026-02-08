from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import Session
from passlib.context import CryptContext
from datetime import timedelta
import uuid

from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserResponse, UserRegister
from ..database.session import get_session
from ..middleware.auth import create_access_token
from ..api.utils import handle_error
from ..services.auth_service import authenticate_user, create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
async def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    """
    Register a new user and return access token
    """
    # Force reload
    try:
        # Validate that passwords match
        if user_data.password != user_data.confirmPassword:
            handle_error("Passwords do not match", status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        existing_user = session.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            handle_error("Email already registered", status.HTTP_409_CONFLICT)

        # Create UserCreate object (without confirmPassword) for the service
        user_create = UserCreate(email=user_data.email, password=user_data.password)

        # Create new user
        db_user = await create_user(user_create, session)

        # Create access token for the new user
        access_token = create_access_token(
            data={"sub": str(db_user.id)}, expires_delta=30  # 30 minutes expiry
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=db_user.id,
                email=db_user.email,
                created_at=db_user.created_at
            )
        }
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        handle_error(f"Registration failed: {str(e)}")


@router.post("/signin")
async def login_user(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login user and return access token
    """
    try:
        user = await authenticate_user(session, user_credentials.email, user_credentials.password)
        if not user:
            handle_error("Incorrect email or password", status.HTTP_401_UNAUTHORIZED)

        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=30  # 30 minutes expiry
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at
            )
        }
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        handle_error(f"Login failed: {str(e)}")


@router.post("/signout")
async def signout_user():
    """
    Sign out user (client-side operation, no server-side state to clear in JWT)
    """
    return {"message": "Successfully signed out"}
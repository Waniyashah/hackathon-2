from sqlmodel import Session
from passlib.context import CryptContext
from typing import Optional
import uuid
from datetime import datetime

from ..models.user import User
from ..schemas.user import UserCreate

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its hash
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password
    """
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


async def create_user(user_data: UserCreate, session: Session) -> User:
    """
    Create a new user with hashed password
    """
    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create the user object
    db_user = User(
        id=uuid.uuid4(),
        email=user_data.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add to session and commit
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
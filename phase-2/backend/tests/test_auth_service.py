import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
import bcrypt
from datetime import datetime

from src.services.auth_service import (
    hash_password,
    verify_password,
    authenticate_user,
    create_user
)
from src.models.user import User
from src.schemas.user import UserCreate


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        password = "test_password_123"
        hashed = hash_password(password)
        assert isinstance(hashed, str)

    def test_hash_password_different_each_time(self):
        """Test that hashing the same password produces different hashes (due to salt)"""
        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2

    def test_hash_password_valid_bcrypt_format(self):
        """Test that the hash is in valid bcrypt format"""
        password = "test_password_123"
        hashed = hash_password(password)
        # Bcrypt hashes start with $2b$ and are 60 characters long
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60

    def test_verify_password_correct_password(self):
        """Test that verify_password returns True for correct password"""
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect_password(self):
        """Test that verify_password returns False for incorrect password"""
        password = "test_password_123"
        wrong_password = "wrong_password_456"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_password(self):
        """Test that verify_password handles empty password"""
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password("", hashed) is False

    def test_verify_password_special_characters(self):
        """Test password hashing with special characters"""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_unicode_characters(self):
        """Test password hashing with unicode characters"""
        password = "пароль密码🔒"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True


class TestAuthenticateUser:
    """Test user authentication"""

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, session: Session):
        """Test successful user authentication"""
        # Create a test user
        user_data = UserCreate(email="test@example.com", password="password123")
        user = await create_user(user_data, session)

        # Authenticate the user
        authenticated_user = await authenticate_user(session, "test@example.com", "password123")

        assert authenticated_user is not None
        assert authenticated_user.id == user.id
        assert authenticated_user.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, session: Session):
        """Test authentication with wrong password"""
        # Create a test user
        user_data = UserCreate(email="test@example.com", password="password123")
        await create_user(user_data, session)

        # Try to authenticate with wrong password
        authenticated_user = await authenticate_user(session, "test@example.com", "wrong_password")

        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_authenticate_user_nonexistent_email(self, session: Session):
        """Test authentication with non-existent email"""
        authenticated_user = await authenticate_user(session, "nonexistent@example.com", "password123")
        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_authenticate_user_empty_password(self, session: Session):
        """Test authentication with empty password"""
        # Create a test user
        user_data = UserCreate(email="test@example.com", password="password123")
        await create_user(user_data, session)

        # Try to authenticate with empty password
        authenticated_user = await authenticate_user(session, "test@example.com", "")

        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_authenticate_user_case_sensitive_email(self, session: Session):
        """Test that email authentication is case-sensitive"""
        # Create a test user
        user_data = UserCreate(email="test@example.com", password="password123")
        await create_user(user_data, session)

        # Try to authenticate with different case email
        authenticated_user = await authenticate_user(session, "TEST@EXAMPLE.COM", "password123")

        # Should be None because email is case-sensitive in our implementation
        assert authenticated_user is None


class TestCreateUser:
    """Test user creation"""

    @pytest.mark.asyncio
    async def test_create_user_success(self, session: Session):
        """Test successful user creation"""
        user_data = UserCreate(email="newuser@example.com", password="password123")
        user = await create_user(user_data, session)

        assert user is not None
        assert user.email == "newuser@example.com"
        assert user.id is not None
        assert user.password_hash is not None
        assert user.password_hash != "password123"  # Password should be hashed
        assert user.created_at is not None
        assert user.updated_at is not None

    @pytest.mark.asyncio
    async def test_create_user_password_is_hashed(self, session: Session):
        """Test that password is properly hashed"""
        user_data = UserCreate(email="newuser@example.com", password="password123")
        user = await create_user(user_data, session)

        # Verify the password hash is valid bcrypt format
        assert user.password_hash.startswith("$2b$")
        assert len(user.password_hash) == 60

        # Verify the password can be verified
        assert verify_password("password123", user.password_hash) is True

    @pytest.mark.asyncio
    async def test_create_user_uuid_generated(self, session: Session):
        """Test that UUID is generated for new user"""
        user_data = UserCreate(email="newuser@example.com", password="password123")
        user = await create_user(user_data, session)

        # Check that ID is a valid UUID
        assert user.id is not None
        assert len(str(user.id)) == 36  # UUID string length with hyphens

    @pytest.mark.asyncio
    async def test_create_user_timestamps_set(self, session: Session):
        """Test that timestamps are set correctly"""
        user_data = UserCreate(email="newuser@example.com", password="password123")
        user = await create_user(user_data, session)

        assert user.created_at is not None
        assert user.updated_at is not None
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    @pytest.mark.asyncio
    async def test_create_user_persisted_to_database(self, session: Session):
        """Test that user is persisted to database"""
        user_data = UserCreate(email="newuser@example.com", password="password123")
        user = await create_user(user_data, session)

        # Query the database to verify user exists
        db_user = session.get(User, user.id)
        assert db_user is not None
        assert db_user.email == "newuser@example.com"

    @pytest.mark.asyncio
    async def test_create_multiple_users(self, session: Session):
        """Test creating multiple users"""
        user1_data = UserCreate(email="user1@example.com", password="password123")
        user2_data = UserCreate(email="user2@example.com", password="password456")

        user1 = await create_user(user1_data, session)
        user2 = await create_user(user2_data, session)

        assert user1.id != user2.id
        assert user1.email != user2.email
        assert user1.password_hash != user2.password_hash

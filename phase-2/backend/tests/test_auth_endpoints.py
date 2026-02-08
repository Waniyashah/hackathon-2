import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from main import app
from src.database.session import get_session


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


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with test database"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestAuthenticationEndpoints:
    """Integration tests for authentication endpoints"""

    def test_signup_success(self, client: TestClient):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["email"] == "newuser@example.com"
        assert "created_at" in data
        assert "password" not in data  # Password should not be returned

    def test_signup_duplicate_email(self, client: TestClient):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/api/auth/signup",
            json={
                "email": "duplicate@example.com",
                "password": "password123"
            }
        )

        # Second registration with same email
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "duplicate@example.com",
                "password": "password456"
            }
        )

        assert response.status_code == 409  # Conflict

    def test_signup_invalid_email(self, client: TestClient):
        """Test registration with invalid email format"""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "invalid-email",
                "password": "password123"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signup_missing_password(self, client: TestClient):
        """Test registration without password"""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "test@example.com"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signup_missing_email(self, client: TestClient):
        """Test registration without email"""
        response = client.post(
            "/api/auth/signup",
            json={
                "password": "password123"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signin_success(self, client: TestClient):
        """Test successful user login"""
        # First register a user
        client.post(
            "/api/auth/signup",
            json={
                "email": "loginuser@example.com",
                "password": "password123"
            }
        )

        # Then login
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "loginuser@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "loginuser@example.com"

    def test_signin_wrong_password(self, client: TestClient):
        """Test login with incorrect password"""
        # First register a user
        client.post(
            "/api/auth/signup",
            json={
                "email": "loginuser@example.com",
                "password": "password123"
            }
        )

        # Try to login with wrong password
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "loginuser@example.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401  # Unauthorized

    def test_signin_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 401  # Unauthorized

    def test_signin_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format"""
        response = client.post(
            "/api/auth/signin",
            json={
                "email": "invalid-email",
                "password": "password123"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_signout_endpoint(self, client: TestClient):
        """Test signout endpoint"""
        response = client.post("/api/auth/signout")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_jwt_token_format(self, client: TestClient):
        """Test that JWT token has correct format"""
        # Register and login
        client.post(
            "/api/auth/signup",
            json={
                "email": "tokentest@example.com",
                "password": "password123"
            }
        )

        response = client.post(
            "/api/auth/signin",
            json={
                "email": "tokentest@example.com",
                "password": "password123"
            }
        )

        data = response.json()
        token = data["access_token"]

        # JWT tokens have 3 parts separated by dots
        parts = token.split(".")
        assert len(parts) == 3

    def test_complete_auth_flow(self, client: TestClient):
        """Test complete authentication flow: signup -> signin -> signout"""
        # Step 1: Signup
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "flowtest@example.com",
                "password": "password123"
            }
        )
        assert signup_response.status_code == 200

        # Step 2: Signin
        signin_response = client.post(
            "/api/auth/signin",
            json={
                "email": "flowtest@example.com",
                "password": "password123"
            }
        )
        assert signin_response.status_code == 200
        assert "access_token" in signin_response.json()

        # Step 3: Signout
        signout_response = client.post("/api/auth/signout")
        assert signout_response.status_code == 200


class TestJWTTokenValidation:
    """Tests for JWT token validation"""

    def test_protected_endpoint_without_token(self, client: TestClient):
        """Test accessing protected endpoint without token"""
        # Register a user first to get a valid user_id
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "protected@example.com",
                "password": "password123"
            }
        )
        user_id = signup_response.json()["id"]

        # Try to access protected endpoint without token
        response = client.get(f"/api/users/{user_id}/tasks")

        assert response.status_code == 401  # Unauthorized (no token provided)

    def test_protected_endpoint_with_invalid_token(self, client: TestClient):
        """Test accessing protected endpoint with invalid token"""
        # Register a user first
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "protected@example.com",
                "password": "password123"
            }
        )
        user_id = signup_response.json()["id"]

        # Try to access with invalid token
        response = client.get(
            f"/api/users/{user_id}/tasks",
            headers={"Authorization": "Bearer invalid_token_here"}
        )

        assert response.status_code == 401  # Unauthorized

    def test_protected_endpoint_with_valid_token(self, client: TestClient):
        """Test accessing protected endpoint with valid token"""
        # Register and login
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "protected@example.com",
                "password": "password123"
            }
        )
        user_id = signup_response.json()["id"]

        signin_response = client.post(
            "/api/auth/signin",
            json={
                "email": "protected@example.com",
                "password": "password123"
            }
        )
        token = signin_response.json()["access_token"]

        # Access protected endpoint with valid token
        response = client.get(
            f"/api/users/{user_id}/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200

    def test_token_contains_user_id(self, client: TestClient):
        """Test that token contains user ID in payload"""
        # Register and login
        signup_response = client.post(
            "/api/auth/signup",
            json={
                "email": "tokenid@example.com",
                "password": "password123"
            }
        )
        user_id = signup_response.json()["id"]

        signin_response = client.post(
            "/api/auth/signin",
            json={
                "email": "tokenid@example.com",
                "password": "password123"
            }
        )
        token = signin_response.json()["access_token"]

        # Decode token (without verification for testing)
        import base64
        import json

        # Get payload (second part of JWT)
        payload_encoded = token.split(".")[1]
        # Add padding if needed
        payload_encoded += "=" * (4 - len(payload_encoded) % 4)
        payload_decoded = base64.b64decode(payload_encoded)
        payload = json.loads(payload_decoded)

        assert "sub" in payload
        assert payload["sub"] == user_id

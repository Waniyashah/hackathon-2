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


@pytest.fixture(name="auth_user")
def auth_user_fixture(client: TestClient):
    """Create and authenticate a test user"""
    # Register user
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    user_id = signup_response.json()["id"]

    # Login to get token
    signin_response = client.post(
        "/api/auth/signin",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    token = signin_response.json()["access_token"]

    return {"user_id": user_id, "token": token}


@pytest.fixture(name="auth_user2")
def auth_user2_fixture(client: TestClient):
    """Create and authenticate a second test user"""
    # Register user
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "testuser2@example.com",
            "password": "password123"
        }
    )
    user_id = signup_response.json()["id"]

    # Login to get token
    signin_response = client.post(
        "/api/auth/signin",
        json={
            "email": "testuser2@example.com",
            "password": "password123"
        }
    )
    token = signin_response.json()["access_token"]

    return {"user_id": user_id, "token": token}


class TestTaskEndpoints:
    """Integration tests for task management endpoints"""

    def test_get_tasks_empty(self, client: TestClient, auth_user: dict):
        """Test getting tasks for user with no tasks"""
        response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_create_task_success(self, client: TestClient, auth_user: dict):
        """Test successfully creating a task"""
        response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={
                "title": "Test Task",
                "description": "Test Description"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["completed"] is False
        assert "id" in data
        assert data["user_id"] == auth_user["user_id"]

    def test_create_task_without_description(self, client: TestClient, auth_user: dict):
        """Test creating task without description"""
        response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={
                "title": "Test Task"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] is None

    def test_create_task_missing_title(self, client: TestClient, auth_user: dict):
        """Test creating task without required title"""
        response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={
                "description": "Test Description"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_create_task_without_auth(self, client: TestClient, auth_user: dict):
        """Test creating task without authentication"""
        response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            json={
                "title": "Test Task"
            }
        )

        assert response.status_code == 401  # Unauthorized (no token provided)

    def test_get_tasks_after_creation(self, client: TestClient, auth_user: dict):
        """Test getting tasks after creating some"""
        # Create tasks
        client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Task 1"}
        )
        client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Task 2"}
        )

        # Get tasks
        response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_specific_task(self, client: TestClient, auth_user: dict):
        """Test getting a specific task by ID"""
        # Create task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Test Task"}
        )
        task_id = create_response.json()["id"]

        # Get specific task
        response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"

    def test_get_nonexistent_task(self, client: TestClient, auth_user: dict):
        """Test getting a non-existent task"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks/{fake_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 404

    def test_update_task_success(self, client: TestClient, auth_user: dict):
        """Test successfully updating a task"""
        # Create task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Original Title", "description": "Original Description"}
        )
        task_id = create_response.json()["id"]

        # Update task
        response = client.put(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Updated Title", "description": "Updated Description"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated Description"

    def test_update_task_partial(self, client: TestClient, auth_user: dict):
        """Test partially updating a task"""
        # Create task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Original Title", "description": "Original Description"}
        )
        task_id = create_response.json()["id"]

        # Update only title
        response = client.put(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Updated Title"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Original Description"

    def test_toggle_task_completion(self, client: TestClient, auth_user: dict):
        """Test toggling task completion status"""
        # Create task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Test Task"}
        )
        task_id = create_response.json()["id"]

        # Toggle to completed
        response = client.patch(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

        # Toggle back to incomplete
        response = client.patch(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False

    def test_delete_task_success(self, client: TestClient, auth_user: dict):
        """Test successfully deleting a task"""
        # Create task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Test Task"}
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert get_response.status_code == 404

    def test_delete_nonexistent_task(self, client: TestClient, auth_user: dict):
        """Test deleting a non-existent task"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(
            f"/api/users/{auth_user['user_id']}/tasks/{fake_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        assert response.status_code == 404


class TestUserDataIsolation:
    """Tests for user data isolation"""

    def test_user_cannot_see_other_users_tasks(self, client: TestClient, auth_user: dict, auth_user2: dict):
        """Test that users can only see their own tasks"""
        # User 1 creates a task
        client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "User 1 Task"}
        )

        # User 2 creates a task
        client.post(
            f"/api/users/{auth_user2['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user2['token']}"},
            json={"title": "User 2 Task"}
        )

        # User 1 gets their tasks
        response1 = client.get(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )

        # User 2 gets their tasks
        response2 = client.get(
            f"/api/users/{auth_user2['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user2['token']}"}
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        tasks1 = response1.json()
        tasks2 = response2.json()

        assert len(tasks1) == 1
        assert len(tasks2) == 1
        assert tasks1[0]["title"] == "User 1 Task"
        assert tasks2[0]["title"] == "User 2 Task"

    def test_user_cannot_access_other_users_task(self, client: TestClient, auth_user: dict, auth_user2: dict):
        """Test that user cannot access another user's specific task"""
        # User 1 creates a task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "User 1 Task"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to access User 1's task
        response = client.get(
            f"/api/users/{auth_user2['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user2['token']}"}
        )

        assert response.status_code == 404

    def test_user_cannot_update_other_users_task(self, client: TestClient, auth_user: dict, auth_user2: dict):
        """Test that user cannot update another user's task"""
        # User 1 creates a task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "User 1 Task"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to update User 1's task
        response = client.put(
            f"/api/users/{auth_user2['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user2['token']}"},
            json={"title": "Hacked Title"}
        )

        assert response.status_code == 404

        # Verify task was not updated
        get_response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert get_response.json()["title"] == "User 1 Task"

    def test_user_cannot_delete_other_users_task(self, client: TestClient, auth_user: dict, auth_user2: dict):
        """Test that user cannot delete another user's task"""
        # User 1 creates a task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "User 1 Task"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to delete User 1's task
        response = client.delete(
            f"/api/users/{auth_user2['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user2['token']}"}
        )

        assert response.status_code == 404

        # Verify task still exists
        get_response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert get_response.status_code == 200

    def test_user_cannot_toggle_other_users_task(self, client: TestClient, auth_user: dict, auth_user2: dict):
        """Test that user cannot toggle another user's task completion"""
        # User 1 creates a task
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "User 1 Task"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to toggle User 1's task
        response = client.patch(
            f"/api/users/{auth_user2['user_id']}/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {auth_user2['token']}"}
        )

        assert response.status_code == 404


class TestCompleteTaskWorkflow:
    """Test complete task management workflow"""

    def test_complete_crud_workflow(self, client: TestClient, auth_user: dict):
        """Test complete CRUD workflow for tasks"""
        # Create
        create_response = client.post(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Workflow Task", "description": "Test workflow"}
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Read (list)
        list_response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        # Read (specific)
        get_response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert get_response.status_code == 200

        # Update
        update_response = client.put(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"},
            json={"title": "Updated Workflow Task"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Workflow Task"

        # Toggle completion
        toggle_response = client.patch(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert toggle_response.status_code == 200
        assert toggle_response.json()["completed"] is True

        # Delete
        delete_response = client.delete(
            f"/api/users/{auth_user['user_id']}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert delete_response.status_code == 204

        # Verify deletion
        final_list_response = client.get(
            f"/api/users/{auth_user['user_id']}/tasks",
            headers={"Authorization": f"Bearer {auth_user['token']}"}
        )
        assert len(final_list_response.json()) == 0

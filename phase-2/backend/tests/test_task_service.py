import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
import uuid
from datetime import datetime

from src.services.task_service import (
    create_task,
    get_user_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    toggle_task_completion
)
from src.services.auth_service import create_user
from src.models.user import User
from src.models.task import Task
from src.schemas.user import UserCreate
from src.schemas.task import TaskCreate, TaskUpdate


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


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Create a test user synchronously"""
    import asyncio
    user_data = UserCreate(email="testuser@example.com", password="password123")
    user = asyncio.run(create_user(user_data, session))
    return user


@pytest.fixture(name="test_user2")
def test_user2_fixture(session: Session):
    """Create a second test user synchronously"""
    import asyncio
    user_data = UserCreate(email="testuser2@example.com", password="password123")
    user = asyncio.run(create_user(user_data, session))
    return user


class TestCreateTask:
    """Test task creation"""

    @pytest.mark.asyncio
    async def test_create_task_success(self, session: Session, test_user: User):
        """Test successful task creation"""
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description"
        )
        task = await create_task(task_data, test_user.id, session)

        assert task is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.user_id == test_user.id
        assert task.completed is False
        assert task.id is not None
        assert task.created_at is not None
        assert task.updated_at is not None

    @pytest.mark.asyncio
    async def test_create_task_without_description(self, session: Session, test_user: User):
        """Test creating task without description"""
        task_data = TaskCreate(title="Test Task")
        task = await create_task(task_data, test_user.id, session)

        assert task is not None
        assert task.title == "Test Task"
        assert task.description is None

    @pytest.mark.asyncio
    async def test_create_task_default_completed_false(self, session: Session, test_user: User):
        """Test that new tasks default to completed=False"""
        task_data = TaskCreate(title="Test Task")
        task = await create_task(task_data, test_user.id, session)

        assert task.completed is False

    @pytest.mark.asyncio
    async def test_create_task_uuid_generated(self, session: Session, test_user: User):
        """Test that UUID is generated for new task"""
        task_data = TaskCreate(title="Test Task")
        task = await create_task(task_data, test_user.id, session)

        assert task.id is not None
        assert len(str(task.id)) == 36  # UUID string length with hyphens

    @pytest.mark.asyncio
    async def test_create_multiple_tasks_for_user(self, session: Session, test_user: User):
        """Test creating multiple tasks for the same user"""
        task1_data = TaskCreate(title="Task 1")
        task2_data = TaskCreate(title="Task 2")

        task1 = await create_task(task1_data, test_user.id, session)
        task2 = await create_task(task2_data, test_user.id, session)

        assert task1.id != task2.id
        assert task1.user_id == task2.user_id == test_user.id


class TestGetUserTasks:
    """Test retrieving user tasks"""

    @pytest.mark.asyncio
    async def test_get_user_tasks_empty(self, session: Session, test_user: User):
        """Test getting tasks for user with no tasks"""
        tasks = await get_user_tasks(test_user.id, session)
        assert tasks == []

    @pytest.mark.asyncio
    async def test_get_user_tasks_single_task(self, session: Session, test_user: User):
        """Test getting tasks for user with one task"""
        task_data = TaskCreate(title="Test Task")
        await create_task(task_data, test_user.id, session)

        tasks = await get_user_tasks(test_user.id, session)
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task"

    @pytest.mark.asyncio
    async def test_get_user_tasks_multiple_tasks(self, session: Session, test_user: User):
        """Test getting multiple tasks for user"""
        task1_data = TaskCreate(title="Task 1")
        task2_data = TaskCreate(title="Task 2")
        task3_data = TaskCreate(title="Task 3")

        await create_task(task1_data, test_user.id, session)
        await create_task(task2_data, test_user.id, session)
        await create_task(task3_data, test_user.id, session)

        tasks = await get_user_tasks(test_user.id, session)
        assert len(tasks) == 3

    @pytest.mark.asyncio
    async def test_get_user_tasks_isolation(self, session: Session, test_user: User, test_user2: User):
        """Test that users only see their own tasks"""
        task1_data = TaskCreate(title="User 1 Task")
        task2_data = TaskCreate(title="User 2 Task")

        await create_task(task1_data, test_user.id, session)
        await create_task(task2_data, test_user2.id, session)

        user1_tasks = await get_user_tasks(test_user.id, session)
        user2_tasks = await get_user_tasks(test_user2.id, session)

        assert len(user1_tasks) == 1
        assert len(user2_tasks) == 1
        assert user1_tasks[0].title == "User 1 Task"
        assert user2_tasks[0].title == "User 2 Task"


class TestGetTaskById:
    """Test retrieving specific task"""

    @pytest.mark.asyncio
    async def test_get_task_by_id_success(self, session: Session, test_user: User):
        """Test successfully getting task by ID"""
        task_data = TaskCreate(title="Test Task")
        created_task = await create_task(task_data, test_user.id, session)

        retrieved_task = await get_task_by_id(created_task.id, test_user.id, session)

        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == "Test Task"

    @pytest.mark.asyncio
    async def test_get_task_by_id_nonexistent(self, session: Session, test_user: User):
        """Test getting non-existent task"""
        fake_id = uuid.uuid4()
        task = await get_task_by_id(fake_id, test_user.id, session)
        assert task is None

    @pytest.mark.asyncio
    async def test_get_task_by_id_wrong_user(self, session: Session, test_user: User, test_user2: User):
        """Test that user cannot access another user's task"""
        task_data = TaskCreate(title="User 1 Task")
        created_task = await create_task(task_data, test_user.id, session)

        # Try to get task as different user
        retrieved_task = await get_task_by_id(created_task.id, test_user2.id, session)
        assert retrieved_task is None


class TestUpdateTask:
    """Test task updates"""

    @pytest.mark.asyncio
    async def test_update_task_title(self, session: Session, test_user: User):
        """Test updating task title"""
        task_data = TaskCreate(title="Original Title")
        created_task = await create_task(task_data, test_user.id, session)

        update_data = TaskUpdate(title="Updated Title")
        updated_task = await update_task(created_task.id, update_data, test_user.id, session)

        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.id == created_task.id

    @pytest.mark.asyncio
    async def test_update_task_description(self, session: Session, test_user: User):
        """Test updating task description"""
        task_data = TaskCreate(title="Test Task", description="Original Description")
        created_task = await create_task(task_data, test_user.id, session)

        update_data = TaskUpdate(description="Updated Description")
        updated_task = await update_task(created_task.id, update_data, test_user.id, session)

        assert updated_task.description == "Updated Description"
        assert updated_task.title == "Test Task"  # Title unchanged

    @pytest.mark.asyncio
    async def test_update_task_completed(self, session: Session, test_user: User):
        """Test updating task completion status"""
        task_data = TaskCreate(title="Test Task")
        created_task = await create_task(task_data, test_user.id, session)

        update_data = TaskUpdate(completed=True)
        updated_task = await update_task(created_task.id, update_data, test_user.id, session)

        assert updated_task.completed is True

    @pytest.mark.asyncio
    async def test_update_task_wrong_user(self, session: Session, test_user: User, test_user2: User):
        """Test that user cannot update another user's task"""
        task_data = TaskCreate(title="User 1 Task")
        created_task = await create_task(task_data, test_user.id, session)

        update_data = TaskUpdate(title="Hacked Title")
        updated_task = await update_task(created_task.id, update_data, test_user2.id, session)

        assert updated_task is None

    @pytest.mark.asyncio
    async def test_update_task_nonexistent(self, session: Session, test_user: User):
        """Test updating non-existent task"""
        fake_id = uuid.uuid4()
        update_data = TaskUpdate(title="Updated Title")
        updated_task = await update_task(fake_id, update_data, test_user.id, session)

        assert updated_task is None


class TestDeleteTask:
    """Test task deletion"""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, session: Session, test_user: User):
        """Test successfully deleting task"""
        task_data = TaskCreate(title="Test Task")
        created_task = await create_task(task_data, test_user.id, session)

        result = await delete_task(created_task.id, test_user.id, session)
        assert result is True

        # Verify task is deleted
        deleted_task = await get_task_by_id(created_task.id, test_user.id, session)
        assert deleted_task is None

    @pytest.mark.asyncio
    async def test_delete_task_wrong_user(self, session: Session, test_user: User, test_user2: User):
        """Test that user cannot delete another user's task"""
        task_data = TaskCreate(title="User 1 Task")
        created_task = await create_task(task_data, test_user.id, session)

        result = await delete_task(created_task.id, test_user2.id, session)
        assert result is False

        # Verify task still exists
        task = await get_task_by_id(created_task.id, test_user.id, session)
        assert task is not None

    @pytest.mark.asyncio
    async def test_delete_task_nonexistent(self, session: Session, test_user: User):
        """Test deleting non-existent task"""
        fake_id = uuid.uuid4()
        result = await delete_task(fake_id, test_user.id, session)
        assert result is False


class TestToggleTaskCompletion:
    """Test toggling task completion"""

    @pytest.mark.asyncio
    async def test_toggle_task_completion_false_to_true(self, session: Session, test_user: User):
        """Test toggling task from incomplete to complete"""
        task_data = TaskCreate(title="Test Task")
        created_task = await create_task(task_data, test_user.id, session)

        assert created_task.completed is False

        toggled_task = await toggle_task_completion(created_task.id, test_user.id, session)
        assert toggled_task.completed is True

    @pytest.mark.asyncio
    async def test_toggle_task_completion_true_to_false(self, session: Session, test_user: User):
        """Test toggling task from complete to incomplete"""
        task_data = TaskCreate(title="Test Task")
        created_task = await create_task(task_data, test_user.id, session)

        # First toggle to True
        await toggle_task_completion(created_task.id, test_user.id, session)

        # Then toggle back to False
        toggled_task = await toggle_task_completion(created_task.id, test_user.id, session)
        assert toggled_task.completed is False

    @pytest.mark.asyncio
    async def test_toggle_task_completion_wrong_user(self, session: Session, test_user: User, test_user2: User):
        """Test that user cannot toggle another user's task"""
        task_data = TaskCreate(title="User 1 Task")
        created_task = await create_task(task_data, test_user.id, session)

        toggled_task = await toggle_task_completion(created_task.id, test_user2.id, session)
        assert toggled_task is None

    @pytest.mark.asyncio
    async def test_toggle_task_completion_nonexistent(self, session: Session, test_user: User):
        """Test toggling non-existent task"""
        fake_id = uuid.uuid4()
        toggled_task = await toggle_task_completion(fake_id, test_user.id, session)
        assert toggled_task is None

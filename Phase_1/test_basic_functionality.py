"""
Basic functionality test for the Todo application.

This script tests the core functionality of the todo application
to ensure all features work as expected.
"""

import sys
import os

# Add src directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.task import Task
from models.task_list import TaskList
from services.task_service import TaskService


def test_task_creation():
    """Test basic task creation and properties."""
    print("Testing task creation...")

    task = Task(1, "Test task", "Test description")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed == False

    print("PASS: Task creation test passed")


def test_task_list_operations():
    """Test TaskList operations."""
    print("Testing TaskList operations...")

    task_list = TaskList()

    # Add a task
    task_id = task_list.add_task("Test task", "Test description")
    assert task_id == 1

    # Get the task
    task = task_list.get_task(task_id)
    assert task is not None
    assert task.title == "Test task"

    # List tasks
    tasks = task_list.list_tasks()
    assert len(tasks) == 1

    # Update task
    success = task_list.update_task(task_id, title="Updated task")
    assert success == True
    updated_task = task_list.get_task(task_id)
    assert updated_task.title == "Updated task"

    # Toggle completion
    success = task_list.toggle_task_completion(task_id)
    assert success == True
    toggled_task = task_list.get_task(task_id)
    assert toggled_task.completed == True

    # Toggle again
    success = task_list.toggle_task_completion(task_id)
    assert success == True
    toggled_task = task_list.get_task(task_id)
    assert toggled_task.completed == False

    # Delete task
    success = task_list.delete_task(task_id)
    assert success == True
    assert task_list.get_task(task_id) is None

    print("PASS: TaskList operations test passed")


def test_task_service():
    """Test TaskService operations."""
    print("Testing TaskService operations...")

    service = TaskService()

    # Add a task
    task_id = service.add_task("Service task", "Service description")
    assert task_id == 1

    # Get the task
    task_data = service.get_task(task_id)
    assert task_data is not None
    assert task_data['title'] == "Service task"

    # List tasks
    tasks = service.list_tasks()
    assert len(tasks) == 1

    # Update task
    success = service.update_task(task_id, title="Updated service task")
    assert success == True
    updated_task = service.get_task(task_id)
    assert updated_task['title'] == "Updated service task"

    # Toggle completion
    success = service.toggle_complete(task_id)
    assert success == True
    toggled_task = service.get_task(task_id)
    assert toggled_task['completed'] == True

    # Delete task
    success = service.delete_task(task_id)
    assert success == True
    assert service.get_task(task_id) is None

    print("PASS: TaskService operations test passed")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")

    # Test invalid inputs in Task constructor
    try:
        Task("invalid", "Valid title")
        assert False, "Should have raised ValueError for invalid ID type"
    except ValueError:
        pass  # Expected

    try:
        Task(1, "")
        assert False, "Should have raised ValueError for empty title"
    except ValueError:
        pass  # Expected

    try:
        Task(1, "Valid title", "Valid description", "invalid")
        assert False, "Should have raised ValueError for invalid completed type"
    except ValueError:
        pass  # Expected

    # Test service error handling
    service = TaskService()

    # Try to get non-existent task
    result = service.get_task(999)
    assert result is None

    # Try to update non-existent task
    success = service.update_task(999, title="New title")
    assert success == False

    # Try to delete non-existent task
    success = service.delete_task(999)
    assert success == False

    # Try to toggle non-existent task
    success = service.toggle_complete(999)
    assert success == False

    print("PASS: Edge cases test passed")


def run_tests():
    """Run all tests."""
    print("Running basic functionality tests...\n")

    test_task_creation()
    test_task_list_operations()
    test_task_service()
    test_edge_cases()

    print("\nSUCCESS: All tests passed! The Todo application is working correctly.")


if __name__ == "__main__":
    run_tests()
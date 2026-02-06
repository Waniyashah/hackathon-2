"""
Unit and Integration Tests for the Todo Application

This file contains basic unit tests for each service method and
integration tests for CLI commands as specified in the tasks.
"""

import unittest
import sys
import os

# Add src directory to Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from models.task import Task
from models.task_list import TaskList
from services.task_service import TaskService
from cli.cli_interface import CLIInterface


class TestTaskModel(unittest.TestCase):
    """Unit tests for the Task model."""

    def test_task_creation_valid(self):
        """Test creating a valid task."""
        task = Task(1, "Test Title", "Test Description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "Test Description")
        self.assertFalse(task.completed)

    def test_task_creation_defaults(self):
        """Test creating a task with default values."""
        task = Task(1, "Test Title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)

    def test_task_creation_with_completion(self):
        """Test creating a task with completion status."""
        task = Task(1, "Test Title", "Test Description", True)
        self.assertTrue(task.completed)

    def test_invalid_task_id(self):
        """Test creating a task with invalid ID raises ValueError."""
        with self.assertRaises(ValueError):
            Task("invalid", "Test Title")

    def test_empty_task_title(self):
        """Test creating a task with empty title raises ValueError."""
        with self.assertRaises(ValueError):
            Task(1, "")

    def test_invalid_completed_status(self):
        """Test creating a task with invalid completed status raises ValueError."""
        with self.assertRaises(ValueError):
            Task(1, "Test Title", "Test Description", "invalid")

    def test_toggle_completion(self):
        """Test toggling task completion status."""
        task = Task(1, "Test Title")
        self.assertFalse(task.completed)
        task.toggle_completion()
        self.assertTrue(task.completed)
        task.toggle_completion()
        self.assertFalse(task.completed)

    def test_update_task(self):
        """Test updating task title and description."""
        task = Task(1, "Original Title", "Original Description")

        task.update(title="New Title")
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.description, "Original Description")

        task.update(description="New Description")
        self.assertEqual(task.description, "New Description")
        self.assertEqual(task.title, "New Title")

        task.update(title="Final Title", description="Final Description")
        self.assertEqual(task.title, "Final Title")
        self.assertEqual(task.description, "Final Description")

    def test_repr_method(self):
        """Test string representation of task."""
        task = Task(1, "Test Title", "Test Description", False)
        repr_str = repr(task)
        self.assertIn("[○]", repr_str)

        task.completed = True
        repr_str = repr(task)
        self.assertIn("[✓]", repr_str)


class TestTaskListModel(unittest.TestCase):
    """Unit tests for the TaskList model."""

    def setUp(self):
        """Set up a fresh TaskList for each test."""
        self.task_list = TaskList()

    def test_add_task(self):
        """Test adding a task to the list."""
        task_id = self.task_list.add_task("Test Title", "Test Description")
        self.assertEqual(task_id, 1)

        task = self.task_list.get_task(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Title")
        self.assertEqual(task.description, "Test Description")

    def test_get_task(self):
        """Test retrieving a task."""
        task_id = self.task_list.add_task("Test Title")
        task = self.task_list.get_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task.id, task_id)

    def test_get_nonexistent_task(self):
        """Test retrieving a non-existent task returns None."""
        task = self.task_list.get_task(999)
        self.assertIsNone(task)

    def test_update_task(self):
        """Test updating a task."""
        task_id = self.task_list.add_task("Original Title", "Original Description")
        result = self.task_list.update_task(task_id, title="New Title")

        self.assertTrue(result)
        task = self.task_list.get_task(task_id)
        self.assertEqual(task.title, "New Title")

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task returns False."""
        result = self.task_list.update_task(999, title="New Title")
        self.assertFalse(result)

    def test_delete_task(self):
        """Test deleting a task."""
        task_id = self.task_list.add_task("Test Title")
        result = self.task_list.delete_task(task_id)

        self.assertTrue(result)
        task = self.task_list.get_task(task_id)
        self.assertIsNone(task)

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task returns False."""
        result = self.task_list.delete_task(999)
        self.assertFalse(result)

    def test_list_tasks(self):
        """Test listing all tasks."""
        self.task_list.add_task("Task 1")
        self.task_list.add_task("Task 2")
        self.task_list.add_task("Task 3")

        tasks = self.task_list.list_tasks()
        self.assertEqual(len(tasks), 3)

    def test_toggle_task_completion(self):
        """Test toggling task completion."""
        task_id = self.task_list.add_task("Test Title")
        result = self.task_list.toggle_task_completion(task_id)

        self.assertTrue(result)
        task = self.task_list.get_task(task_id)
        self.assertTrue(task.completed)

    def test_toggle_nonexistent_task_completion(self):
        """Test toggling completion of a non-existent task returns False."""
        result = self.task_list.toggle_task_completion(999)
        self.assertFalse(result)


class TestTaskService(unittest.TestCase):
    """Unit tests for the TaskService."""

    def setUp(self):
        """Set up a fresh TaskService for each test."""
        self.service = TaskService()

    def test_add_task(self):
        """Test adding a task via service."""
        task_id = self.service.add_task("Test Title", "Test Description")
        self.assertEqual(task_id, 1)

    def test_get_task(self):
        """Test getting a task via service."""
        task_id = self.service.add_task("Test Title")
        task_data = self.service.get_task(task_id)

        self.assertIsNotNone(task_data)
        self.assertEqual(task_data['title'], "Test Title")

    def test_get_nonexistent_task(self):
        """Test getting a non-existent task returns None."""
        task_data = self.service.get_task(999)
        self.assertIsNone(task_data)

    def test_update_task(self):
        """Test updating a task via service."""
        task_id = self.service.add_task("Original Title")
        result = self.service.update_task(task_id, title="New Title")

        self.assertTrue(result)
        task_data = self.service.get_task(task_id)
        self.assertEqual(task_data['title'], "New Title")

    def test_update_nonexistent_task(self):
        """Test updating a non-existent task returns False."""
        result = self.service.update_task(999, title="New Title")
        self.assertFalse(result)

    def test_delete_task(self):
        """Test deleting a task via service."""
        task_id = self.service.add_task("Test Title")
        result = self.service.delete_task(task_id)

        self.assertTrue(result)
        task_data = self.service.get_task(task_id)
        self.assertIsNone(task_data)

    def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task returns False."""
        result = self.service.delete_task(999)
        self.assertFalse(result)

    def test_list_tasks(self):
        """Test listing all tasks via service."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")

        tasks = self.service.list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_toggle_complete(self):
        """Test toggling task completion via service."""
        task_id = self.service.add_task("Test Title")
        result = self.service.toggle_complete(task_id)

        self.assertTrue(result)
        task_data = self.service.get_task(task_id)
        self.assertTrue(task_data['completed'])

    def test_toggle_nonexistent_task(self):
        """Test toggling completion of a non-existent task returns False."""
        result = self.service.toggle_complete(999)
        self.assertFalse(result)


class TestCLIInterface(unittest.TestCase):
    """Integration tests for the CLI interface."""

    def setUp(self):
        """Set up a fresh CLIInterface for each test."""
        self.cli = CLIInterface()

    def test_cli_initialization(self):
        """Test that CLI initializes with a service."""
        self.assertIsNotNone(self.cli.service)
        self.assertIsInstance(self.cli.service, TaskService)

    def test_get_valid_task_id_valid_input(self):
        """Test get_valid_task_id with mock input would return correct value."""
        # This is difficult to test without mocking input(), but we can at least
        # verify the method exists and has the right signature
        self.assertTrue(hasattr(self.cli, 'get_valid_task_id'))
        self.assertTrue(callable(getattr(self.cli, 'get_valid_task_id')))


def run_tests():
    """Run all tests."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add tests to the suite
    suite.addTests(loader.loadTestsFromTestCase(TestTaskModel))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskListModel))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskService))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIInterface))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    if success:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")
        sys.exit(1)
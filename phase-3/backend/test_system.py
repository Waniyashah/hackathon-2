"""
Test script for Todo AI Chatbot
Tests core functionality without running the full server.
"""

import asyncio
import sys
sys.path.insert(0, '.')

from src.db_context import init_db, get_db_session
from src.tools.task_tools import TaskTools
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.services.intent_service import IntentService

async def test_database_initialization():
    """Test database initialization."""
    print("\n=== Testing Database Initialization ===")
    try:
        await init_db()
        print("[PASS] Database initialized successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Database initialization failed: {e}")
        return False

async def test_task_tools():
    """Test MCP task tools."""
    print("\n=== Testing MCP Task Tools ===")
    tools = TaskTools()
    user_id = "test_user_123"

    try:
        # Test add_task
        print("\n1. Testing add_task...")
        result = await tools.add_task(user_id, "Buy groceries", "Get milk and bread")
        if result.get("success"):
            task_id = result["task"]["id"]
            print(f"[PASS] Task created: {result['task']['title']} (ID: {task_id})")
        else:
            print(f"[FAIL] Failed to create task: {result.get('error')}")
            return False

        # Test list_tasks
        print("\n2. Testing list_tasks...")
        result = await tools.list_tasks(user_id, "all")
        if result.get("success"):
            print(f"[PASS] Listed {result['count']} task(s)")
            for task in result["tasks"]:
                print(f"   - {task['title']} (completed: {task['completed']})")
        else:
            print(f"[FAIL] Failed to list tasks: {result.get('error')}")
            return False

        # Test complete_task
        print("\n3. Testing complete_task...")
        result = await tools.complete_task(user_id, task_id)
        if result.get("success"):
            print(f"[PASS] Task completed: {result['task']['title']}")
        else:
            print(f"[FAIL] Failed to complete task: {result.get('error')}")
            return False

        # Test update_task
        print("\n4. Testing update_task...")
        result = await tools.update_task(user_id, task_id, title="Buy groceries and snacks")
        if result.get("success"):
            print(f"[PASS] Task updated: {result['task']['title']}")
        else:
            print(f"[FAIL] Failed to update task: {result.get('error')}")
            return False

        # Test delete_task
        print("\n5. Testing delete_task...")
        result = await tools.delete_task(user_id, task_id)
        if result.get("success"):
            print(f"[PASS] Task deleted successfully")
        else:
            print(f"[FAIL] Failed to delete task: {result.get('error')}")
            return False

        print("\n[PASS] All task tool tests passed!")
        return True

    except Exception as e:
        print(f"\n[FAIL] Task tools test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_conversation_service():
    """Test conversation service."""
    print("\n=== Testing Conversation Service ===")
    service = ConversationService()
    user_id = "test_user_123"

    try:
        # Create conversation
        print("\n1. Testing create_conversation...")
        result = await service.create_conversation(user_id)
        if result.get("success"):
            conv_id = result["conversation"]["id"]
            print(f"[PASS] Conversation created (ID: {conv_id})")
        else:
            print(f"[FAIL] Failed to create conversation: {result.get('error')}")
            return False

        # Get conversation
        print("\n2. Testing get_conversation...")
        result = await service.get_conversation(conv_id, user_id)
        if result.get("success"):
            print(f"[PASS] Conversation retrieved successfully")
        else:
            print(f"[FAIL] Failed to get conversation: {result.get('error')}")
            return False

        print("\n[PASS] All conversation service tests passed!")
        return True

    except Exception as e:
        print(f"\n[FAIL] Conversation service test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_message_service():
    """Test message service."""
    print("\n=== Testing Message Service ===")
    conv_service = ConversationService()
    msg_service = MessageService()
    user_id = "test_user_123"

    try:
        # Create conversation first
        result = await conv_service.create_conversation(user_id)
        conv_id = result["conversation"]["id"]

        # Store user message
        print("\n1. Testing store_message (user)...")
        result = await msg_service.store_message(conv_id, user_id, "user", "Hello, chatbot!")
        if result.get("success"):
            print(f"[PASS] User message stored")
        else:
            print(f"[FAIL] Failed to store user message: {result.get('error')}")
            return False

        # Store assistant message
        print("\n2. Testing store_message (assistant)...")
        result = await msg_service.store_message(conv_id, user_id, "assistant", "Hello! How can I help?")
        if result.get("success"):
            print(f"[PASS] Assistant message stored")
        else:
            print(f"[FAIL] Failed to store assistant message: {result.get('error')}")
            return False

        # Get conversation history
        print("\n3. Testing get_conversation_history...")
        result = await conv_service.get_conversation_history(conv_id, user_id)
        if result.get("success"):
            print(f"[PASS] Retrieved {result['count']} message(s)")
            for msg in result["messages"]:
                print(f"   - {msg['role']}: {msg['content']}")
        else:
            print(f"[FAIL] Failed to get conversation history: {result.get('error')}")
            return False

        print("\n[PASS] All message service tests passed!")
        return True

    except Exception as e:
        print(f"\n[FAIL] Message service test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_intent_detection():
    """Test intent detection."""
    print("\n=== Testing Intent Detection ===")
    service = IntentService()

    test_cases = [
        ("Add a task to buy groceries", "add_task"),
        ("Show my tasks", "list_tasks"),
        ("Complete task 1", "complete_task"),
        ("Delete task 2", "delete_task"),
        ("Update task 3 to walk the dog", "update_task"),
    ]

    try:
        for message, expected_intent in test_cases:
            print(f"\nTesting: '{message}'")
            result = await service.detect_intent(message)
            detected_intent = result.get("intent")
            confidence = result.get("confidence", 0)

            if detected_intent == expected_intent:
                print(f"[PASS] Correct intent: {detected_intent} (confidence: {confidence:.2f})")
            else:
                print(f"[FAIL] Wrong intent: got {detected_intent}, expected {expected_intent}")

        print("\n[PASS] Intent detection tests completed!")
        return True

    except Exception as e:
        print(f"\n[FAIL] Intent detection test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("=" * 60)
    print("TODO AI CHATBOT - COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Database Initialization", await test_database_initialization()))
    results.append(("Task Tools", await test_task_tools()))
    results.append(("Conversation Service", await test_conversation_service()))
    results.append(("Message Service", await test_message_service()))
    results.append(("Intent Detection", await test_intent_detection()))

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "[PASS]" if result else "[FAIL]"
        print(f"{symbol} {test_name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n[SUCCESS] All tests passed! The system is working correctly.")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Please review the errors above.")

if __name__ == "__main__":
    asyncio.run(main())

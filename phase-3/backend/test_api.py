"""
API Endpoint Test Script
Tests the FastAPI chat endpoint with various scenarios.
"""

import requests
import json

BASE_URL = "http://localhost:8001"
USER_ID = "api_test_user"

def test_api():
    """Test the chat API endpoint."""
    print("=" * 60)
    print("TODO AI CHATBOT - API ENDPOINT TESTS")
    print("=" * 60)

    conversation_id = None

    # Test 1: Add first task
    print("\n1. Testing: Add a task to buy groceries")
    response = requests.post(
        f"{BASE_URL}/api/{USER_ID}/chat",
        json={"message": "Add a task to buy groceries"}
    )
    result = response.json()
    print(f"   Response: {result['response']}")
    print(f"   Tool executed: {result['tool_executed']}")
    print(f"   Intent: {result['intent']}")
    conversation_id = result['conversation_id']

    # Test 2: Add second task
    print("\n2. Testing: Add a task to call mom")
    response = requests.post(
        f"{BASE_URL}/api/{USER_ID}/chat",
        json={"message": "Add a task to call mom", "conversation_id": conversation_id}
    )
    result = response.json()
    print(f"   Response: {result['response']}")

    # Test 3: List tasks
    print("\n3. Testing: List my tasks")
    response = requests.post(
        f"{BASE_URL}/api/{USER_ID}/chat",
        json={"message": "List my tasks", "conversation_id": conversation_id}
    )
    result = response.json()
    print(f"   Response: {result['response']}")

    # Test 4: Add third task
    print("\n4. Testing: Add a task to finish report")
    response = requests.post(
        f"{BASE_URL}/api/{USER_ID}/chat",
        json={"message": "Add a task to finish report", "conversation_id": conversation_id}
    )
    result = response.json()
    print(f"   Response: {result['response']}")

    # Test 5: List all tasks
    print("\n5. Testing: Show my tasks")
    response = requests.post(
        f"{BASE_URL}/api/{USER_ID}/chat",
        json={"message": "Show my tasks", "conversation_id": conversation_id}
    )
    result = response.json()
    print(f"   Response: {result['response']}")

    # Test 6: Get conversation history
    print("\n6. Testing: Get conversation history")
    response = requests.get(
        f"{BASE_URL}/api/{USER_ID}/conversations/{conversation_id}/history"
    )
    result = response.json()
    print(f"   Messages: {result['count']}")
    for msg in result['messages'][-3:]:  # Show last 3 messages
        print(f"   - {msg['role']}: {msg['content'][:50]}...")

    # Test 7: Health check
    print("\n7. Testing: Health check endpoint")
    response = requests.get(f"{BASE_URL}/health")
    result = response.json()
    print(f"   Status: {result['status']}")
    print(f"   Service: {result['service']}")

    # Test 8: Root endpoint
    print("\n8. Testing: Root endpoint")
    response = requests.get(f"{BASE_URL}/")
    result = response.json()
    print(f"   Message: {result['message']}")
    print(f"   Version: {result['version']}")

    print("\n" + "=" * 60)
    print("API ENDPOINT TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_api()

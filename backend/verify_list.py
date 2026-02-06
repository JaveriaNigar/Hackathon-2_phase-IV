import requests
import uuid
import json

BASE_URL = "http://localhost:8000/api"

def verify_list_tasks():
    # 1. Signup
    email = f"test_list_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    name = "Test List User"
    
    resp = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password, "name": name})
    if resp.status_code not in [200, 201]:
        print("Signup failed")
        return
    token = resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_resp = requests.get(f"{BASE_URL}/user/", headers=headers)
    user_id = user_resp.json()["id"]

    # 2. Add a task
    requests.post(f"{BASE_URL}/{user_id}/chat", json={"message": "Add task CheckList", "conversation_id": None}, headers=headers)

    # 3. List tasks via Chat
    print("\nAsking Agent to list tasks...")
    # Using 'Show my tasks' to trigger list logic
    chat_resp = requests.post(f"{BASE_URL}/{user_id}/chat", json={"message": "Show my tasks", "conversation_id": None}, headers=headers)
    data = chat_resp.json()
    response_text = data["response"]
    
    print(f"Agent Response: {response_text}")
    
    if "CheckList" in response_text:
        print("SUCCESS: Task 'CheckList' found in agent response text.")
    else:
        print("FAILURE: Task 'CheckList' NOT found in agent response text.")

if __name__ == "__main__":
    verify_list_tasks()

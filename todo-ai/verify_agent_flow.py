import requests
import uuid
import json
import sys

BASE_URL = "http://localhost:8000/api"

def run_verification():
    # 1. Signup/Login to get User ID
    email = f"test_agent_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    name = "Test Agent User"
    
    print(f"1. Creating user {email}...")
    resp = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email,
        "password": password,
        "name": name
    })
    
    if resp.status_code not in [200, 201]:
        print(f"Signup failed: {resp.text}")
        return

    data = resp.json()
    token = data["token"]
    
    # Decoded token to get userId (or fetch from user profile)
    headers = {"Authorization": f"Bearer {token}"}
    user_resp = requests.get(f"{BASE_URL}/user/", headers=headers)
    user_id = user_resp.json()["id"]
    print(f"   User ID: {user_id}")

    # 2. Add Task via Chat
    print("\n2. Sending 'Add task Buy Milk' to Agent...")
    chat_payload = {
        "message": "Add task Buy Milk",
        "conversation_id": None
    }
    # Note: Chat endpoint requires user_id in path
    chat_resp = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_payload, headers=headers)
    
    if chat_resp.status_code != 200:
        print(f"Chat failed: {chat_resp.text}")
        return
        
    chat_data = chat_resp.json()
    print(f"   Agent Response: {chat_data['response']}")
    print(f"   Tool Calls: {chat_data['tool_calls']}")

    # 3. Verify Task in DB
    print("\n3. Verifying task existence via GET /tasks...")
    tasks_resp = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers)
    tasks = tasks_resp.json()
    
    found = False
    for t in tasks:
        if t['title'].lower() == "buy milk" or t['title'].lower() == "milk":
            found = True
            print(f"   SUCCESS: Found task '{t['title']}' with ID {t['id']}")
            break
    
    if not found:
        print("   FAILURE: Task not found in list!")
        print(f"   Tasks found: {[t['title'] for t in tasks]}")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"Error: {e}")

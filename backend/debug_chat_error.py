import requests
import uuid
import json

BASE_URL = "http://localhost:8000/api"

def run_verification():
    # 1. Signup/Login to get User ID
    email = f"test_debug_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    name = "Test Debug User"
    
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
    
    headers = {"Authorization": f"Bearer {token}"}
    user_resp = requests.get(f"{BASE_URL}/user/", headers=headers)
    user_id = user_resp.json()["id"]
    print(f"   User ID: {user_id}")

    # 2. Send Chat Message
    print("\n2. Sending 'Add task Buy Bread' to Agent...")
    chat_payload = {
        "message": "Add task Buy Bread",
        "conversation_id": None
    }
    
    try:
        chat_resp = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_payload, headers=headers)
        
        if chat_resp.status_code != 200:
            print(f"Chat failed with status {chat_resp.status_code}")
            print(f"Response Body: {chat_resp.text}")
        else:
            print("Chat successful!")
            print(f"Response: {chat_resp.json()}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    run_verification()

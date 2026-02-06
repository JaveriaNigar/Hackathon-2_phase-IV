import requests
import uuid
import time

BASE_URL = "http://localhost:8000/api"

def run_frontend_flow():
    # 1. Signup/Login
    email = f"test_frontend_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    name = "Frontend User"
    
    resp = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password, "name": name})
    if resp.status_code not in [200, 201]:
        print(f"Signup failed: {resp.text}")
        return
    token = resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = requests.get(f"{BASE_URL}/user/", headers=headers).json()["id"]

    # 2. Simulate sendMessage: POST /chat then GET /messages
    print("\nSimulating sendMessage flow...")
    
    # POST
    chat_payload = {"message": "Add task Buy Milk", "conversation_id": None}
    start_time = time.time()
    chat_resp = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_payload, headers=headers)
    print(f"POST /chat status: {chat_resp.status_code}")
    
    if chat_resp.status_code != 200:
        print(f"Chat Error: {chat_resp.text}")
        return

    data = chat_resp.json()
    conv_id = data["conversation_id"]
    print(f"Conversation ID: {conv_id}")

    # GET Messages immediately
    msg_url = f"{BASE_URL}/{user_id}/conversations/{conv_id}/messages"
    msg_resp = requests.get(msg_url, headers=headers)
    print(f"GET /messages status: {msg_resp.status_code}")
    
    if msg_resp.status_code == 200:
        msgs = msg_resp.json()
        print(f"Messages count: {len(msgs)}")
        last_msg = msgs[-1] if msgs else None
        print(f"Last message: {last_msg['content'] if last_msg else 'None'}")
        
    # Check tasks
    tasks = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers).json()
    print(f"Tasks found: {[t['title'] for t in tasks]}")

if __name__ == "__main__":
    run_frontend_flow()

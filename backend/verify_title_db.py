import requests
import uuid
import time
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def verify_title_saving():
    # 1. Signup
    email = f"title_test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    name = "Title Tester"
    
    resp = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password, "name": name})
    if resp.status_code not in [200, 201]:
        print("Signup failed")
        return
    token = resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = requests.get(f"{BASE_URL}/user/", headers=headers).json()["id"]

    # 2. Send Message
    msg = "I need to plan a wedding with 500 guests"
    print(f"\nSending message: '{msg}'")
    chat_resp = requests.post(f"{BASE_URL}/{user_id}/chat", json={"message": msg, "conversation_id": None}, headers=headers)
    
    if chat_resp.status_code != 200:
        print(f"Chat failed: {chat_resp.text}")
        return

    data = chat_resp.json()
    conv_id = data["conversation_id"]
    print(f"Conversation ID: {conv_id}")
    
    # 3. Check DB for Title (via API)
    # We need an endpoint to get conversations.
    # checking main.py or chat.py for GET /conversations
    print("Checking conversations list...")
    convs_resp = requests.get(f"{BASE_URL}/conversations?user_id={user_id}", headers=headers)
    
    if convs_resp.status_code != 200:
        # Try fallback path or different route structure?
        # chat.py has @router.get("/conversations")
        convs_resp = requests.get(f"{BASE_URL}/{user_id}/conversations", headers=headers)

    if convs_resp.status_code == 200:
        convs = convs_resp.json()
        my_conv = next((c for c in convs if c["id"] == conv_id), None)
        if my_conv:
            print(f"Found Conversation. Title: '{my_conv['title']}'")
            if my_conv['title'] and "Chat from" not in my_conv['title']:
                print("SUCCESS: Meaningful title generated.")
            else:
                print("FAILURE: Title is missing or default.")
        else:
            print("FAILURE: Conversation not found in list.")
    else:
        print(f"Error fetching conversations: {convs_resp.status_code}")

if __name__ == "__main__":
    verify_title_saving()

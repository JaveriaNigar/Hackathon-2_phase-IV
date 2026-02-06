import requests
import sqlite3
import json
import time

BASE_URL = "http://localhost:8000/api"
DB_PATH = "c:/Projects/hachathon-phase-3/backend/todo_app.db"

def test_backend():
    print("--- Starting Backend Verification ---")
    
    # 1. Signup
    signup_data = {
        "name": "Test User",
        "email": "test_verify@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 201:
            data = response.json()
            token = data["token"]
            user_id = data["user_id"]
            print(f"Signup successful. User ID: {user_id}")
        else:
            print(f"Signup failed: {response.status_code} - {response.text}")
            # Try login if user already exists
            login_data = {"email": "test_verify@example.com", "password": "password123"}
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            data = response.json()
            token = data["token"]
            user_id = data["user_id"]
            print(f"Login successful. User ID: {user_id}")
    except Exception as e:
        print(f"Error during auth: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Start Chat
    chat_data = {
        "message": "I want to plan a vacation to Japan for 10 days."
    }
    print("Sending chat message: 'I want to plan a vacation to Japan for 10 days.'")
    response = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_data, headers=headers)
    if response.status_code == 200:
        chat_res = response.json()
        conv_id = chat_res["conversation_id"]
        print(f"Chat response received. Conversation ID: {conv_id}")
        print(f"Assistant: {chat_res['response']}")
    else:
        print(f"Chat failed: {response.status_code} - {response.text}")
        return

    # 3. Check Database for Title
    print("Checking database for generated title...")
    time.sleep(1) # Give it a second to be sure
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, user_id FROM conversations WHERE id = ?", (conv_id,))
    row = cursor.fetchone()
    if row:
        title, db_user_id = row
        print(f"Generated Title in DB: '{title}'")
        if title and title != "New Chat" and len(title) > 0:
            print("SUCCESS: Automatic title generation verified.")
        else:
            print("FAILURE: Title not generated or is default.")
    else:
        print("FAILURE: Conversation not found in DB.")
    
    cursor.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY created_at", (conv_id,))
    messages = cursor.fetchall()
    print(f"Found {len(messages)} messages in DB for this conversation.")
    for role, content in messages:
        print(f" - {role}: {content[:50]}...")

    conn.close()
    print("--- Backend Verification Complete ---")

if __name__ == "__main__":
    test_backend()

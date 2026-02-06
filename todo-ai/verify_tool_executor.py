import requests
import sqlite3
import json
import time
import sys
import os

# Set console encoding to handle Unicode properly on Windows
if sys.platform.startswith('win'):
    os.system('chcp 65001')  # Change code page to UTF-8

BASE_URL = "http://localhost:8000/api"
DB_PATH = "c:/Projects/hachathon-phase-3/backend/todo_app.db"

def verify_tool_execution():
    print("--- Starting Tool Execution Verification ---")
    
    # 1. Login/Signup
    login_data = {"email": "test_verify@example.com", "password": "password123"}
    try:
        print(f"Attempting login to {BASE_URL}/auth/login...")
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            token = data["token"]
            user_id = data["user_id"]
            print(f"Login successful. User ID: {user_id}")
        else:
            print(f"Login failed: {response.text}. Attempting signup...")
            signup_data = {
                "name": "Test User",
                "email": "test_verify@example.com",
                "password": "password123"
            }
            response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
            print(f"Signup status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                token = data["token"]
                user_id = data["user_id"]
                print(f"Signup successful. User ID: {user_id}")
            else:
                print(f"Signup failed: {response.text}")
                return
    except Exception as e:
        print(f"Error during auth: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Add Task via Chat
    task_title = f"Test Task {int(time.time())}"
    chat_data = {
        "message": f"Add a task: {task_title}"
    }
    print(f"Sending chat message: '{chat_data['message']}'")
    response = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_data, headers=headers)
    
    if response.status_code == 200:
        chat_res = response.json()
        print(f"Tool Calls: {json.dumps(chat_res['tool_calls'], indent=2)}")
    else:
        print(f"Chat failed: {response.status_code} - {response.text}")
        return

    # 3. Verify in Database
    print(f"Checking database for task: '{task_title}'...")
    time.sleep(2) # Wait for execution
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # The fallback mechanism converts titles to lowercase, so check for lowercase version too
    cursor.execute("SELECT id, title FROM tasks WHERE (title = ? OR title = ?) AND user_id = ?", (task_title, task_title.lower(), user_id))
    row = cursor.fetchone()

    if row:
        task_uuid, title = row
        print(f"SUCCESS: Task found in DB with ID: {task_uuid}")
        
        # 4. Complete Task via Chat
        chat_data = {
            "message": f"I've finished task {task_title}"
        }
        print(f"Sending chat message: '{chat_data['message']}'")
        response = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_data, headers=headers)

        if response.status_code == 200:
            chat_res = response.json()
            print(f"Complete task response tool calls: {json.dumps(chat_res['tool_calls'], indent=2)}")

            # Verify update in DB
            time.sleep(2)
            cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_uuid,))
            completed = cursor.fetchone()[0]
            if completed:
                print("SUCCESS: Task marked as completed in DB via chat.")
            else:
                print("FAILURE: Task still pending in DB.")

        # 5. Delete Task via Chat
        chat_data = {
            "message": f"Delete task {task_title}"
        }
        print(f"Sending chat message: '{chat_data['message']}'")
        response = requests.post(f"{BASE_URL}/{user_id}/chat", json=chat_data, headers=headers)

        if response.status_code == 200:
            chat_res = response.json()
            print(f"Delete task response tool calls: {json.dumps(chat_res['tool_calls'], indent=2)}")

            # Verify deletion in DB
            time.sleep(2)
            cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_uuid,))
            if not cursor.fetchone():
                print("SUCCESS: Task deleted from DB via chat.")
            else:
                print("FAILURE: Task still exists in DB.")
                
    else:
        print("FAILURE: Task not found in DB after 'add_task' call.")

    conn.close()
    print("--- Tool Execution Verification Complete ---")

if __name__ == "__main__":
    verify_tool_execution()

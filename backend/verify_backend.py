import requests
import uuid
import json

BASE_URL = "http://127.0.0.1:8001"

def print_response(response):
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

print("\n1. Health Check:")
try:
    r = requests.get(f"{BASE_URL}/health")
    print_response(r)
except Exception as e:
    print(f"Failed to connect: {e}")
    exit()

# Create a test user first
print("\n2. Register Test User:")
USER_EMAIL = f"test_{uuid.uuid4()}@example.com"
USER_NAME = "Test User"
USER_PASSWORD = "password123"

signup_data = {
    "email": USER_EMAIL,
    "name": USER_NAME,
    "password": USER_PASSWORD
}

r = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
print_response(r)

if r.status_code != 201:
    print("Failed to create test user")
    exit()

response_data = r.json()
USER_ID = response_data.get("user_id")
TOKEN = response_data.get("token")

print(f"Created test user with ID: {USER_ID}")
print(f"Received token: {TOKEN[:10]}..." if TOKEN else "No token received")

# Set headers with the authentication token
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print(f"\n3. Create Task for User {USER_ID}:")
task_data = {
    "title": "Test Task 1",
    "description": "Description 1"
}
r = requests.post(f"{BASE_URL}/api/{USER_ID}/tasks", json=task_data, headers=headers)
print_response(r)

task_id = None
if r.status_code == 201:  # Expecting 201 Created
    try:
        task_response = r.json()
        task_id = task_response.get("id")
        print(f"Created task with ID: {task_id}")
    except:
        print("Could not parse task creation response")

print(f"\n4. List Tasks for User {USER_ID}:")
r = requests.get(f"{BASE_URL}/api/{USER_ID}/tasks", headers=headers)
print_response(r)

if task_id:
    print(f"\n5. Update Task {task_id}:")
    update_data = {
        "title": "Updated Test Task 1",
        "description": "Updated Description 1",
        "completed": True
    }
    r = requests.put(f"{BASE_URL}/api/{USER_ID}/tasks/{task_id}", json=update_data, headers=headers)
    print_response(r)

    print(f"\n6. Toggle Task Completion for Task {task_id}:")
    r = requests.patch(f"{BASE_URL}/api/{USER_ID}/tasks/{task_id}/complete", headers=headers)
    print_response(r)

    print(f"\n7. Get Pending Tasks Count:")
    r = requests.get(f"{BASE_URL}/api/{USER_ID}/pending-tasks", headers=headers)
    print_response(r)

    print(f"\n8. Get Completed Tasks Count:")
    r = requests.get(f"{BASE_URL}/api/{USER_ID}/completed-tasks", headers=headers)
    print_response(r)

    print(f"\n9. Delete Task {task_id}:")
    r = requests.delete(f"{BASE_URL}/api/{USER_ID}/tasks/{task_id}", headers=headers)
    print(f"Delete status code: {r.status_code}")
    if r.status_code == 204:
        print("Task deleted successfully")
    else:
        print_response(r)

print(f"\n10. Chat - Add Task (Regex) for User {USER_ID}:")
chat_payload = {"message": "Add a task called Buy Milk"}
r = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload, headers=headers)
print_response(r)

print(f"\n11. Chat - General Query (Gemini) for User {USER_ID}:")
chat_payload = {"message": "What is the meaning of life?"}
r = requests.post(f"{BASE_URL}/api/{USER_ID}/chat", json=chat_payload, headers=headers)
print_response(r)

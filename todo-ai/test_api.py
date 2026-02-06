import requests
import uuid

# Test the backend API
BASE_URL = "http://localhost:8001"

# Test health endpoint
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test with a random UUID to see if it gives a 404 vs 500
random_user_id = str(uuid.uuid4())
try:
    # This should return 404 if user doesn't exist, but not 500
    response = requests.get(f"{BASE_URL}/api/{random_user_id}/tasks")
    print(f"Random user tasks check: {response.status_code}")
    if response.status_code == 500:
        print("There's an internal server error!")
        print(response.text)
except Exception as e:
    print(f"Random user tasks check failed: {e}")
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from src.main import app
from src.database.session import get_session
from src.models.task import Task, TaskUpdate
from .test_utils import create_test_token

# Create a test database engine
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session

# Override the get_session dependency
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_task(client: TestClient, session: Session):
    """
    Test task creation with valid JWT and verify user_id association (T012).
    """
    user_id = "test_user_123"
    token = create_test_token(user_id)

    # Prepare task data
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

    # Make request with JWT token
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    # Verify response
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["user_id"] == user_id
    assert data["completed"] == task_data["completed"]

def test_get_user_tasks(client: TestClient, session: Session):
    """
    Test task listing with valid JWT and verify user isolation (T016).
    """
    user_id = "test_user_456"
    token = create_test_token(user_id)

    # Create a task for this user
    task_data = {
        "title": "Test Task for Listing",
        "description": "This task should appear in the list",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    # Get all tasks for the user
    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == task_data["title"]
    assert tasks[0]["user_id"] == user_id

def test_get_task(client: TestClient, session: Session):
    """
    Test retrieving a specific task.
    """
    user_id = "test_user_789"
    token = create_test_token(user_id)

    # Create a task first
    task_data = {
        "title": "Specific Task",
        "description": "This is a specific task to retrieve",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Retrieve the specific task
    response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == task_data["title"]
    assert retrieved_task["user_id"] == user_id

def test_update_task(client: TestClient, session: Session):
    """
    Test task updates with valid JWT and verify user isolation (T020).
    """
    user_id = "test_user_update"
    token = create_test_token(user_id)

    # Create a task first
    task_data = {
        "title": "Original Task Title",
        "description": "Original description",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Update the task
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["description"] == update_data["description"]
    assert updated_task["completed"] == update_data["completed"]
    assert updated_task["user_id"] == user_id

def test_delete_task(client: TestClient, session: Session):
    """
    Test task deletion with valid JWT and verify user isolation (T024).
    """
    user_id = "test_user_delete"
    token = create_test_token(user_id)

    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Verify task exists before deletion
    response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Delete the task
    response = client.delete(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify task no longer exists
    response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

def test_toggle_task_completion(client: TestClient, session: Session):
    """
    Test completion toggle with valid JWT and verify user isolation (T028).
    """
    user_id = "test_user_toggle"
    token = create_test_token(user_id)

    # Create a task first
    task_data = {
        "title": "Task to Toggle",
        "description": "This task completion status will be toggled",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]

    # Verify initial state
    response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    task = response.json()
    assert task["completed"] == False

    # Toggle completion status
    response = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["completed"] == True
    assert toggled_task["id"] == task_id
    assert toggled_task["user_id"] == user_id

    # Toggle again to verify it changes back
    response = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["completed"] == False

def test_user_isolation(client: TestClient, session: Session):
    """
    Test that users can only access their own tasks (user isolation).
    """
    user_id_1 = "test_user_isolation_1"
    user_id_2 = "test_user_isolation_2"
    token_1 = create_test_token(user_id_1)
    token_2 = create_test_token(user_id_2)

    # Create a task for user 1
    task_data = {
        "title": "User 1's Task",
        "description": "This task belongs to user 1",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id_1}/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token_1}"}
    )

    assert response.status_code == 201
    created_task = response.json()
    task_id = created_task["id"]
    assert created_task["user_id"] == user_id_1

    # User 2 should not be able to access user 1's task
    response = client.get(
        f"/api/{user_id_1}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_2}"}
    )

    # This should fail with 403 (Forbidden) due to user ID mismatch
    assert response.status_code == 403

    # User 2 should not be able to see user 1's tasks in their list
    response = client.get(
        f"/api/{user_id_2}/tasks",
        headers={"Authorization": f"Bearer {token_2}"}
    )

    assert response.status_code == 200
    user2_tasks = response.json()
    assert len(user2_tasks) == 0  # User 2 has no tasks yet

def test_invalid_jwt(client: TestClient):
    """
    Test that requests with invalid JWT tokens are rejected.
    """
    user_id = "test_user_invalid"

    # Try to create a task with an invalid token
    task_data = {
        "title": "Invalid Token Task",
        "description": "This should fail",
        "completed": False
    }

    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401

def test_task_not_found(client: TestClient, session: Session):
    """
    Test that requests for non-existent tasks return 404.
    """
    user_id = "test_user_not_found"
    token = create_test_token(user_id)

    # Try to get a non-existent task
    response = client.get(
        f"/api/{user_id}/tasks/99999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

    # Try to update a non-existent task
    update_data = {"title": "Updated Title"}
    response = client.put(
        f"/api/{user_id}/tasks/99999",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

    # Try to delete a non-existent task
    response = client.delete(
        f"/api/{user_id}/tasks/99999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

    # Try to toggle completion of a non-existent task
    response = client.patch(
        f"/api/{user_id}/tasks/99999/complete",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_get_pending_tasks_count(client: TestClient, session: Session):
    """
    Test getting the count of pending tasks for a user.
    """
    user_id = "test_user_pending"
    token = create_test_token(user_id)

    # Create some tasks - some completed, some not
    task_data_1 = {
        "title": "Completed Task",
        "description": "This task is completed",
        "completed": True
    }
    task_data_2 = {
        "title": "Pending Task 1",
        "description": "This task is pending",
        "completed": False
    }
    task_data_3 = {
        "title": "Pending Task 2",
        "description": "This task is also pending",
        "completed": False
    }

    # Create the completed task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_1,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Create the first pending task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_2,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Create the second pending task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_3,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Get the pending tasks count
    response = client.get(
        f"/api/{user_id}/pending-tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "pending" in data
    assert data["pending"] == 2  # Two pending tasks

def test_get_pending_tasks_count_empty(client: TestClient, session: Session):
    """
    Test getting the count of pending tasks for a user with no tasks.
    """
    user_id = "test_user_empty"
    token = create_test_token(user_id)

    # Get the pending tasks count when no tasks exist
    response = client.get(
        f"/api/{user_id}/pending-tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "pending" in data
    assert data["pending"] == 0  # No tasks means zero pending tasks

def test_get_pending_tasks_count_all_completed(client: TestClient, session: Session):
    """
    Test getting the count of pending tasks when all tasks are completed.
    """
    user_id = "test_user_all_completed"
    token = create_test_token(user_id)

    # Create completed tasks
    task_data_1 = {
        "title": "Completed Task 1",
        "description": "This task is completed",
        "completed": True
    }
    task_data_2 = {
        "title": "Completed Task 2",
        "description": "This task is also completed",
        "completed": True
    }

    # Create the first completed task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_1,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Create the second completed task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_2,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Get the pending tasks count
    response = client.get(
        f"/api/{user_id}/pending-tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "pending" in data
    assert data["pending"] == 0  # All tasks are completed

def test_get_completed_tasks_count(client: TestClient, session: Session):
    """
    Test getting the count of completed tasks for a user.
    """
    user_id = "test_user_completed"
    token = create_test_token(user_id)

    # Create some tasks - some completed, some not
    task_data_1 = {
        "title": "Completed Task",
        "description": "This task is completed",
        "completed": True
    }
    task_data_2 = {
        "title": "Pending Task 1",
        "description": "This task is pending",
        "completed": False
    }
    task_data_3 = {
        "title": "Completed Task 2",
        "description": "This task is also completed",
        "completed": True
    }

    # Create the first completed task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_1,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Create the pending task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_2,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Create the second completed task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_3,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Get the completed tasks count
    response = client.get(
        f"/api/{user_id}/completed-tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "completed" in data
    assert data["completed"] == 2  # Two completed tasks

def test_get_completed_tasks_count_empty(client: TestClient, session: Session):
    """
    Test getting the count of completed tasks for a user with no tasks.
    """
    user_id = "test_user_completed_empty"
    token = create_test_token(user_id)

    # Get the completed tasks count when no tasks exist
    response = client.get(
        f"/api/{user_id}/completed-tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "completed" in data
    assert data["completed"] == 0  # No tasks means zero completed tasks

def test_get_completed_tasks_count_all_pending(client: TestClient, session: Session):
    """
    Test getting the count of completed tasks when all tasks are pending.
    """
    user_id = "test_user_all_pending"
    token = create_test_token(user_id)

    # Create pending tasks
    task_data_1 = {
        "title": "Pending Task 1",
        "description": "This task is pending",
        "completed": False
    }
    task_data_2 = {
        "title": "Pending Task 2",
        "description": "This task is also pending",
        "completed": False
    }

    # Create the first pending task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_1,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Create the second pending task
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data_2,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

    # Get the completed tasks count
    response = client.get(
        f"/api/{user_id}/completed-tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "completed" in data
    assert data["completed"] == 0  # All tasks are pending
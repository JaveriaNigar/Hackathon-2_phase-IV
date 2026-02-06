import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from src.main import app
from src.database.session import get_session
from src.models.task import Task

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

def test_full_task_lifecycle(client: TestClient, session: Session):
    """
    Test the full lifecycle of a task: create, read, update, toggle completion, delete.
    This test simulates the user story flow for task management.
    """
    # Note: This test would normally require a valid JWT token in headers
    # For this integration test, we're focusing on the backend logic flow
    # In a real scenario, we would need to mock the authentication
    
    # Since we can't easily mock JWT authentication in this test setup,
    # we'll focus on testing the internal service functions directly
    from src.services.task_service import TaskService
    
    # Create a task
    user_id = "test_user_123"
    title = "Integration test task"
    description = "This is a task for integration testing"
    
    # Create task using the service directly
    created_task = TaskService.create_task(
        session=session,
        user_id=user_id,
        title=title,
        description=description
    )
    
    assert created_task.title == title
    assert created_task.description == description
    assert created_task.user_id == user_id
    assert created_task.completed is False
    
    # Get the task by ID
    retrieved_task = TaskService.get_task_by_id(
        session=session,
        task_id=created_task.id,
        user_id=user_id
    )
    
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    
    # Get all tasks for the user
    user_tasks = TaskService.get_user_tasks(
        session=session,
        user_id=user_id
    )
    
    assert len(user_tasks) == 1
    assert user_tasks[0].id == created_task.id
    
    # Update the task
    from src.models.task import TaskUpdate
    update_data = TaskUpdate(title="Updated task title", completed=True)
    
    updated_task = TaskService.update_task(
        session=session,
        task_id=created_task.id,
        user_id=user_id,
        task_update=update_data
    )
    
    assert updated_task.title == "Updated task title"
    assert updated_task.completed is True
    
    # Toggle completion status
    toggled_task = TaskService.toggle_completion(
        session=session,
        task_id=created_task.id,
        user_id=user_id
    )
    
    assert toggled_task.completed is False  # Was True, now False
    
    # Delete the task
    deletion_result = TaskService.delete_task(
        session=session,
        task_id=created_task.id,
        user_id=user_id
    )
    
    assert deletion_result is True
    
    # Verify the task is gone
    deleted_task = TaskService.get_task_by_id(
        session=session,
        task_id=created_task.id,
        user_id=user_id
    )
    
    assert deleted_task is None
import sys
import os
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.main import app
from src.models.task import Task
from sqlmodel import Session, select
from src.database.session import engine

import asyncio
from src.api.routes.chat import chat_endpoint, ChatRequest
from src.models.task import Task
from sqlmodel import Session, select
from src.database.session import engine
from unittest.mock import MagicMock, patch

async def test_tool_execution_logic():
    print("--- Testing Tool Executor Layer with Mocks (Direct Call) ---")
    
    # Simulate a response that includes an 'add_task' tool call
    mock_agent_result = {
        "response": "I've added the task 'Mocked Task' for you.",
        "tool_calls": [
            {
                "name": "add_task",
                "arguments": {
                    "title": "Mocked Task",
                    "description": "Controlled test description"
                }
            }
        ]
    }
    
    # Mock TodoAgent to avoid Gemini API calls
    with patch("src.api.routes.chat.TodoAgent") as MockAgent:
        mock_agent_instance = MockAgent.return_value
        mock_agent_instance.generate_conversation_title.return_value = "Test Title"
        mock_agent_instance.process_message.return_value = mock_agent_result
        
        # We need a session
        with Session(engine) as session:
            # Create a request object
            request = ChatRequest(message="add mock task")
            
            # Call the endpoint directly
            print("Calling chat_endpoint directly...")
            # Note: verify_user_access is a dependency, 
            # but since we're calling the function directly, we just pass the payload
            response = await chat_endpoint(
                user_id="test-mock-user",
                request=request,
                payload={"userId": "test-mock-user"},
                session=session
            )
            
            print(f"Assistant Response: {response.response}")
            print(f"Tool Calls in response: {len(response.tool_calls)}")
            
            # Verify database state
            print("Verifying database for 'Mocked Task'...")
            statement = select(Task).where(Task.title == "Mocked Task", Task.user_id == "test-mock-user")
            task = session.exec(statement).first()
            
            if task:
                print(f"SUCCESS: Task '{task.title}' found in database!")
                print(f"Description: {task.description}")
                
                # Clean up
                session.delete(task)
                session.commit()
                print("Cleaned up test task.")
            else:
                print("FAILURE: Task not found in database. Executor layer did not run as expected.")

if __name__ == "__main__":
    asyncio.run(test_tool_execution_logic())

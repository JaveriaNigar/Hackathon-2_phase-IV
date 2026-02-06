import os
import sys
from dotenv import load_dotenv

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.agents.todo_agent import TodoAgent

def test_agent():
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Testing agent with DB: {database_url}")
    
    agent = TodoAgent(database_url=database_url)
    
    # Test a simple greeting
    message = "hy"
    user_id = "test_user_id"
    
    print(f"\n--- Testing message: '{message}' ---")
    result = agent.process_message(user_id=user_id, message=message)
    
    print("\nResult:")
    print(result)
    
    if result.get("response") == "I'm sorry, I encountered an error while processing your message.":
        print("\nFAILURE: Agent returned error response.")
    else:
        print("\nSUCCESS: Agent returned a valid response.")

if __name__ == "__main__":
    # Load .env
    load_dotenv()
    test_agent()

import os
from dotenv import load_dotenv
from src.agents.todo_agent import TodoAgent

# Mock database URL since TodoAgent needs it but won't use it for title gen
DATABASE_URL = "sqlite:///./test.db"

def test_title_gen():
    agent = TodoAgent(database_url=DATABASE_URL)
    
    messages = [
        "Add a task to buy milk",
        "Show my tasks",
        "I want to plan a party",
        "Delete the task 5"
    ]
    
    print("\nTesting Title Generation:")
    for msg in messages:
        title = agent.generate_conversation_title(msg)
        print(f"Message: '{msg}' -> Title: '{title}'")

if __name__ == "__main__":
    try:
        test_title_gen()
    except Exception as e:
        print(f"Error: {e}")

import os
import sys
from src.agents.todo_agent import TodoAgent

# Mock DB
DATABASE_URL = "sqlite:///./test_debug.db"

def debug_agent():
    agent = TodoAgent(database_url=DATABASE_URL)
    user_id = "debug_user"
    msg = "I want to bake a cake"
    
    print(f"Sending: {msg}")
    result = agent.process_message(user_id, msg, conversation_id=None)
    
    print("\n--- RESULT ---")
    print(result)
    
    if result.get("chat_title"):
         print(f"SUCCESS: Got title '{result['chat_title']}'")
    else:
         print("FAILURE: No chat_title found.")

if __name__ == "__main__":
    debug_agent()

#!/usr/bin/env python3
"""
Test script to verify that complete_task operations work properly.
"""

import os
import sys

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import TodoAgent

def test_complete_task():
    """Test if the agent can properly complete a task."""
    print("Testing complete task functionality...")

    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")

    # Create the agent
    agent = TodoAgent(database_url=database_url)
    print(f"Selected model: {agent.model_name}")

    # First, let's list the tasks to see what we have
    print("\nListing tasks first...")
    result = agent.process_message(
        user_id="44bce376-6d8b-42ce-ad23-df3aee3cd012",
        message="Show my tasks",
        conversation_id="test_conversation"
    )
    
    print(f"Tool calls for list: {result['tool_calls']}")
    
    # Now try to complete a specific task
    print("\nTrying to complete a task...")
    result = agent.process_message(
        user_id="44bce376-6d8b-42ce-ad23-df3aee3cd012",
        message="Complete task test task 1769363372",
        conversation_id="test_conversation"
    )
    
    print(f"Tool calls for complete: {result['tool_calls']}")
    print(f"Response: {result['response']}")
    
    # Check if a complete_task tool call was generated
    complete_calls = [call for call in result['tool_calls'] if call['name'] == 'complete_task']
    if complete_calls:
        print(f"✓ Generated complete_task call: {complete_calls[0]}")
    else:
        print("✗ No complete_task call generated")

if __name__ == "__main__":
    test_complete_task()
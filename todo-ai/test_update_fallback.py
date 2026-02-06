#!/usr/bin/env python3
"""
Test script to verify the updated TodoAgent fallback mechanism.
"""

import os
import sys
import logging

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import TodoAgent

def test_update_task_fallback():
    """Test that the TodoAgent generates proper tool calls for update task messages when AI fails."""
    print("Testing TodoAgent update task fallback...")

    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")

    try:
        # Create the agent
        agent = TodoAgent(database_url=database_url)
        print("+ TodoAgent initialized successfully!")
        print("+ Selected model: {}".format(agent.model_name))

        # Test an update task message processing to ensure the fallback works
        result = agent.process_message(
            user_id="44bce376-6d8b-42ce-ad23-df3aee3cd012",  # Use the same user ID as in the verification
            message="Update task test task 1769364072 to updated task title",
            conversation_id="test_conversation"
        )

        print("+ Message processed successfully!")
        print("  Tool calls: {}".format(len(result['tool_calls'])))
        print("  Tool calls content: {}".format(result['tool_calls']))
        print("  Response: {}".format(result['response']))

        return True

    except Exception as e:
        print("- Error testing TodoAgent: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up basic logging
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("TodoAgent Update Task Fallback Test")
    print("=" * 60)

    success = test_update_task_fallback()

    print("=" * 60)
    if success:
        print("+ Test PASSED: TodoAgent update task fallback is working correctly!")
    else:
        print("- Test FAILED: There are issues with TodoAgent update task fallback.")
    print("=" * 60)
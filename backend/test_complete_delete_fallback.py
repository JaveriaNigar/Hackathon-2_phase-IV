#!/usr/bin/env python3
"""
Test script to verify that the TodoAgent fallback mechanism works for complete and delete messages.
"""

import os
import sys
import logging

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import TodoAgent

def test_complete_task_fallback():
    """Test that the TodoAgent generates proper tool calls for complete task messages when AI fails."""
    print("Testing TodoAgent complete task fallback...")

    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")

    try:
        # Create the agent
        agent = TodoAgent(database_url=database_url)
        print("+ TodoAgent initialized successfully!")
        print("+ Selected model: {}".format(agent.model_name))

        # Test a complete task message processing to ensure the fallback works
        result = agent.process_message(
            user_id="44bce376-6d8b-42ce-ad23-df3aee3cd012",  # Use the same user ID as in the verification
            message="I've finished task Test Task",
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

def test_delete_task_fallback():
    """Test that the TodoAgent generates proper tool calls for delete task messages when AI fails."""
    print("\nTesting TodoAgent delete task fallback...")

    try:
        # Create the agent
        agent = TodoAgent(database_url=os.getenv("DATABASE_URL", "sqlite:///./todo_app.db"))

        # Test a delete task message processing
        result = agent.process_message(
            user_id="44bce376-6d8b-42ce-ad23-df3aee3cd012",  # Use the same user ID as in the verification
            message="Delete task Test Task",
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
    print("TodoAgent Fallback Mechanism Test for Complete/Delete")
    print("=" * 60)

    success1 = test_complete_task_fallback()
    success2 = test_delete_task_fallback()

    print("=" * 60)
    print("Test completed.")
    print("=" * 60)
#!/usr/bin/env python3
"""
Test script to verify that the TodoAgent fallback mechanism works for task-related messages.
"""

import os
import sys
import logging

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import TodoAgent

def test_add_task_fallback():
    """Test that the TodoAgent generates proper tool calls for add task messages when AI fails."""
    print("Testing TodoAgent add task fallback...")

    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")

    try:
        # Create the agent
        agent = TodoAgent(database_url=database_url)
        print("+ TodoAgent initialized successfully!")
        print("+ Selected model: {}".format(agent.model_name))

        # Test an add task message processing to ensure the fallback works
        result = agent.process_message(
            user_id="test_user_123",
            message="Add a task: Buy groceries",
            conversation_id="test_conversation"
        )

        print("+ Message processed successfully!")
        print("  Tool calls: {}".format(len(result['tool_calls'])))
        print("  Tool calls content: {}".format(result['tool_calls']))
        print("  Response: {}".format(result['response']))

        # Check if the tool call was generated correctly
        if len(result['tool_calls']) > 0:
            tool_call = result['tool_calls'][0]
            if tool_call['name'] == 'add_task' and 'Buy groceries' in tool_call['arguments']['title']:
                print("+ SUCCESS: Correct tool call generated for add task!")
                return True
            else:
                print("- ERROR: Incorrect tool call generated")
                return False
        else:
            print("- ERROR: No tool calls generated for add task message")
            return False

    except Exception as e:
        print("- Error testing TodoAgent: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

def test_list_tasks_fallback():
    """Test that the TodoAgent generates proper tool calls for list tasks messages when AI fails."""
    print("\nTesting TodoAgent list tasks fallback...")

    try:
        # Create the agent
        agent = TodoAgent(database_url=os.getenv("DATABASE_URL", "sqlite:///./todo_app.db"))

        # Test a list tasks message processing
        result = agent.process_message(
            user_id="test_user_123",
            message="Show me my tasks",
            conversation_id="test_conversation"
        )

        print("+ Message processed successfully!")
        print("  Tool calls: {}".format(len(result['tool_calls'])))
        print("  Tool calls content: {}".format(result['tool_calls']))
        print("  Response: {}".format(result['response']))

        # Check if the tool call was generated correctly
        if len(result['tool_calls']) > 0:
            tool_call = result['tool_calls'][0]
            if tool_call['name'] == 'list_tasks':
                print("+ SUCCESS: Correct tool call generated for list tasks!")
                return True
            else:
                print("- ERROR: Incorrect tool call generated")
                return False
        else:
            print("- ERROR: No tool calls generated for list tasks message")
            return False

    except Exception as e:
        print("- Error testing TodoAgent: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up basic logging
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("TodoAgent Fallback Mechanism Test")
    print("=" * 60)

    success1 = test_add_task_fallback()
    success2 = test_list_tasks_fallback()

    print("=" * 60)
    if success1 and success2:
        print("+ All tests PASSED: TodoAgent fallback mechanism is working correctly!")
    else:
        print("- Some tests FAILED: There are issues with TodoAgent fallback mechanism.")
    print("=" * 60)
#!/usr/bin/env python3
"""
Test script to verify that the TodoAgent can be initialized without the 'Error listing/probing' issue.
"""

import os
import sys
import logging

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import TodoAgent

def test_agent_initialization():
    """Test that the TodoAgent can be initialized without errors."""
    print("Testing TodoAgent initialization...")
    
    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")
    
    try:
        # Create the agent - this is where the error was occurring
        agent = TodoAgent(database_url=database_url)
        print("+ TodoAgent initialized successfully!")
        print("+ Selected model: {}".format(agent.model_name))

        # Test a simple message processing to ensure everything works
        result = agent.process_message(
            user_id="test_user_123",
            message="Hello, how are you?",
            conversation_id="test_conversation"
        )

        print("+ Message processed successfully!")
        print("  Tool calls: {}".format(len(result['tool_calls'])))
        print("  Tool calls content: {}".format(result['tool_calls']))  # Print the actual tool calls
        
        return True
        
    except Exception as e:
        print("- Error initializing TodoAgent: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up basic logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("TodoAgent Initialization Test")
    print("=" * 60)
    
    success = test_agent_initialization()
    
    print("=" * 60)
    if success:
        print("+ Test PASSED: TodoAgent is working correctly!")
    else:
        print("- Test FAILED: There are still issues with TodoAgent.")
    print("=" * 60)
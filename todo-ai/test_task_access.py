#!/usr/bin/env python3
"""
Test script to check if the agent can properly access tasks in the database.
"""

import os
import sys
import sqlite3

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import TodoAgent
from src.tools.task_tools import TaskTools

def test_task_access():
    """Test if the agent and tools can access tasks in the database."""
    print("Testing task access...")

    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")

    # Create a TaskTools instance to check tasks directly
    task_tools = TaskTools(database_url)
    
    # Check if we can list tasks for our test user
    user_id = "44bce376-6d8b-42ce-ad23-df3aee3cd012"
    print(f"Checking tasks for user: {user_id}")
    
    try:
        tasks_result = task_tools.list_tasks(user_id)
        print(f"Tasks result: {tasks_result}")
        
        if tasks_result.get("success"):
            print(f"Found {len(tasks_result.get('tasks', []))} tasks")
            for task in tasks_result.get("tasks", []):
                print(f"  - ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
        else:
            print(f"Failed to get tasks: {tasks_result.get('message')}")
    except Exception as e:
        print(f"Error accessing tasks: {e}")
        import traceback
        traceback.print_exc()

def test_direct_database_access():
    """Test direct database access to verify tasks exist."""
    print("\nTesting direct database access...")
    
    # Use the same database URL to connect directly
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    # Extract the file path from the URL
    if database_url.startswith("sqlite:///"):
        db_path = database_url[10:]  # Remove "sqlite:///"
        print(f"Database path: {db_path}")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query for tasks with our test user ID
            user_id = "44bce376-6d8b-42ce-ad23-df3aee3cd012"
            cursor.execute("SELECT id, title, completed FROM tasks WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            
            print(f"Direct DB query found {len(rows)} tasks for user {user_id}:")
            for row in rows:
                print(f"  - ID: {row[0]}, Title: {row[1]}, Completed: {row[2]}")
                
            conn.close()
        except Exception as e:
            print(f"Error querying database directly: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_task_access()
    test_direct_database_access()
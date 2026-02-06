#!/usr/bin/env python3
"""
Test script to check the specific issue with TaskTools session.
"""

import os
import sys

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlmodel import create_engine, Session, select
from sqlalchemy.orm import sessionmaker
from src.models.task import Task

def test_session_creation():
    """Test if session creation and exec method work properly."""
    print("Testing session creation and exec method...")
    
    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    print(f"Using database URL: {database_url}")
    
    # Create engine and sessionmaker like TaskTools does
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create a session
    db = SessionLocal()
    print(f"Session type: {type(db)}")
    
    # Check if the session has exec method
    print(f"Has exec method: {hasattr(db, 'exec')}")
    print(f"Has execute method: {hasattr(db, 'execute')}")
    
    # Try to use the session to query tasks
    try:
        user_id = "44bce376-6d8b-42ce-ad23-df3aee3cd012"
        query = select(Task).where(Task.user_id == user_id)
        
        # Try both methods
        if hasattr(db, 'exec'):
            print("Using session.exec()...")
            result = db.exec(query)
            tasks = result.all()
            print(f"Found {len(tasks)} tasks using exec()")
        elif hasattr(db, 'execute'):
            print("Using session.execute()...")
            result = db.execute(query)
            tasks = result.scalars().all()
            print(f"Found {len(tasks)} tasks using execute()")
        else:
            print("Session has neither exec nor execute method!")
            
    except Exception as e:
        print(f"Error querying tasks: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_session_creation()
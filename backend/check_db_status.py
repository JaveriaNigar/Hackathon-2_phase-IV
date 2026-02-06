import sys
import os
from sqlmodel import Session, select, create_engine
from src.models.task import Task

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

def check_db():
    database_url = os.getenv("DATABASE_URL") or "sqlite:///backend/todo_app.db"
    # Try different paths for the db
    possible_paths = [
        "sqlite:///backend/todo_app.db",
        "sqlite:///todo_app.db",
        "sqlite:///backend/src/todo_app.db"
    ]
    
    for url in possible_paths:
        try:
            engine = create_engine(url)
            with Session(engine) as session:
                statement = select(Task).limit(20)
                tasks = session.exec(statement).all()
                if tasks:
                    print(f"\n--- Found tasks in {url} ---")
                    for t in tasks:
                        print(f"User: {t.user_id} | Title: {t.title} | Completed: {t.completed} | ID: {t.id}")
                    return
        except Exception as e:
            continue
    print("No tasks found or could not connect to database.")

if __name__ == "__main__":
    check_db()

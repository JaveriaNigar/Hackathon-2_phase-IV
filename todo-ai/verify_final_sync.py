import sys
import os
import io
import uuid

# Handle Windows emoji printing
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from src.agents.todo_agent import TodoAgent
    from src.services.task_service import TaskService
    from src.database.session import engine
    from sqlmodel import SQLModel, Session, select
    from src.models.task import Task
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def verify_final_sync():
    # Ensure tables exist
    SQLModel.metadata.create_all(engine)
    
    db_url = "sqlite:///todo_app.db"
    agent = TodoAgent(db_url)
    session = Session(engine)
    user_id = "final_sync_user_" + str(uuid.uuid4())[:8]
    
    print(f"\n--- Final Verification: Session Sync (User: {user_id}) ---\n")
    
    # 1. Create a task
    task_title = "Final Test"
    # We call it as the router would: service + manual commit
    task = TaskService.create_task(session, user_id, task_title)
    session.commit()
    session.refresh(task)
    print(f"Initial DB State: Task '{task.title}', Completed: {task.completed}")
    
    # 2. Simulate Chat Message
    msg = "mark task Final Test as done"
    print(f"Processing Message: '{msg}'")
    
    # Simulate chat.py logic
    result = agent.process_message(user_id, msg)
    tool_calls = result.get("tool_calls", [])
    
    if not tool_calls:
        print("[FAIL] No tool calls generated.")
        return

    print(f"Tool Call: {tool_calls[0]['name']}")

    # EXECUTE TOOLS (simulating chat_endpoint logic in chat.py)
    for call in tool_calls:
        if call['name'] == 'complete_task':
            args = call['arguments']
            identifier = args.get('task_id') or args.get('title')
            
            # Resolve
            resolved_task, status = TaskService.resolve_task(session, user_id, identifier)
            if status == "FOUND":
                print(f"Calling complete_task for {resolved_task.title}...")
                TaskService.complete_task(session, user_id, resolved_task.id)
                # CRITICAL: This is what we added to chat.py
                session.commit()
                print("Explicit commit performed.")
            else:
                print(f"[FAIL] Resolution failed: {status}")
                return

    # 3. Verify Database
    session.close() # Close and re-open to be 100% sure
    session = Session(engine)
    db_task = session.exec(select(Task).where(Task.user_id == user_id, Task.title == "Final Test")).first()
    
    print(f"Final DB State: Completed = {db_task.completed}")
    
    if db_task.completed == True:
        print("\n[SUCCESS] Synchronization confirmed. Database updated correctly!")
    else:
        print("\n[FAILED] Synchronization failed. Database was not updated.")

    session.close()

if __name__ == "__main__":
    verify_final_sync()

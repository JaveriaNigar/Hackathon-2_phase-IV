import sqlite3  
import os  
  
db_path = 'c:/Projects/hachathon-phase-3/backend/todo_app.db'  
  
if os.path.exists(db_path):  
    print(f"Database exists at: {db_path}")  
ECHO is on.
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()  
ECHO is on.
    # Get table info  
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
    tables = cursor.fetchall()  
    print("Tables in database:", tables)  
ECHO is on.
    if ('tasks',) in tables:  
        print("\\nTasks table structure:")  
        cursor.execute('PRAGMA table_info(tasks);')  
        rows = cursor.fetchall()  
        for row in rows:  
            print(row)  
ECHO is on.
        print("\\nSample tasks data:")  
        cursor.execute('SELECT * FROM tasks LIMIT 5;')  
        tasks = cursor.fetchall()  
        for task in tasks:  
            print(task)  
ECHO is on.
    conn.close()  
else:  

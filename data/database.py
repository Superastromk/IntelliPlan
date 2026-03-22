import sqlite3

def get_connection():
    return sqlite3.connect("planner.db")
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            due_date TEXT,
            created_at TEXT,
            priority TEXT,
            category TEXT,
            tags TEXT,
            estimated_minutes INTEGER,
            predicted_minutes INTEGER,
            actual_minutes INTEGER DEFAULT 0,
            difficulty INTEGER,
            status TEXT DEFAULT 'Not Started',
            subtasks TEXT   
    )
    """)

    conn.commit()
    conn.close()
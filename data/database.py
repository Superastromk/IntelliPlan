import sqlite3
import os

def get_connection():
    # Store db in project root, not in the same folder as main.py
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "planner.db")
    return sqlite3.connect(db_path)
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TEXT,
            category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            front TEXT,
            back TEXT,
            deck_name TEXT,
            last_reviewed TEXT,
            next_review TEXT,
            interval INTEGER DEFAULT 0,
            easiness REAL DEFAULT 2.5
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            start_time TEXT,
            end_time TEXT,
            date TEXT,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()
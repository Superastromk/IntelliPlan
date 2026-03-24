import json
from datetime import datetime

from data.database import get_connection
from data.models import Task, Note, Flashcard, Event


def create_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks(
            title, description, due_date, created_at, priority, category,
            tags, estimated_minutes, predicted_minutes, actual_minutes,
            difficulty, status, subtasks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        task.title,
        task.description,
        task.due_date,
        task.created_at,
        task.priority,
        task.category,
        json.dumps(task.tags),
        task.estimated_minutes,
        task.predicted_minutes,
        task.actual_minutes,
        task.difficulty,
        task.status,
        json.dumps(task.subtasks)
    ))

    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append(Task(
            id=row[0],
            title=row[1],
            description=row[2],
            due_date=row[3],
            created_at=row[4],
            priority=row[5],
            category=row[6],
            tags=json.loads(row[7]) if row[7] else [],
            estimated_minutes=row[8],
            predicted_minutes=row[9],
            actual_minutes=row[10],
            difficulty=row[11],
            status=row[12],
            subtasks=json.loads(row[13]) if row[13] else []
        ))
    return tasks



def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def update_task(task_id: int, task: Task):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks SET
            title = ?, description = ?, due_date = ?, priority = ?, category = ?,
            tags = ?, estimated_minutes = ?, predicted_minutes = ?, actual_minutes = ?,
            difficulty = ?, status = ?, subtasks = ?
        WHERE id = ?
    """, (
        task.title,
        task.description,
        task.due_date,
        task.priority,
        task.category,
        json.dumps(task.tags),
        task.estimated_minutes,
        task.predicted_minutes,
        task.actual_minutes,
        task.difficulty,
        task.status,
        json.dumps(task.subtasks),
        task_id
    ))

    conn.commit()
    conn.close()


def create_note(note: Note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notes(title, content, created_at, category)
        VALUES (?, ?, ?, ?)
    """, (note.title, note.content, note.created_at, note.category))
    conn.commit()
    conn.close()


def get_all_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [Note(*row) for row in rows]


def delete_note(note_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


def create_flashcard(card: Flashcard):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO flashcards(front, back, deck_name, last_reviewed, next_review, interval, easiness)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (card.front, card.back, card.deck_name, card.last_reviewed, card.next_review, card.interval, card.easiness))
    conn.commit()
    conn.close()


def get_flashcards_by_deck(deck_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards WHERE deck_name = ?", (deck_name,))
    rows = cursor.fetchall()
    conn.close()
    return [Flashcard(*row) for row in rows]


def get_all_decks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT deck_name FROM flashcards")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def delete_flashcard(card_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()


def create_event(event: Event):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events(title, description, start_time, end_time, date, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (event.title, event.description, event.start_time, event.end_time, event.date, event.category))
    conn.commit()
    conn.close()


def get_events_for_date(date_str: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE date = ?", (date_str,))
    rows = cursor.fetchall()
    conn.close()
    return [Event(*row) for row in rows]


def get_events_for_range(start_date: str, end_date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE date >= ? AND date <= ?", (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return [Event(*row) for row in rows]


def delete_event(event_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


def delete_events_by_category_and_date(category: str, date_str: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE category = ? AND date = ?", (category, date_str))
    conn.commit()
    conn.close()
import json
from datetime import datetime

from data.database import get_connection
from data.models import Task


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
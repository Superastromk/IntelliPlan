from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    due_date: str
    created_at: str
    priority: str
    category:str
    tags: List[str]
    estimated_minutes: int
    predicted_minutes: int
    actual_minutes: int
    difficulty: int
    status: str
    subtasks: List[str]

@dataclass
class Note:
    id: Optional[int]
    title: str
    content: str
    created_at: str
    category: str

@dataclass
class Flashcard:
    id: Optional[int]
    front: str
    back: str
    deck_name: str
    last_reviewed: Optional[str]
    next_review: Optional[str]
    interval: int = 0
    easiness: float = 2.5

@dataclass
class Event:
    id: Optional[int]
    title: str
    description: str
    start_time: str
    end_time: str
    date: str
    category: str
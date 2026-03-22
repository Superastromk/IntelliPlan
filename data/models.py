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
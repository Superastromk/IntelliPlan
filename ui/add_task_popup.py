from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QDateEdit, QFormLayout, QWidget, QListWidget
)
from PyQt5.QtCore import QDate, Qt
from datetime import datetime
from data.task_repository import create_task
from data.models import Task


class AddTaskPopup(QDialog):
    def __init__(self, task=None):
        super().__init__()
        self.task = task
        self.setWindowTitle("Edit Task" if task else "Add Task")
        self.setMinimumWidth(600)
        self.setStyleSheet("""
            QDialog {
                background-color: #1c1b1f;
                color: #e6e1e5;
            }
            QLabel {
                color: #d0bcff;
                font-weight: 800;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background-color: #252429;
                border: 2px solid transparent;
                border-radius: 20px;
                padding: 12px;
                color: #e6e1e5;
                font-size: 15px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #d0bcff;
                background-color: #1c1b1f;
            }
            QPushButton#SaveBtn {
                background-color: #d0bcff;
                color: #381e72;
                border-radius: 32px;
                padding: 24px;
                font-weight: 800;
                font-size: 17px;
                margin-top: 24px;
            }
            QPushButton#SaveBtn:hover {
                background-color: #e8def8;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(24)

        header = QLabel("Edit Task" if task else "New Task")
        header.setStyleSheet("font-size: 32px; font-weight: 800; color: #d1e1ff; margin-bottom: 8px; text-transform: none;")
        main_layout.addWidget(header)

        form_container = QWidget()
        form = QFormLayout(form_container)
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignLeft)

        # Title
        self.title_input = QLineEdit()
        if task: self.title_input.setText(task.title)
        form.addRow("Title", self.title_input)

        # Description
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        if task: self.desc_input.setPlainText(task.description or "")
        form.addRow("Description", self.desc_input)

        # Due date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if task:
            self.date_input.setDate(QDate.fromString(task.due_date, "yyyy-MM-dd"))
        else:
            self.date_input.setDate(QDate.currentDate())
        form.addRow("Due Date", self.date_input)

        # Priority
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        if task: self.priority_input.setCurrentText(task.priority)
        form.addRow("Priority", self.priority_input)

        # Category
        self.category_input = QComboBox()
        self.category_input.addItems([
            "General", "School", "Homework", "Project",
            "Exam", "Personal", "Chores", "Other"
        ])
        if task: self.category_input.setCurrentText(task.category)
        form.addRow("Category", self.category_input)

        # Tags
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Comma-separated (e.g., math, urgent)")
        if task: self.tags_input.setText(", ".join(task.tags))
        form.addRow("Tags", self.tags_input)

        # Estimated time
        self.estimate_input = QLineEdit()
        self.estimate_input.setPlaceholderText("Minutes (e.g., 45)")
        if task: self.estimate_input.setText(str(task.estimated_minutes))
        form.addRow("Est. Minutes", self.estimate_input)

        # Difficulty
        self.difficulty_input = QLineEdit()
        self.difficulty_input.setPlaceholderText("1–10")
        if task: self.difficulty_input.setText(str(task.difficulty))
        form.addRow("Difficulty", self.difficulty_input)

        # Subtasks
        self.subtasks_input = QTextEdit()
        self.subtasks_input.setMaximumHeight(100)
        self.subtasks_input.setPlaceholderText("One subtask per line")
        if task: self.subtasks_input.setPlainText("\n".join(task.subtasks))
        form.addRow("Subtasks", self.subtasks_input)

        main_layout.addWidget(form_container)

        # Save button
        save_btn = QPushButton("Update Task" if task else "Create Task")
        save_btn.setObjectName("SaveBtn")
        save_btn.clicked.connect(self.save_task)
        main_layout.addWidget(save_btn)

    def save_task(self):
        from data.task_repository import create_task, update_task
        title = self.title_input.text()
        desc = self.desc_input.toPlainText()
        due_date = self.date_input.date().toString("yyyy-MM-dd")
        priority = self.priority_input.currentText()
        category = self.category_input.currentText()

        tags = [t.strip() for t in self.tags_input.text().split(",") if t.strip()]
        try:
            estimated = int(self.estimate_input.text() or 0)
        except ValueError:
            estimated = 0
        
        try:
            difficulty = int(self.difficulty_input.text() or 0)
        except ValueError:
            difficulty = 0

        subtasks_raw = self.subtasks_input.toPlainText().split("\n")
        subtasks = [s.strip() for s in subtasks_raw if s.strip()]

        if self.task:
            # Update existing task
            updated_task = Task(
                id=self.task.id,
                title=title,
                description=desc,
                due_date=due_date,
                created_at=self.task.created_at,
                priority=priority,
                category=category,
                tags=tags,
                estimated_minutes=estimated,
                predicted_minutes=self.task.predicted_minutes,
                actual_minutes=self.task.actual_minutes,
                difficulty=difficulty,
                status=self.task.status,
                subtasks=subtasks
            )
            update_task(self.task.id, updated_task)
        else:
            # Create new task
            new_task = Task(
                id=None,
                title=title,
                description=desc,
                due_date=due_date,
                created_at=datetime.now().strftime("%Y-%m-%d"),
                priority=priority,
                category=category,
                tags=tags,
                estimated_minutes=estimated,
                predicted_minutes=0,
                actual_minutes=0,
                difficulty=difficulty,
                status="Not Started",
                subtasks=subtasks
            )
            create_task(new_task)
        
        self.accept()
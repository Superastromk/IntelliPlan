from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from data.task_repository import get_all_tasks


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Task list widget
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        # Add Task button
        self.btn_add = QPushButton("Add Task")
        layout.addWidget(self.btn_add)

        self.setLayout(layout)

        # Load tasks from database
        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()

        tasks = get_all_tasks()

        for task in tasks:
            item = QListWidgetItem(
                f"{task.title} | Due: {task.due_date} | Priority: {task.priority}"
            )
            item.setData(1000, task.id)
            self.task_list.addItem(item)
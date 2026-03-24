from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLineEdit,
    QLabel, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from data.task_repository import get_all_tasks
from ui.add_task_popup import AddTaskPopup

class TaskItemWidget(QFrame):
    def __init__(self, task):
        super().__init__()
        self.setObjectName("TaskCard")
        self.setStyleSheet("""
            QFrame#TaskCard {
                background-color: #252429;
                border: 2px solid transparent;
                border-radius: 28px;
                margin: 8px 16px;
                padding: 20px;
            }
            QFrame#TaskCard:hover {
                background-color: #2d2c33;
                border: 2px solid #d0bcff;
            }
            QLabel#TaskTitle {
                font-size: 20px;
                font-weight: 700;
                color: #e6e1e5;
            }
            QLabel#TaskMeta {
                font-size: 15px;
                color: #cac4d0;
            }
            QLabel#PriorityBadge {
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 800;
                text-transform: uppercase;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        
        info_layout = QVBoxLayout()
        self.title_label = QLabel(task.title)
        self.title_label.setObjectName("TaskTitle")
        
        meta_text = f"Due: {task.due_date}  •  {task.category}"
        self.meta_label = QLabel(meta_text)
        self.meta_label.setObjectName("TaskMeta")
        
        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.meta_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        self.priority_label = QLabel(task.priority)
        self.priority_label.setObjectName("PriorityBadge")
        
        # Color based on priority (Material 3 Dark tones)
        p = task.priority.lower()
        if p == 'high':
            self.priority_label.setStyleSheet("background-color: #8c1d18; color: #ffdad6;")
        elif p == 'medium':
            self.priority_label.setStyleSheet("background-color: #715500; color: #ffdf9e;")
        else:
            self.priority_label.setStyleSheet("background-color: #004a77; color: #c2e8ff;")
            
        layout.addWidget(self.priority_label)

class TaskManager(QWidget):
    def __init__(self, drawer):
        super().__init__()
        self.drawer = drawer
        self.setObjectName("TaskManager")
        self.setStyleSheet("""
            QWidget#TaskManager {
                background-color: transparent;
            }
            QPushButton#AddBtn {
                background-color: #d0bcff;
                color: #381e72;
                border-radius: 32px;
                font-weight: 800;
                font-size: 17px;
                padding: 24px;
                margin: 20px;
            }
            QPushButton#AddBtn:hover {
                background-color: #e8def8;
            }
            QListWidget {
                border: none;
                background: transparent;
            }
            QLabel#Header {
                font-size: 42px;
                font-weight: 900;
                color: #d0bcff;
                margin-bottom: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(12)

        header = QLabel("Tasks")
        header.setObjectName("Header")
        layout.addWidget(header)

        # Search bar (Inherits from main window QLineEdit style)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search your tasks...")
        self.search_input.textChanged.connect(self.load_tasks)
        layout.addWidget(self.search_input)

        self.task_list = QListWidget()
        self.task_list.setSpacing(8)
        layout.addWidget(self.task_list)

        self.btn_add = QPushButton("+ Add New Task")
        self.btn_add.setObjectName("AddBtn")
        layout.addWidget(self.btn_add)

        self.btn_add.clicked.connect(self.open_add_task_popup)
        self.task_list.itemClicked.connect(self.open_task_detail)

        self.all_tasks = []
        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        self.all_tasks = get_all_tasks()
        
        search_text = self.search_input.text().lower()

        for task in self.all_tasks:
            if search_text and search_text not in task.title.lower() and search_text not in task.description.lower():
                continue
            
            item = QListWidgetItem(self.task_list)
            custom_widget = TaskItemWidget(task)
            item.setSizeHint(custom_widget.sizeHint())
            item.setData(1000, task.id)
            
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, custom_widget)

    def open_add_task_popup(self):
        popup = AddTaskPopup()
        if popup.exec_():
            self.load_tasks()

    def open_task_detail(self, item):
        task_id = item.data(1000)
        task = next((t for t in self.all_tasks if t.id == task_id), None)

        if task and self.drawer:
            self.drawer.load_task(task)
            self.drawer.open()
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QProgressBar, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class TaskDetailDrawer(QWidget):
    def __init__(self, parent=None):
        # IMPORTANT: make this a top-level window, not a child widget
        super().__init__(None)

        # Make it behave like a floating drawer
        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setFixedWidth(450)
        self.setStyleSheet("""
            QWidget#DrawerRoot {
                background-color: #1c1b1f;
                border-left: 2px solid #252429;
            }
            QLabel#TitleLabel {
                font-size: 32px;
                font-weight: 900;
                color: #d0bcff;
            }
            QLabel#SectionTitle {
                font-weight: 800;
                font-size: 15px;
                color: #cac4d0;
                margin-top: 32px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            QLabel {
                color: #e6e1e5;
                font-size: 17px;
                font-weight: 500;
            }
            QProgressBar {
                border: none;
                background-color: #252429;
                border-radius: 12px;
                height: 20px;
                text-align: center;
                font-weight: 800;
                color: transparent;
            }
            QProgressBar::chunk {
                background-color: #d0bcff;
                border-radius: 12px;
            }
            QPushButton#EditBtn {
                background-color: #d0bcff;
                color: #381e72;
                border-radius: 28px;
                padding: 20px;
                font-weight: 800;
                font-size: 16px;
            }
            QPushButton#EditBtn:hover {
                background-color: #e8def8;
            }
            QPushButton#DeleteBtn {
                background-color: #8c1d18;
                color: #ffdad6;
                border-radius: 28px;
                padding: 20px;
                font-weight: 800;
                font-size: 16px;
            }
            QPushButton#DeleteBtn:hover {
                background-color: #b3261e;
            }
        """)
        self.setObjectName("DrawerRoot")
        
        # Add shadow to the drawer
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setXOffset(-15)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Header bar
        header = QWidget()
        header.setStyleSheet("background-color: #111318; padding: 20px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 24, 24, 24)

        self.title_label = QLabel("Task Title")
        self.title_label.setObjectName("TitleLabel")

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background: #2e3033;
                color: #c4c6cf;
                font-size: 18px;
                font-weight: 800;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #383a3d;
                color: #d1e1ff;
            }
        """)
        self.close_btn.clicked.connect(self.hide)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)

        root_layout.addWidget(header)

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")

        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 32)
        content_layout.setSpacing(16)

        # Description
        self.desc_label = QLabel("Description goes here...")
        self.desc_label.setWordWrap(True)
        content_layout.addWidget(self.desc_label)

        # Meta info
        self.category_label = QLabel("Category: None")
        self.tags_label = QLabel("Tags: None")
        self.difficulty_label = QLabel("Difficulty: -")
        self.time_label = QLabel("Estimated Time: - minutes")

        content_layout.addWidget(self.category_label)
        content_layout.addWidget(self.tags_label)
        content_layout.addWidget(self.difficulty_label)
        content_layout.addWidget(self.time_label)

        # Progress
        section_progress = QLabel("Progress")
        section_progress.setObjectName("SectionTitle")
        content_layout.addWidget(section_progress)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        content_layout.addWidget(self.progress)

        # Subtasks
        subtasks_title = QLabel("Subtasks")
        subtasks_title.setObjectName("SectionTitle")
        content_layout.addWidget(subtasks_title)

        self.subtasks_container = QWidget()
        self.subtasks_layout = QVBoxLayout(self.subtasks_container)
        self.subtasks_layout.setContentsMargins(0, 0, 0, 0)
        self.subtasks_layout.setSpacing(4)
        content_layout.addWidget(self.subtasks_container)

        content_layout.addStretch()

        scroll.setWidget(content)
        root_layout.addWidget(scroll)

        # Footer buttons
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(12, 8, 12, 12)

        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        footer_layout.addWidget(self.edit_btn)
        footer_layout.addWidget(self.delete_btn)

        root_layout.addWidget(footer)

        self.setLayout(root_layout)

        # Store reference to main window for positioning
        self._main_window = parent

    def open(self):
        """Position the drawer relative to the main window and show it."""
        if self._main_window is None:
            return

        geo = self._main_window.geometry()

        self.setGeometry(
            geo.x() + geo.width() - self.width(),
            geo.y(),
            self.width(),
            geo.height()
        )
        self.show()

    def load_task(self, task):
        """Fill drawer with task data (safe version)."""
        self.task = task
        self.title_label.setText(task.title)
        self.desc_label.setText(task.description or "")
        self.category_label.setText(f"Category: {task.category}")
        self.tags_label.setText(f"Tags: {task.tags}")
        self.difficulty_label.setText(f"Difficulty: {task.difficulty}")
        self.time_label.setText(f"Estimated Time: {task.estimated_minutes} minutes")

        # Clear old subtasks
        while self.subtasks_layout.count():
            item = self.subtasks_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        subtasks = task.subtasks or []

        # Add new subtasks as labels
        for sub in subtasks:
            label = QLabel(f"• {sub}")
            self.subtasks_layout.addWidget(label)

        # Update progress based on [x] markers
        if subtasks:
            completed = sum(1 for s in subtasks if s.startswith("[x]"))
            percent = int((completed / len(subtasks)) * 100)
            self.progress.setValue(percent)
        else:
            self.progress.setValue(0)

        # Re-connect buttons with fresh task reference
        try:
            self.edit_btn.clicked.disconnect()
            self.delete_btn.clicked.disconnect()
        except:
            pass

        self.edit_btn.clicked.connect(self.on_edit_clicked)
        self.delete_btn.clicked.connect(self.on_delete_clicked)

    def on_edit_clicked(self):
        from ui.add_task_popup import AddTaskPopup
        popup = AddTaskPopup(self.task)
        if popup.exec_():
            # Refresh TaskManager (if possible) or just this drawer
            self.load_task(self.task) 
            # We need to notify TaskManager to reload.
            # Usually we'd use a signal, but let's see if we can access parent.
            if hasattr(self._main_window, "page_tasks"):
                self._main_window.page_tasks.load_tasks()

    def on_delete_clicked(self):
        from PyQt5.QtWidgets import QMessageBox
        from data.task_repository import delete_task
        reply = QMessageBox.question(self, 'Delete Task', 
                                    f"Are you sure you want to delete '{self.task.title}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            delete_task(self.task.id)
            self.hide()
            if hasattr(self._main_window, "page_tasks"):
                self._main_window.page_tasks.load_tasks()
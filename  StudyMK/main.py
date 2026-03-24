import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QSize

from data.database import setup_database
setup_database()

from ui.task_manager import TaskManager
from ui.task_detail_drawer import TaskDetailDrawer
from ui.timer_page import TimerPage
from ui.notes_page import NotesPage
from ui.flashcards_page import FlashcardsPage
from ui.schedule_page import SchedulePage
from ui.homework_helper import HomeworkHelperPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StudyMK - Intelligent Planner")
        self.setGeometry(100, 100, 1200, 800)
        
        # SVG Doodle Background for a playful touch
        doodle_svg = """
        <svg width='400' height='400' xmlns='http://www.w3.org/2000/svg'>
            <path d='M 40 60 q 15 -15 30 0' stroke='#3e4759' stroke-width='1.5' fill='none' opacity='0.3'/>
            <circle cx='220' cy='120' r='2' fill='#4e586d' opacity='0.4'/>
            <path d='M 320 180 l 8 8 m -8 0 l 8 -8' stroke='#3e4759' stroke-width='1.5' fill='none' opacity='0.3'/>
            <rect x='110' y='320' width='12' height='12' rx='3' fill='none' stroke='#3e4759' stroke-width='1' opacity='0.2' transform='rotate(25 116 326)'/>
            <path d='M 360 360 c 12 -12, 24 12, 36 0' stroke='#3e4759' stroke-width='1.5' fill='none' opacity='0.3'/>
            <circle cx='60' cy='380' r='5' fill='none' stroke='#3e4759' stroke-width='1.2' opacity='0.2'/>
            <path d='M 270 270 m -6 0 a 6 6 0 1 0 12 0 a 6 6 0 1 0 -12 0' stroke='#3e4759' stroke-width='1.2' fill='none' opacity='0.3'/>
            <path d='M 150 50 l 10 0 m -5 -5 l 0 10' stroke='#3e4759' stroke-width='1' opacity='0.2'/>
        </svg>
        """.replace("\n", "").replace("  ", "")
        
        import base64
        doodle_b64 = base64.b64encode(doodle_svg.encode()).decode()

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #1c1b1f;
            }}
            QWidget#CentralWidget {{
                background-color: #1c1b1f;
                background-image: url(data:image/svg+xml;base64,{doodle_b64});
                background-repeat: repeat;
                background-position: center;
            }}
            QWidget {{
                color: #e6e1e5;
                font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
            }}
            QPushButton {{
                border-radius: 28px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
                background-color: #d0bcff;
                color: #381e72;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #e8def8;
            }}
            QPushButton:pressed {{
                background-color: #ccc2dc;
            }}
            QPushButton#SidebarButton {{
                text-align: left;
                background: transparent;
                border: none;
                color: #cac4d0;
                margin: 6px 16px;
                padding: 18px 24px;
                border-radius: 32px;
                font-size: 17px;
                font-weight: 500;
            }}
            QPushButton#SidebarButton:hover {{
                background-color: rgba(208, 188, 255, 0.12);
                color: #e6e1e5;
            }}
            QPushButton#SidebarButton:checked {{
                background-color: #4f378b;
                color: #eaddff;
                font-weight: 700;
            }}
            QFrame#SidebarFrame {{
                background-color: #1c1b1f;
                border-right: none;
            }}
            QStackedWidget {{
                background-color: transparent;
                margin: 24px;
            }}
            QLabel#AppTitle {{
                font-size: 36px;
                font-weight: 900;
                color: #d0bcff;
                margin-bottom: 40px;
                margin-left: 24px;
                letter-spacing: 2px;
                font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;
            }}
            QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox {{
                background-color: #252429;
                border: 2px solid transparent;
                border-radius: 24px;
                padding: 16px 20px;
                color: #e6e1e5;
                selection-background-color: #d0bcff;
                selection-color: #381e72;
            }}
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {{
                border: 2px solid #d0bcff;
                background-color: #1c1b1f;
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #49454f;
                min-height: 40px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #938f99;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Central widget required for QMainWindow
        central = QWidget()
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("SidebarFrame")
        sidebar_frame.setFixedWidth(280)
        sidebar = QVBoxLayout(sidebar_frame)
        sidebar.setContentsMargins(12, 32, 12, 32)
        sidebar.setSpacing(8)
        
        app_title = QLabel("StudyMK")
        app_title.setObjectName("AppTitle")
        sidebar.addWidget(app_title)

        self.btn_tasks = QPushButton("Tasks")
        self.btn_timer = QPushButton("Timer")
        self.btn_notes = QPushButton("Notes")
        self.btn_flashcards = QPushButton("Flashcards")
        self.btn_schedule = QPushButton("Schedule")
        self.btn_homework = QPushButton("Homework Helper")

        for btn in [self.btn_tasks, self.btn_timer, self.btn_notes, self.btn_flashcards, self.btn_schedule, self.btn_homework]:
            btn.setObjectName("SidebarButton")
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            sidebar.addWidget(btn)

        sidebar.addStretch()

        # Pages container
        self.pages = QStackedWidget()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.pages.setGraphicsEffect(shadow)

        # Drawer attached to MAIN WINDOW
        self.drawer = TaskDetailDrawer(self)
        self.drawer.hide()

        # Pages
        self.page_tasks = TaskManager(self.drawer)
        self.page_timer = TimerPage()
        self.page_notes = NotesPage()
        self.page_flashcards = FlashcardsPage()
        self.page_schedule = SchedulePage()
        self.page_homework = HomeworkHelperPage()

        self.pages.addWidget(self.page_tasks)
        self.pages.addWidget(self.page_timer)
        self.pages.addWidget(self.page_notes)
        self.pages.addWidget(self.page_flashcards)
        self.pages.addWidget(self.page_schedule)
        self.pages.addWidget(self.page_homework)

        # Sidebar button connections
        self.btn_tasks.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_timer.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_notes.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.btn_flashcards.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.btn_schedule.clicked.connect(lambda: self.pages.setCurrentIndex(4))
        self.btn_homework.clicked.connect(lambda: self.pages.setCurrentIndex(5))

        # Default selection
        self.btn_tasks.setChecked(True)

        # Add sidebar + pages to layout
        main_layout.addWidget(sidebar_frame)
        main_layout.addWidget(self.pages, 1)

    # Close drawer when clicking anywhere outside it
    def mousePressEvent(self, event):
        if self.drawer.isVisible():
            self.drawer.hide()

    # Keep drawer aligned during window resize (prevents crash)
    def resizeEvent(self, event):
        if self.drawer.isVisible():
            self.drawer.setGeometry(
                self.width() - self.drawer.width(),
                0,
                self.drawer.width(),
                self.height()
            )
        super().resizeEvent(event)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import(QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget)
from data.database import setup_database
setup_database()
from ui.task_manager import TaskManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Intelligent Planner")
        self.setGeometry(200,200,1000,600)

        main_layout = QVBoxLayout()
        sidebar = QVBoxLayout()
        btn_tasks = QPushButton("Tasks")
        btn_timer = QPushButton("Timer")
        btn_notes = QPushButton("Notes")
        btn_flashcards = QPushButton("Flashcards")
        btn_schedule = QPushButton("Schedule")

        sidebar.addWidget(btn_tasks)
        sidebar.addWidget(btn_timer)
        sidebar.addWidget(btn_notes)
        sidebar.addWidget(btn_flashcards)
        sidebar.addWidget(btn_schedule)
        sidebar.addStretch()

        #make the pages

        self.pages = QStackedWidget()
        self.page_tasks = TaskManager()
        self.page_timer = QLabel("Timer Page")
        self.page_notes = QLabel("Notes Page")
        self.page_flashcards = QLabel("Flashcards Page")
        self.page_schedule = QLabel("Schedule Page")

        #Add pages to stacks

        self.pages.addWidget(self.page_tasks)
        self.pages.addWidget(self.page_timer)
        self.pages.addWidget(self.page_notes)
        self.pages.addWidget(self.page_flashcards)
        self.pages.addWidget(self.page_schedule)

        #link buttons to pages
        btn_tasks.clicked.connect(lambda:self.pages.setCurrentIndex(0))
        btn_timer.clicked.connect(lambda:self.pages.setCurrentIndex(1))
        btn_notes.clicked.connect(lambda:self.pages.setCurrentIndex(2))
        btn_flashcards.clicked.connect(lambda:self.pages.setCurrentIndex(3))
        btn_schedule.clicked.connect(lambda:self.pages.setCurrentIndex(4))

        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.pages, 4)

        self.setLayout(main_layout)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
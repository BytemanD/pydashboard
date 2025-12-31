from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class Dashboard(QMainWindow):

    def __init__(self, *args, title: str = "Dashboard", **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)
        self.central = QWidget(self)

        self.central_layout = QGridLayout(self.central)

        # Application bar
        self.app_bar = QWidget()
        self.app_bar_layout = QGridLayout(self.app_bar)
        self.app_bar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # navigation widget
        self.navigation = QWidget()
        self.navigation_layout = QVBoxLayout(self.navigation)
        # self.navigation.setStyleSheet("border: 1px solid  #666;")

        # content widget
        self.content = QWidget()
        self.content_layout = QHBoxLayout(self.content)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setup_ui()

    def setup_ui(self):
        self.setup_navigation()
        self.setup_application_bar()
        self.setup_content()

        self.central_layout.addWidget(self.navigation, 0, 0, 12, 1)
        self.central_layout.addWidget(self.app_bar, 0, 1, 0, 11)
        self.central_layout.addWidget(self.content, 1, 1, 11, 11)

        self.setCentralWidget(self.central)

    def setup_navigation(self):
        self.navigation_layout.addWidget(QLabel("left widget"))

    def setup_application_bar(self):
        self.app_bar_layout.addWidget(QLabel("app bar"), 0, 0)

    def setup_content(self):
        self.content_layout.addWidget(QLabel("content"))

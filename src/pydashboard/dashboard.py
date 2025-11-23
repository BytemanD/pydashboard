from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout



class Dashboard(QMainWindow):

    def __init__(self, title:str='Dashboard', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)
        self.central = QWidget(self)

        self.central_layout = QGridLayout(self.central)

        # Application bar
        self.app_bar = QWidget()
        self.app_bar_layout = QGridLayout(self.app_bar)

        self.left = QWidget()
        self.left_layout = QHBoxLayout(self.left)

        self.content = QWidget()
        self.content_layout = QHBoxLayout(self.content)

        self._init_dashboard()

    def _init_dashboard(self):
        self.central_layout.addWidget(self.left, 0, 0)
        self.central_layout.addWidget(self.app_bar, 0, 1, 0, 11)
        self.central_layout.addWidget(self.content, 1, 1, 11, 11)

        self.app_bar_layout.addWidget(QLabel("app bar"))
        self.left_layout.addWidget(QLabel("left widget"))
        self.content_layout.addWidget(QLabel("content"))

        self.setCentralWidget(self.central)

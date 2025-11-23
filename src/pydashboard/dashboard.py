from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout



class Dashboard(QMainWindow):

    def __init__(self, title:str='Dashboard', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget(self)

        self.central_layout = QGridLayout(self)

        # Application bar
        self.app_bar = QWidget()
        self.app_bar_layout = QGridLayout(self.app_bar)
        self._init_dashboard()

    def _init_dashboard(self):
        self.setCentralWidget(self.central_widget)
        self.central_layout.addWidget(self.app_bar)

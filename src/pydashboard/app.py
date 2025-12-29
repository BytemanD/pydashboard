import sys
from typing import List, Mapping, Optional, Sequence, Tuple

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt


from pydashboard.components.button import MButton
from pydashboard.components.button_group import ButtonGroup
from pydashboard.components.icon import MIcon
from pydashboard.layout.cell import Cell
from pydashboard.models import DataTable, TableHeader

from pydashboard.theme import Theme
from pydashboard.style import Variant, Colors


class MainWindow(QMainWindow):

    def __init__(
        self,
        title: str = "",
        geometry: Tuple[int, int, int, int] = (100, 100, 800, 600),
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])

        central_widget = QWidget(self)
        self.central_layout = QGridLayout(central_widget)
        self.setCentralWidget(central_widget)

        for i in range(12):
            for j in range(12):
                self.central_layout.addWidget(QWidget(), i, j, 1, 1)

    def add_cell(self, cell: Cell, row: int, column: int=0, rowspan: int = 1, columnspan: int = 1):
        self.central_layout.addWidget(cell, row, column, rowspan, columnspan)

    def add_label(self, text: str, row: int, column: int=0, rowspan: int = 1, columnspan: int = 1):
        self.central_layout.addWidget(Cell([QLabel(text)]), row, column, rowspan, columnspan)


APP = QApplication(sys.argv)


def run(window: MainWindow, theme: Optional[Theme] = None):
    theme = theme or Theme()
    MIcon.COLORS = theme.colors

    APP.setStyleSheet(theme.style_sheet)
    window.show()
    sys.exit(APP.exec())

from typing import Sequence

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt


class Cell(QWidget):

    def __init__(self, items: Sequence[QWidget], vertical=False):
        """A widget that contains a list of widgets.

        :param items: 组件列表
        :param vertical: 是否使用垂直布局
        """
        super().__init__()
        self._layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.add_widgets(items)

    def add_widgets(self, items: Sequence[QWidget]):
        for item in items:
            self.add_widget(item)

    def add_widget(self, item: QWidget):
        self._layout.addWidget(item)

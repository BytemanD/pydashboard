from typing import List, Sequence

from PyQt6.QtWidgets import QWidget, QHBoxLayout,QPushButton


class ButtonGroup(QWidget):

    def __init__(self, items: Sequence[QPushButton]):
        """A button group that contains a list of buttons.

        :param items: 组件列表
        :param vertical: 是否使用垂直布局
        """
        super().__init__()
        self._layout = QHBoxLayout(self)
        # 移除所有间距
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.add_buttons(items)
        # self._layout.addStretch()

    def add_buttons(self, items: Sequence[QWidget]):
        for item in items:
            item.setStyleSheet("border:none;")
            item.setProperty("class", 'border-right: none')
            self.add_button(item)

    def add_button(self, item: QWidget):
        self._layout.addWidget(item)

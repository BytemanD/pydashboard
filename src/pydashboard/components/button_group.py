from typing import Optional, Sequence

from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class ButtonGroup(QWidget):

    def __init__(
        self,
        items: Sequence[QPushButton],
        color: str = "grey",
        border_radius: Optional[str] = None,
        variant: Optional[str] = None,
    ):
        """A button group that contains a list of buttons.

        :param items: 组件列表
        :param vertical: 是否使用垂直布局
        """
        super().__init__()
        self.color = color
        self.rounded = border_radius
        self.variant = variant
        self._layout = QHBoxLayout(self)
        # 移除所有间距
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.add_buttons(items)
        # self._layout.addStretch()

    def add_buttons(self, items: Sequence[QWidget]):
        for i, item in enumerate(items):
            item.setProperty("color", self.color)
            if self.variant:
                item.setProperty("variant", self.variant)
            if i == 0:
                item.setProperty("rounded-right", "0")
                if self.variant != "text":
                    item.setProperty("border-right-color", "grey")
                if self.rounded:
                    item.setProperty("rounded-left", self.rounded)
            elif i < len(items) - 1:
                item.setProperty("rounded", "0")
                if self.variant != "text":
                    item.setProperty("border-right-color", "grey")
            elif i == len(items) - 1:
                item.setProperty("rounded-left", "0")
                if self.rounded:
                    item.setProperty("rounded-right", self.rounded)
            self.add_button(item)

    def add_button(self, item: QWidget):
        self._layout.addWidget(item)

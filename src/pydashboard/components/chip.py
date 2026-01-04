from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
)
from qtawesome import icon as qta_icon

from pydashboard.components.button import MButton
from pydashboard.layout.frame import Container


class MChip(Container):

    def __init__(
        self,
        text: str,
        prepend_icon: Optional[str] = None,
        append_icon: Optional[str] = None,
        label: bool = False,
        closable: bool = False,
        **kwargs,
    ):
        super().__init__(border_radius="md" if label else "round", **kwargs)
        self.prepend_icon = prepend_icon
        self.append_icon = append_icon
        self.closable = closable

        if self.prepend_icon:
            self._prepend_label = QLabel()
            self._prepend_label.setFixedSize(18, 18)
            icon1 = qta_icon(self.prepend_icon, color="white")
            self._prepend_label.setPixmap(icon1.pixmap(18, 18))
            self._layout.addWidget(self._prepend_label)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self._layout.addWidget(self.label)

        if self.append_icon:
            self._append_label = QLabel()
            self._append_label.setFixedSize(18, 18)
            icon2 = qta_icon(self.append_icon, color="white")
            self._append_label.setPixmap(icon2.pixmap(18, 18))
            self._layout.addWidget(self._append_label)

        if closable:
            self._btn_close = MButton("X", color="grey", border_radius="xl")
            self._btn_close.setContentsMargins(0, 0, 0, 0)

            self._layout.addWidget(self._btn_close)

    def build(self):
        return []

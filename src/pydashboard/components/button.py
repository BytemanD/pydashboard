from typing import Any, Callable, Optional, Union

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton
from qtawesome import icon as qta_icon

from pydashboard.components.icon import MIcon
from pydashboard.layout.frame import Container
from pydashboard.theme import Variant


class MButton(Container):

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        icon: Optional[str] = None,
        tooltip: Optional[str] = None,
        **kwargs,
    ):
        self._btn = QPushButton(text)
        
        self._icon = icon

        super().__init__(**kwargs)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if on_click:
            self.clicked.connect(on_click)
        if tooltip:
            self.setToolTip(tooltip)

    def build(self):
        return [self._btn]

    def enterEvent(self, event: Optional[QEnterEvent]) -> None:
        super().enterEvent(event)
        if event and event.type() == QEvent.Type.Enter and self._icon:
            if self._variant in [Variant.OUTLINED.value, Variant.TEXT.value]:
                self._btn.setIcon(qta_icon(self._icon, color="white"))
            return

    def leaveEvent(self, a0: QEvent | None) -> None:
        super().leaveEvent(a0)
        if a0 and a0.type() == QEvent.Type.Leave and self._icon:
            if self._variant in [Variant.OUTLINED, Variant.TEXT]:
                self._btn.setIcon(qta_icon(self._icon, color=self._color))
            return

    def _update_stylesheet(self):
        super()._update_stylesheet()
        self._update_icon()

    def _update_icon(self):
        if not self._icon:
            return
        if self._variant in [Variant.OUTLINED, Variant.TEXT, Variant.PLAIN]:
            self._btn.setIcon(qta_icon(self._icon, color=self.theme.get_hover_color(self._color)))
            # Icon(self._icon, color=self._color))
        else:
            self._btn.setIcon(qta_icon(self._icon, color="white"))

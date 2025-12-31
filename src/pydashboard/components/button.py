from typing import Any, Callable, Optional, Union

from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton

from pydashboard.components.icon import MIcon
from pydashboard.theme import Variant


class MButton(QPushButton):

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        variant: Union[Variant, str] = Variant.FLAT,
        color: str = "primary",
        icon: Optional[str] = None,
        rounded: Optional[str] = None,
        tooltip: Optional[str] = None,
    ):
        super().__init__(text)
        self._icon = icon
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty(
            "variant", variant.value if isinstance(variant, Variant) else variant
        )
        self.setProperty("color", color)

        if rounded:
            self.setProperty("rounded", rounded)

        if on_click:
            self.clicked.connect(on_click)
        if tooltip:
            self.setToolTip(tooltip)

    @property
    def variant(self):
        return self.property("variant")

    @property
    def color(self):
        return self.property("color")

    def enterEvent(self, event: Optional[QEnterEvent]) -> None:
        """事件过滤器"""
        super().enterEvent(event)
        if event and event.type() == QEvent.Type.Enter and self._icon:
            if self.variant in [Variant.OUTLINED.value, Variant.TEXT.value]:
                self.setIcon(MIcon.get(self._icon, color="white"))
            return

    def leaveEvent(self, a0: QEvent | None) -> None:
        super().leaveEvent(a0)
        if a0 and a0.type() == QEvent.Type.Leave and self._icon:
            if self.variant in [Variant.OUTLINED, Variant.TEXT]:
                self.setIcon(MIcon.get(self._icon, color=self.color))
            return

    def setProperty(self, name: str | None, value: Any) -> bool:
        result = super().setProperty(name, value)
        if name == "variant" or name == "color":
            self._update_icon()

        if name == "variant" and self.variant in [Variant.ELEVATED.value]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)  # 偏移
            shadow.setBlurRadius(20)  # 阴影半径
            shadow.setColor(Qt.GlobalColor.darkGray)  # 阴影颜色
            self.setGraphicsEffect(shadow)
        return result

    def _update_icon(self):
        if not self._icon:
            return
        if self.variant in [
            Variant.OUTLINED.value,
            Variant.TEXT.value,
            Variant.PLAIN.value,
        ]:
            self.setIcon(MIcon.get(self._icon, color=self.color))
        else:
            self.setIcon(MIcon.get(self._icon, color="white"))

    def disable(self):
        self.setDisabled(True)
        return self

    def enable(self):
        self.setDisabled(False)
        return self

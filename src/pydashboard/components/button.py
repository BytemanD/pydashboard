from typing import Callable, Optional, Union

from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QApplication, QStyle
from PyQt6.QtCore import QObject, Qt, QEvent, QTimer
from PyQt6.QtGui import QEnterEvent, QPaintEvent, QPalette, QColor
from loguru import logger

from pydashboard.components.icon import MIcon
from pydashboard.theme import Variant


class MButton(QPushButton):

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        variant: Union[Variant, str] = Variant.FLAT,
        color: Optional[str] = "primary",
        icon: Optional[str] = None,
    ):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon = icon
        self._color = color
        self._variant = variant

        if on_click:
            self.clicked.connect(on_click)

        if self._icon:
            if self._variant in (Variant.FLAT, Variant.ELEVATED):
                self.setIcon(MIcon.get(self._icon, color='white'))
            else:
                self.setIcon(MIcon.get(self._icon, color=color))

        self.setProperty(
            "variant", variant.value if isinstance(variant, Variant) else variant
        )
        self.setProperty("color", color)

        if variant == Variant.ELEVATED.value or variant == Variant.ELEVATED:
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)  # 偏移
            shadow.setBlurRadius(20)  # 阴影半径
            shadow.setColor(Qt.GlobalColor.darkGray)  # 阴影颜色
            self.setGraphicsEffect(shadow)

    def enterEvent(self, event: Optional[QEnterEvent]) -> None:
        """事件过滤器"""
        super().enterEvent(event)
        if event and event.type() == QEvent.Type.Enter and self._icon:
            if self._variant in [Variant.OUTLINED, Variant.TEXT]:
                self.setIcon(MIcon.get(self._icon, color="white"))
            return

    def leaveEvent(self, a0: QEvent | None) -> None:
        super().leaveEvent(a0)
        if a0 and a0.type() == QEvent.Type.Leave and self._icon:
            if self._variant in [Variant.OUTLINED, Variant.TEXT]:
                self.setIcon(MIcon.get(self._icon, color=self._color))
            return

    def setStyle(self, a0: QStyle | None) -> None:
        logger.info("setStyle {}", a0)
        return super().setStyle(a0)

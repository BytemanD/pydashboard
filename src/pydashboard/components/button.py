from typing import Callable, Optional, Union

from PyQt6.QtWidgets import QPushButton, QStyle, QGraphicsDropShadowEffect, QSizePolicy
from PyQt6.QtCore import Qt

from pydashboard.theme import Variant


class MButton(QPushButton):

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable[[], None]] = None,
        variant: Union[Variant, str] = Variant.FLAT,
        color: Optional[str] = None,
    ):
        super().__init__(text)
        if on_click:
            self.clicked.connect(on_click)
        self.setProperty(
            "variant", variant.value if isinstance(variant, Variant) else variant
        )
        if color:
            self.setProperty("color", color)

        if variant == Variant.ELEVATED.value or variant == Variant.ELEVATED:
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)  # 偏移
            shadow.setBlurRadius(16)  # 阴影半径
            shadow.setColor(Qt.GlobalColor.gray)  # 阴影颜色
            self.setGraphicsEffect(shadow)

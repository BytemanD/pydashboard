from typing import Any, Callable, Optional, Sequence, Union

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from pydashboard.style.size import Size
from pydashboard.style.variant import Variant
from pydashboard.theme import Theme


class Container(QFrame):
    update_style = pyqtSignal()

    def __init__(
        self,
        variant: Optional[str] = None,
        color: Optional[str] = None,
        border_radius: Optional[str] = None,
        vertical: bool = False,
        size: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = Theme()
        self._variant = variant or Variant.FLAT.value
        self._color = color or "primary"
        self._size = size
        self.border_radius = border_radius or "md"

        self._layout = QVBoxLayout(self) if vertical else QHBoxLayout(self)
        self._layout.setContentsMargins(8, 1, 8, 2)
        # self.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.update_style.connect(self._update_stylesheet)
        self.setMouseTracking(True)
        for widget in self.build():
            if not widget:
                continue
            self._layout.addWidget(widget)

    def build(self) -> Sequence[QWidget]:
        return []

    def showEvent(self, a0):
        self.setMinimumHeight(26)
        self._update_stylesheet()
        return super().showEvent(a0)

    def _calculate_border_radius(self):
        return int(
            (min(self.height(), self.width()))
            * self.theme.boder_radius.get(self.border_radius)
        )

    def _update_stylesheet(self):
        if self._variant in [Variant.FLAT, Variant.ELEVATED]:
            bg_color = self.theme.get_color(self._color)
            bg_color_hover = self.theme.get_hover_color(self._color)
            color = color_hover = "white"
            border = f"1px solid {bg_color}"
        elif self._variant in [Variant.OUTLINED]:
            bg_color = "transparent"
            color = self.theme.get_color(self._color)
            bg_color_hover = self.theme.get_color(self._color)
            color_hover = "white"
            border = f"1px solid {color}"
        elif self._variant in [Variant.TEXT]:
            bg_color = "transparent"
            color = self.theme.get_color(self._color)
            bg_color_hover = self.theme.get_hover_color(self._color)
            color_hover = "white"
            border = "none"
        else:
            bg_color = bg_color_hover = "transparent"
            color = color_hover = self.theme.get_hover_color(self._color)
            border = "none"

        style_sheet = f"""
        QFrame {{
            border: {border};
            border-radius: {self._calculate_border_radius()}px;
            background-color: {bg_color};
            color: {color};
        }}
        QFrame:hover {{
            background-color: {bg_color_hover};
            color: {color_hover};
        }}
        QPushButton {{
            color: {color};
            border: none;
            margin: 0px;
            padding: 0px;
            border: 0px;
            background-color: transparent;
            
        }}
        QPushButton:hover {{
            color: {color_hover};
        }}
        QLabel {{
            color: {color};
            border: none;
            margin: 0px;
            padding: 0px;
            border: 0px;
            background-color: transparent;
        }}
        """
        self.setStyleSheet(style_sheet)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if self._variant in [Variant.ELEVATED]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)  # 偏移
            shadow.setBlurRadius(16)  # 阴影半径
            shadow.setColor(Qt.GlobalColor.darkGray)  # 阴影颜色
            self.setGraphicsEffect(shadow)

    def set_variant(self, variant: str):
        if self._variant == variant:
            return
        self._variant = variant
        self.update_style.emit()

    def set_color(self, color: str):
        if self._color == color:
            return
        self._color = color
        self.update_style.emit()

    def disable(self):
        self.setDisabled(True)
        return self

    def enable(self):
        self.setDisabled(False)
        return self

from typing import Any, Callable, Optional, Union

from PyQt6.QtWidgets import QFrame,QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


from pydashboard.style.variant import Variant
from pydashboard.theme import Theme


class MaterialFrame(QFrame):
    update_style = pyqtSignal()

    def __init__(
        self,
        variant: Optional[str] = None,
        color: Optional[str] = None,
        border_raidus: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = Theme()
        self.variant = variant or Variant.FLAT.value
        self.color = color or "primary"
        self.border_raidus = border_raidus or self.theme.default_border_raidus

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 6, 12, 6)
        self._layout.setSpacing(1)



        self.update_style.connect(self._update_stylesheet)
        self._update_stylesheet()




    def _update_stylesheet(self):
        if self.variant in [Variant.FLAT, Variant.ELEVATED]:
            bg_color = self.theme.get_color(self.color)
            color = "white"
            border = f"1px solid {bg_color}"
        elif self.variant in [Variant.OUTLINED]:
            bg_color = "transparent"
            color = self.theme.get_color(self.color)
            border = f"1px solid {color}"
        elif self.variant in [Variant.TEXT, Variant.PLAIN]:
            bg_color = "transparent"
            color = self.theme.get_color(self.color)
            border = "none"
        else:
            bg_color = "transparent"
            color = self.theme.get_color(self.color)
            border = "none"

        border_raidus = self.border_raidus

        style_sheet = f"""
        QFrame {{
            background-color: {bg_color};
            border-radius: {border_raidus};
            border: {border};
        }}
        QLabel {{
            color: {color or 'transparent'};
            border: none;
        }}
        """
        self.setStyleSheet(style_sheet)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if self.variant in [Variant.ELEVATED]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)  # 偏移
            shadow.setBlurRadius(16)  # 阴影半径
            shadow.setColor(Qt.GlobalColor.darkGray)  # 阴影颜色
            self.setGraphicsEffect(shadow)

    def set_variant(self, variant: str):
        if self.variant == variant:
            return
        self.variant = variant
        self.update_style.emit()

    def set_color(self, color: str):
        if self.color == color:
            return
        self.color = color
        self.update_style.emit()

    def disable(self):
        self.setDisabled(True)
        return self

    def enable(self):
        self.setDisabled(False)
        return self

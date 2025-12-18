from enum import Enum
from typing import Callable, Optional

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class Colors(Enum):
    PRIMARY = "#2196F3"
    SUCCESS = "#4CAF50"
    DANGER = "#F44336"
    WARNING = "#FF9800"
    GERY = "#9E9E9E"


class FlatButton(QPushButton):

    def __init__(
        self,
        text: str,
        color: Optional[Colors] = None,
        on_click: Optional[Callable[[], None]] = None,
    ):
        super().__init__(text)
        # self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if color:
            self.setStyleSheet(
                f"""QPushButton {{
                        background-color: {color.value};
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {color.value.replace('#', '#CC')};
                    }}
                """
            )
        if on_click:
            self.clicked.connect(on_click)

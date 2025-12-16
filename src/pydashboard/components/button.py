from typing import Callable, Optional
from PyQt6.QtWidgets import QPushButton


class FlatButton(QPushButton):

    def __init__(
        self,
        text: str,
        color: Optional[str] = None,
        on_click: Optional[Callable[[], None]] = None,
    ):
        super().__init__(text)
        # self.setFlat(True)
        if color:
            self.setStyleSheet(f"background-color: {color}; color: white;")
        if on_click:
            self.clicked.connect(on_click)

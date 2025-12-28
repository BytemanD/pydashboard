from typing import Optional

from PyQt6.QtGui import QIcon
from qtawesome import icon as qta_icon

from pydashboard.style.color import Colors


class MIcon:
    COLORS: Colors = Colors()

    @classmethod
    def get(cls, name: str, color: Optional[str] = None) -> QIcon:
        if color:
            c = cls.COLORS.translate(color)
        else:
            c = 'white'
        return qta_icon(name, color=c or 'white')

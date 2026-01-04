from typing import Union

from pydantic import BaseModel


class BorderRadius(BaseModel):
    none: int = 0
    sm: float = 0.1
    md: float = 0.2
    lg: float = 0.3
    xl: float = 0.4
    round: float = 0.5

    def get(self, name: str) -> Union[int, float]:
        field = name
        if hasattr(self, field):
            return getattr(self, field)
        return self.md

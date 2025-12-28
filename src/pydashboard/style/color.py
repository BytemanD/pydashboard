from typing import Optional
from pydantic import BaseModel, ConfigDict


class Colors(BaseModel):
    model_config = ConfigDict(extra="allow")

    primary: str = "#2196F3"
    info: str = "#03A9F4"
    success: str = "#4CAF50"
    danger: str = "#F44336"
    warning: str = "#FF9800"

    cyan: str =  "#00BCD4"
    teal: str =  "#009688"
    purple: str = "#9C27B0"
    grey: str = "#9E9E9E"

    def translate(self, name: str|int) -> Optional[str|int]:
        if isinstance(name, int):
            return name
        if name.startswith('#'):
            return name
        field = getattr(self, name, None)
        return field

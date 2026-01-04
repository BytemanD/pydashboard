from pydantic import BaseModel, ConfigDict


class Colors(BaseModel):
    model_config = ConfigDict(extra="allow")

    primary: str = "#2196F3"
    info: str = "#03A9F4"
    success: str = "#4CAF50"
    danger: str = "#F44336"
    warning: str = "#FF9800"

    cyan: str = "#00BCD4"
    teal: str = "#009688"
    purple: str = "#9C27B0"
    grey: str = "#9E9E9E"

    def get(self, name: str) -> str:
        field = name
        if hasattr(self, field):
            return getattr(self, field)
        return name



class HoverColors(BaseModel):
    model_config = ConfigDict(extra="allow")

    primary: str = "#1976D2"
    info: str = "#0288D1"
    success: str = "#43A047"
    danger: str = "#D32F2F"
    warning: str = "#F57C00"

    cyan: str = "#0097A7"
    teal: str = "#00796B"
    purple: str = "#7B1FA2"
    grey: str = "#616161"

    def get(self, name: str) -> str:
        field = name
        if hasattr(self, field):
            return getattr(self, field)
        return name.replace("#", "#CC")

from pydantic import BaseModel, ConfigDict


class Colors(BaseModel):
    model_config = ConfigDict(extra="allow")

    primary: str = "#2196F3"
    success: str = "#4CAF50"
    danger: str = "#F44336"
    warning: str = "#FF9800"
    grey: str = "#9E9E9E"

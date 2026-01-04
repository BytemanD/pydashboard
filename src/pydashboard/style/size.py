from pydantic import BaseModel


class Size(BaseModel):
    sm: str = "10px"
    md: str = "14px"
    lg: str = "18px"
    xl: str = "24px"

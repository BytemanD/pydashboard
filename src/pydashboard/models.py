from typing import Any, List, Mapping, Optional, Union

from pydantic import BaseModel


class TableHeader(BaseModel):
    name: str
    label: Optional[str] = None
    hide: bool = False

    def text(self) -> str:
        return self.label or self.name


class DataTable(BaseModel):
    """数据表模型"""

    headers: List[TableHeader] = []
    data: List[Mapping[str, Union[str, int, float, bool, Any]]] = []
    max_page: int = 1

    def header_rename(self) -> Mapping[str, str]:
        return {x.name: x.label or x.name for x in self.headers}

    def header_names(self) -> List[str]:
        return [x.name for x in self.headers]

    def header_labels(self, _all=True) -> List[str]:
        return [x.text() for x in self.headers]

import sys
from typing import List, Mapping

from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QGridLayout, QPushButton
from loguru import logger

from pydashboard.components.button import MButton
from pydashboard.components.button_group import ButtonGroup
from pydashboard.components.icon import MIcon
from pydashboard.layout.cell import Cell
from pydashboard.models import DataTable, TableHeader

from pydashboard.theme import Theme
from pydashboard.style import Variant, Colors
from pydashboard import app


def fake_fetch(page: int):
    rows: int = 20
    cols: int = 20
    logger.info("获取第 {} 页数据", page)
    return DataTable(
        headers=[TableHeader(name=f"col-{i}", label=f"列{i+1}") for i in range(cols)],
        data=[
            {f"col-{i}": f"数据({(page-1) * rows + row},{i+1})" for i in range(cols)}
            for row in range(rows)
        ],
        max_page=10,
    )


def func_update(changes: List[Mapping]):
    logger.success("更新数据：{}", changes)


class ComponentsDemo(app.MainWindow):
    def __init__(self):
        super().__init__("组件")
        self.setup_ui()

    def setup_ui(self):
        self.add_label(Variant.FLAT.value, 0, 0)
        self.add_cell(
            Cell([MButton(f"{x}", color=x) for x in Colors.model_fields]),
            0,
            1,
        )
        self.add_label(Variant.ELEVATED.value, 1, 0)
        self.add_cell(
            Cell(
                [
                    MButton(f"{x}", color=x, variant=Variant.ELEVATED)
                    for x in Colors.model_fields
                ]
            ),
            1,
            1,
        )
        self.add_label(Variant.OUTLINED.value, 2)
        self.add_cell(
            Cell(
                [
                    MButton(f"{x}", color=x, variant=Variant.OUTLINED)
                    for x in Colors.model_fields
                ]
                + [
                    MButton("lime", color="lime", variant=Variant.OUTLINED),
                ]
            ),
            2,
            1,
        )
        self.add_label(Variant.TEXT.value, 3)
        self.add_cell(
            Cell(
                [
                    MButton(f"{x}", color=x, variant=Variant.TEXT)
                    for x in Colors.model_fields
                ]
            ),
            3,
            1,
        )
        self.add_label(Variant.PLAIN.value, 4)

        self.add_cell(
            Cell(
                [
                    MButton(f"{x}", color=x, variant=Variant.PLAIN)
                    for x in Colors.model_fields
                ]
            ),
            4,
            1,
        )
        self.add_label("带图标的按钮", 5)
        self.add_cell(
            Cell(
                [
                    MButton("mdi.information", color="info", icon="mdi.information"),
                    MButton("mdi.bell", color="primary", icon="mdi.bell"),
                    MButton(
                        "中文", color="warning", variant=Variant.TEXT, icon="mdi.home"
                    ),
                    MButton(
                        "mdi.alert",
                        color="danger",
                        variant=Variant.TEXT,
                        icon="mdi.alert",
                    ),
                ]
            ),
            5,
            1,
        )
        self.add_label("禁用按钮", 6)
        self.add_cell(
            Cell(
                [
                    MButton("删除", color="danger").disable(),
                    MButton("删除", color="danger", variant=Variant.ELEVATED).disable(),
                    MButton("删除", color="danger", variant=Variant.OUTLINED).disable(),
                    MButton("删除", color="danger", variant=Variant.TEXT).disable(),
                    MButton("删除", color="danger", variant=Variant.PLAIN).disable(),
                ]
            ),
            6,
            1,
        )


if __name__ == "__main__":
    app.run(
        ComponentsDemo(),
        theme=Theme(colors=Colors.model_validate({"lime": "#CDDC39"})),
    )

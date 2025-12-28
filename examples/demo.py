import sys
from typing import List, Mapping

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton
from loguru import logger

from pydashboard.components.button import MButton
from pydashboard.components.button_group import ButtonGroup
from pydashboard.layout.cell import Cell
from pydashboard.models import DataTable, TableHeader

from pydashboard.theme import Theme
from pydashboard.style import Variant, Colors


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数据表示例")
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.central_layout = QGridLayout(self.central_widget)
        for i in range(12):
            for j in range(12):
                self.central_layout.addWidget(QWidget(), i, j, 1, 1)

        self.central_layout.addWidget(
            Cell(items=[MButton(f"{x}", color=x) for x in Colors.model_fields]),
            0,
            0,
            1,
            6,
        )
        self.central_layout.addWidget(
            Cell(
                items=[
                    MButton(f"{x}", color=x, variant=Variant.ELEVATED)
                    for x in Colors.model_fields
                ]
            ),
            0,
            6,
        )
        self.central_layout.addWidget(
            Cell(
                items=[
                    MButton(f"{x}", color=x, variant=Variant.OUTLINED)
                    for x in Colors.model_fields
                ]
                + [
                    MButton("info", color="info", variant=Variant.OUTLINED),
                    MButton("purple", color="purple", variant=Variant.OUTLINED),
                    MButton("cyan", color="cyan", variant=Variant.OUTLINED),
                    MButton("teal", color="teal", variant=Variant.OUTLINED),
                ]
            ),
            1,
            0,
        )
        self.central_layout.addWidget(
            Cell(
                items=[
                    MButton(f"{x}", color=x, variant=Variant.TEXT)
                    for x in Colors.model_fields
                ]
            ),
            1,
            6,
        )
        self.central_layout.addWidget(
            Cell(
                items=[
                    MButton(f"{x}", color=x, variant=Variant.PLAIN)
                    for x in Colors.model_fields
                ]
            ),
            2,
            0,
        )
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        Theme(
            colors=Colors.model_validate(
                {
                    "info": "#03A9F4",
                    "cyan": "#00BCD4",
                    "teal": "#009688",
                    "purple": "#9C27B0",
                }
            )
        ).style_sheet
    )
    font = app.font()
    font.setPointSize(10)  # 设置字体大小为12点
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

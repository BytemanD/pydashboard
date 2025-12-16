import sys
from typing import List, Mapping
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
)
from loguru import logger

from pydashboard.models import DataTable, TableHeader
from pydashboard.datatable import Table


def fake_fetch(page: int):
    rows: int = 20
    cols: int = 20
    logger.info("获取第 {} 页数据", page)
    return DataTable(
        headers=[TableHeader(name=f'col-{i}', label=f"列{i+1}") for i in range(cols)],
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

        self.server_table = Table(func_fetch=fake_fetch,
                                  func_update=func_update)
        # self.server_table.fetch_func = fake_fetch

        self.setup_ui()
        # self.server_table.hide_column("列1")

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.central_layout = QGridLayout(self.central_widget)
        self.central_layout.addWidget(self.server_table)

        self.setCentralWidget(self.central_widget)
        self.resize(1000, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import (
    QTableView,
    QHeaderView,
    QFrame,
    QMainWindow,
    QApplication,
    QAbstractItemView,
    QWidget,
    QGridLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt6.QtGui import QStandardItem, QStandardItemModel

from pydashboard.datatable import DataTableView

def make_model(rows: int, cols: int):
    model = QStandardItemModel(rows, cols)
    for row in range(rows):
        for col in range(cols):
            item = QStandardItem(f"数据({row+1},{col+1})")
            model.setItem(row, col, item)
    model.setHorizontalHeaderLabels([f"列{i+1}" for i in range(cols)])
    return model


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建自定义表格视图
        self.tableView = DataTableView(frozen_columns=2)

        # 创建模型和数据
        model = make_model(25, 10)
        self.tableView.setModel(model)

        self.central_widget = QWidget(self)
        self.central_layout = QGridLayout(self.central_widget)

        self.btn_output = QPushButton("输出")
        self.btn_output.clicked.connect(self.output_data)
        self.central_layout.addWidget(self.btn_output)
        self.central_layout.addWidget(self.tableView)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("自定义列冻结TableView")
        self.resize(800, 500)

    def output_data(self):
        """输出数据
        """
        self.tableView.export(format="csv")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

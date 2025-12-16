from collections import defaultdict
from typing import Any, Dict, List, Mapping, Optional, Union
import sys

from pydantic import BaseModel
from PyQt6.QtWidgets import (
    QTableView,
    QHeaderView,
    QMainWindow,
    QApplication,
    QAbstractItemView,
    QWidget,
    QGridLayout,
    QPushButton,QMessageBox,QStatusBar
)
from PyQt6.QtCore import (
    QAbstractItemModel,
    Qt,
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
)
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QPalette, QColor



class TableHeader(BaseModel):
    name: str
    label: Optional[str] = None


class DataTable(BaseModel):
    """数据表模型"""

    headers: List[TableHeader]
    data: List[Mapping[str, Union[str, int, float, bool]]] = []

    def header_rename(self) -> Mapping[str, str]:
        return {x.name: x.label or x.name for x in self.headers}

    def header_names(self) -> List[str]:
        return [x.name for x in self.headers]

    def header_labels(self) -> List[str]:
        return [x.label or x.name for x in self.headers]


# 模拟数据
table_dict = {
    "headers": [
        {"name": "id", "label": "ID"},
        {"name": "name", "label": "姓名"},
        {"name": "age", "label": "年龄"},
        {"name": "field1", "label": "字段1"},
        {"name": "field2", "label": "字段2"},
        {"name": "field3", "label": "字段3"},
        {"name": "field4", "label": "字段4"},
    ],
    "data": [
        {"name": "张三", "age": 18, "field1": 1, "field3": "xxx", "id": 1},
        {"name": "李四", "age": 44, "field2": 2, "field3": 3, "field4": 4, "id": 2},
        {"name": "王五", "age": 25, "field1": 5, "field2": 6, "id": 3},
        {"id": 4, "name": "赵六", "age": 36, "field1": 7, "field2": 8, "field3": 9},
    ],
}


class TrackerDataModel(QStandardItemModel):
    """带变更跟踪的数据模型"""

    def __init__(self, source: DataTable):
        super().__init__()
        self.source = source
        # 变更记录
        self.changes = {
            "add": defaultdict(dict),
            "update": defaultdict(dict),
            "remove": defaultdict(dict),
        }

        self.setHorizontalHeaderLabels(self.source.header_labels())
        self.setRowCount(len(self.source.data))
        for row_idx, row_data in enumerate(self.source.data):
            for col_idx, header in enumerate(self.source.headers):
                item = QStandardItem()
                item.setData(row_data.get(header.name), Qt.ItemDataRole.UserRole)
                item.setText(str(row_data.get(header.name) or ""))
                # item.setData(True, Qt.DisplayRole)
                self.setItem(row_idx, col_idx, item)
                # breakpoint()

    def _row_data(self, n: int) -> Mapping[str, Any]:
        """获取第n行数据, 转化为dict"""
        row_data = {}
        for col in range(self.columnCount()):
            col_data = self.data(self.index(n, col), role=Qt.ItemDataRole.UserRole)
            if col_data is None:
                continue
            row_data[self.source.header_names()[col]] = col_data
        return row_data

    def add_row(self):
        self.setRowCount(self.rowCount() + 1)

    def delete_row(self, row: int):
        self.removeRow(row)

    def compare(self):
        """比较变更"""

        def _compare_row(n: int) -> Dict:
            different_data = {}
            for col in range(self.columnCount()):
                user_data = self.index(n, col).data(role=Qt.ItemDataRole.UserRole)
                display_data = self.index(n, col).data(role=Qt.ItemDataRole.DisplayRole)
                if user_data is None and not display_data:
                    continue
                print("----------", n, col, user_data, display_data)
                if str(user_data) != str(display_data):
                    different_data[self.source.headers[col].name] = display_data

            return different_data

        add_data = []
        update_data = []
        remove_data = []

        source_data_map = {row["id"]: row for row in self.source.data}
        model_data_map = {}
        for row in range(self.rowCount()):
            _id_index = self.data(self.index(row, 0), role=Qt.ItemDataRole.UserRole)
            if _id_index is None:
                # _id_index 为空，则认为是新增
                _row_data = _compare_row(row)
                if _row_data:
                    add_data.append(_row_data)
                continue
            # 以防万一，通常情况下 _id_index 肯定存在于source_data_map
            assert _id_index in source_data_map
            _row_data = self._row_data(row)
            model_data_map[_id_index] = _row_data
            # breakpoint()
            # 去除None值再对比，如果不同，则认为有变更
            differents = _compare_row(row)
            if differents:
                differents["id"] = _id_index
                update_data.append(differents)

        # 最后计算删除的行
        remove_data.extend(
            [
                row_data
                for key, row_data in source_data_map.items()
                if key in (source_data_map.keys() - model_data_map.keys())
            ]
        )
        print("新增数据:", add_data)
        print("更新数据:", update_data)
        print("删除数据:", remove_data)
        print()


class EditableTableView(QTableView):
    def __init__(self, model: TrackerDataModel):
        super().__init__()
        self._model = model
        # 基本高亮设置
        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )  # 整行选择
        self.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )  # 单行选择

        # 设置选中颜色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(65, 105, 225))  # 皇家蓝
        palette.setColor(
            QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white
        )  # 白色文字
        self.setModel(model)
        

    def setModel(self, model: QAbstractItemModel | None) -> None:
        super().setModel(model)
        header = self.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def delete_selected_row(self):
        """删除当前选中行（无确认）"""
        selected_indexes = self.selectedIndexes()
        
        if not selected_indexes:
            QMessageBox.warning(self, "警告", "请先选择要删除的行！")
            return

        rows = set([x.row() + 1 for x in selected_indexes])

        # 确认对话框
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除第 {rows} 行吗",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            rows_to_delete = sorted(rows, reverse=True)
            for row in rows_to_delete:
                self._model.removeRow(row-1)
            QMessageBox.information(self, "成功", f"已删除第行 {rows_to_delete}")

    def iterrows(self, role=Qt.ItemDataRole.DisplayRole):
        model = self.model()
        if model is None:
            return
        for row in range(model.rowCount()):
            yield [
                model.index(row, col).data(role=role)
                for col in range(model.columnCount())
            ]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("自定义列冻结TableView")
        self.resize(800, 500)

        self.model = TrackerDataModel(DataTable.model_validate(table_dict))
        self.tableView = EditableTableView(self.model)
        self.tableView.setModel(self.model)
        # self.tableView.hideColumn(0)

        self.btn_output = QPushButton("输出")
        self.btn_output.clicked.connect(self.output_data)

        self.btn_compare = QPushButton("比较")
        self.btn_compare.clicked.connect(self.model.compare)

        self.btn_add = QPushButton("+")
        self.btn_add.clicked.connect(self.model.add_row)

        self.btn_delete = QPushButton("-")
        self.btn_delete.clicked.connect(self.tableView.delete_selected_row)

        self.central_widget = QWidget(self)
        self.central_layout = QGridLayout(self.central_widget)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)


        self.setup_ui()

    def setup_ui(self):
        # 创建自定义表格视图
        self.central_layout.addWidget(self.btn_output, 0, 0)
        self.central_layout.addWidget(self.btn_compare, 0, 1)
        self.central_layout.addWidget(self.btn_add, 0, 2)
        self.central_layout.addWidget(self.btn_delete, 0, 3)

        self.central_layout.addWidget(self.tableView, 1, 0, 1, 12)

        self.setCentralWidget(self.central_widget)

    def output_data(self):
        """输出数据"""
        export_io = sys.stdout
        split_char = "\t"

        for cols in self.tableView.iterrows():
            export_io.write(split_char.join([str(x) for x in cols]) + "\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

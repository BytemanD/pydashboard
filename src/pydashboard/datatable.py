from io import StringIO
import sys
from typing import Optional
from PyQt6.QtWidgets import QTableView, QHeaderView, QFrame, QAbstractItemView
from PyQt6.QtCore import Qt, QItemSelection, QItemSelectionModel
from PyQt6.QtGui import QStandardItem, QStandardItemModel


class DataTableView(QTableView):
    """自定义数据表视图"""

    def __init__(self, frozen_columns=2):
        super().__init__()
        self.frozen_columns = frozen_columns
        self.frozen_tableview = QTableView(self)
        self.setup_frozen_tableview()
        self._syncing_selection = False

    def setup_frozen_tableview(self):
        """设置冻结表格"""
        self.frozen_tableview.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        f_v_header = self.frozen_tableview.verticalHeader()
        f_h_header = self.frozen_tableview.horizontalHeader()
        if f_v_header is not None:
            f_v_header.hide()
        if f_h_header is not None:
            f_h_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        # 设置冻结表格的滚动条策略
        self.frozen_tableview.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )  # 隐藏水平滚动条
        self.frozen_tableview.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )  # 隐藏垂直滚动条
        vsb = self.frozen_tableview.verticalScrollBar()
        if vsb is not None:
            vsb.valueChanged.connect(vsb.setValue)
        # 设置无边框
        self.frozen_tableview.setFrameShape(QFrame.Shape.NoFrame)
        self.frozen_tableview.setStyleSheet(
            """
            QTableView {
                border: none;  /* 确保无边框 */
                outline: none; /* 移除焦点边框 */
            }
            
            QTableView::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """
        )

        vp = self.viewport()
        if vp:
            vp.stackUnder(self.frozen_tableview)

    def setModel(self, model):
        """设置模型"""
        super().setModel(model)
        self.frozen_tableview.setModel(model)
        self.update_frozen_tableview_geometry()

        # 只显示前几列
        if model:
            for col in range(model.columnCount()):
                if col >= self.frozen_columns:
                    self.frozen_tableview.setColumnHidden(col, True)

        # 同步列宽
        for col in range(self.frozen_columns):
            self.frozen_tableview.setColumnWidth(col, self.columnWidth(col))

        # 连接选择信号
        self.connect_selection_signals()

    def connect_selection_signals(self):
        """连接选择变化信号"""
        sm = self.selectionModel()
        if sm:
            sm.selectionChanged.connect(self.on_main_selection_changed)
        frozen_sm = self.frozen_tableview.selectionModel()
        if frozen_sm:
            frozen_sm.selectionChanged.connect(self.on_frozen_selection_changed)

    def on_main_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        """主表格选择变化时的处理"""
        if self._syncing_selection:
            return

        self._syncing_selection = True

        # 获取当前选择
        sm = self.selectionModel()
        frozen_sm = self.frozen_tableview.selectionModel()
        if sm:
            selected_indexes = sm.selectedIndexes()

            if selected_indexes and frozen_sm:
                # 取消冻结表格的所有选择
                frozen_sm.clearSelection()

                # 检查是否选择了冻结列
                has_frozen_selection = any(
                    index.column() < self.frozen_columns for index in selected_indexes
                )

                if has_frozen_selection:
                    # 如果选择了冻结列，在冻结表格中也选择
                    for index in selected_indexes:
                        if index.column() < self.frozen_columns:
                            frozen_sm.select(
                                index, QItemSelectionModel.SelectionFlag.Select
                            )

        self._syncing_selection = False

    def on_frozen_selection_changed(self, selected, deselected):
        """冻结表格选择变化时的处理"""
        if self._syncing_selection:
            return

        self._syncing_selection = True
        # 获取冻结表格的选择
        sm = self.selectionModel()
        f_sm = self.frozen_tableview.selectionModel()
        if f_sm:
            frozen_selected = f_sm.selectedIndexes()
            if frozen_selected and sm:
                # 取消主表格的所有选择
                sm.clearSelection()
        self._syncing_selection = False

    def update_frozen_tableview_geometry(self):
        """更新冻结表格的几何形状"""
        if not self.model():
            return

        total_width = 0
        for col in range(self.frozen_columns):
            total_width += self.columnWidth(col)

        v_header = self.verticalHeader()
        h_header = self.horizontalHeader()
        viewport = self.viewport()
        if v_header and h_header and viewport:
            self.frozen_tableview.setGeometry(
                v_header.width() + self.frameWidth(),
                self.frameWidth(),
                total_width,
                viewport.height() + h_header.height(),
            )

    def resizeEvent(self, e):
        """重写 resize 事件"""
        super().resizeEvent(e)
        self.update_frozen_tableview_geometry()

        # 同步垂直滚动
        self.frozen_tableview.setVerticalScrollMode(self.verticalScrollMode())

    def scrollTo(self, index, hint=QAbstractItemView.ScrollHint):
        """重写滚动事件"""
        if index.column() >= self.frozen_columns:
            super().scrollTo(index, hint)

    def _generate_data_lines(self, split_char: str = "\t"):
        model = self.model()
        if model:
            h_header = self.horizontalHeader()
            if h_header is not None:
                yield split_char.join(
                    [
                        model.headerData(i, Qt.Orientation.Horizontal)
                        for i in range(h_header.count())
                    ]
                )

            for row in range(model.rowCount()):
                yield split_char.join(
                    [
                        model.data(model.index(row, col))
                        for col in range(model.columnCount())
                    ]
                )

    def export(self, output: Optional[str] = None, format: Optional[str] = None):
        """导出数据"""
        export_io = sys.stdout if output is None else open(output, "w")
        # if output:
        #     with open(output, "w") as f:
        #         for line in self._generate_data_lines():
        #             f.write(line + "\n")
        # else:
        if format == "csv":
            split_char=","
        else:
            split_char="\t"

        for line in self._generate_data_lines(split_char=split_char):
            export_io.write(line + "\n")


def make_model(rows: int, cols: int):
    model = QStandardItemModel(rows, cols)
    for row in range(rows):
        for col in range(cols):
            item = QStandardItem(f"数据({row+1},{col+1})")
            model.setItem(row, col, item)
    model.setHorizontalHeaderLabels([f"列{i+1}" for i in range(cols)])
    return model

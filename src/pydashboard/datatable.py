from collections import defaultdict

from functools import partial
import sys
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union
from PyQt6.QtWidgets import (
    QTableView,
    QHeaderView,
    QFrame,
    QAbstractItemView,
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QHBoxLayout,
    QDialog,
)
from PyQt6.QtCore import (
    Qt,
    QItemSelection,
    QItemSelectionModel,
    pyqtSignal,
    QThread,
    QTimer,
)
from PyQt6.QtGui import (
    QShowEvent,
    QStandardItem,
    QStandardItemModel,
    QStandardItem,
    QPalette,
    QColor,
)
from loguru import logger
from pydashboard.components.button import Colors, FlatButton
from pydashboard.components.dialog import DraggableListDialog, MultiSelectDialog, Item
from pydashboard.components.pagination import PagesWidget
from pydashboard.job import DataTableThread, ListThread
from pydashboard.models import DataTable


CustomRole = Qt.ItemDataRole.UserRole + 100


class DataModel(QStandardItemModel):
    """带变更跟踪的数据模型"""

    def __init__(self, source: DataTable, top_headers: Optional[List[str]] = None):
        super().__init__()
        self.source = source
        if top_headers:
            self.display_headers = [
                x for x in self.source.headers if x.name in top_headers
            ] + [x for x in self.source.headers if x.name not in top_headers]
        else:
            self.display_headers = self.source.headers

        self.refresh()

    def refresh(self):
        self.setHorizontalHeaderLabels([x.text() for x in self.display_headers])
        self.setRowCount(len(self.source.data))
        for row_idx, row_data in enumerate(self.source.data):
            for col_idx, header in enumerate([x for x in self.display_headers]):
                item = QStandardItem(str(row_data.get(header.name) or ""))
                item.setData(row_data.get(header.name), Qt.ItemDataRole.UserRole)
                item.setData(row_idx, CustomRole)
                self.setItem(row_idx, col_idx, item)

    def header_names(self, all: bool = True) -> List[str]:
        return [x.name for x in self.display_headers]

    def header_labels(self, _all: bool = True) -> List[str]:
        return [x.text() for x in self.display_headers]

    def _row_data(self, n: int) -> Mapping[str, Any]:
        """获取第n行数据, 转化为dict"""
        if 0 <= n < self.rowCount():
            return self.source.data[n]
        return {}

    def compare(self):
        """比较变更"""

        def _compare_row(n: int) -> Dict:
            different_data = {}
            for col in range(self.columnCount()):
                user_data = self.index(n, col).data(role=Qt.ItemDataRole.UserRole)
                display_data = self.index(n, col).data(role=Qt.ItemDataRole.DisplayRole)
                if user_data is None and not display_data:
                    continue
                if str(user_data) != str(display_data):
                    different_data[self.source.headers[col].name] = display_data

            return different_data

        def _edited_data(row: int) -> Mapping[str, str]:
            return {
                self.display_headers[x]
                .name: self.index(row, x)
                .data(role=Qt.ItemDataRole.DisplayRole)
                for x in range(self.columnCount())
                if self.index(row, x).data(role=Qt.ItemDataRole.DisplayRole) is not None
            }

        changes = []
        exists_row = set([])
        for row in range(self.rowCount()):
            setted_row: Optional[int] = self.index(row, 0).data(role=CustomRole)
            if setted_row is None:
                # index_row 为空，则认为是新增

                changes.append({"source": None, "change": _edited_data(row)})
                continue
            exists_row.add(setted_row)
            changed_data = _compare_row(row)
            if changed_data:
                changes.append(
                    {"source": self.source.data[setted_row], "change": changed_data}
                )
                continue

        # 最后计算删除的行
        for source_row in [
            x for i, x in enumerate(self.source.data) if i not in exists_row
        ]:
            changes.append({"source": source_row, "change": None})
        return changes

    def column_index(self, name: str):
        for i, header in enumerate(self.source.headers):
            print(i, header.label, name)
            if header.name == name or header.label == name:
                return i
        return -1


class TableView(QTableView):
    """自定义数据表视图"""

    def __init__(self, resize_mode=QHeaderView.ResizeMode.ResizeToContents):
        super().__init__()
        self.resize_mode = resize_mode
        self.frozen_tableview = QTableView(self)

        self.setup_frozen_tableview()

        self._syncing_selection = False

        # 基本高亮设置
        # 整行选择
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # 单行选择
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        # 设置选中颜色
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(65, 105, 225))  # 皇家蓝
        palette.setColor(
            QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white
        )  # 白色文字
        self.frozen_columns = 0

        # 同步两个视图
        vsb = self.verticalScrollBar()
        frozen_vsb = self.frozen_tableview.verticalScrollBar()
        if vsb and frozen_vsb:
            vsb.valueChanged.connect(frozen_vsb.setValue)
            frozen_vsb.valueChanged.connect(vsb.setValue)

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
                color: orange;
            }
            
            QTableView::item:selected {
                background-color: #0078d4;
            }
        """
        )

        vp = self.viewport()

        if vp:
            vp.stackUnder(self.frozen_tableview)

    def set_model(self, model: DataModel):
        """设置模型"""
        self.setModel(model)
        header = self.horizontalHeader()
        if header:
            header.setSectionResizeMode(self.resize_mode)

        frozen_header = self.frozen_tableview.horizontalHeader()
        if frozen_header:
            frozen_header.setSectionResizeMode(self.resize_mode)

        self.frozen_tableview.setModel(model)
        self.update_frozen_tableview_geometry()

        # 只显示前几列
        if model:
            for col in range(model.columnCount()):
                self.frozen_tableview.setColumnHidden(col, col >= self.frozen_columns)
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


class Table(QWidget):

    def __init__(
        self,
        hide_columns: list[int] = [],
        resize_mode=QHeaderView.ResizeMode.ResizeToContents,
        # selection_mode=QAbstractItemView.SelectionMode.MultiSelection,
        func_fetch: Optional[Callable[[int], DataTable]] = None,
        func_update: Optional[Callable[[List[Mapping]], None]] = None,
    ) -> None:
        super().__init__()
        self.resize_mode = resize_mode
        self.hide_columns = hide_columns

        self.model = DataModel(DataTable())

        self.btn_add = FlatButton("新增", on_click=self.add_row, color=Colors.SUCCESS)
        self.btn_save = FlatButton("保存", on_click=self.save, color=Colors.PRIMARY)
        self.btn_delete = FlatButton(
            "删除", on_click=self.delete_selected_row, color=Colors.DANGER
        )

        self.btn_export = FlatButton("导出", on_click=self.export)
        self.btn_drag = FlatButton("调整表头", on_click=self.drag_columns)
        self.btn_frozen = FlatButton("冻结", on_click=self.open_frozen_dialog)
        self.btn_hide = FlatButton("隐藏", on_click=self.open_hide_dialog)
        self.btn_refresh = FlatButton("刷新", on_click=self.refresh)

        self.view = TableView(resize_mode=resize_mode)

        self.page_widget = PagesWidget()
        self.page_widget.page_changed.connect(self._page_changed)

        self.func_fetch = func_fetch
        self.func_update = func_update
        self._frozen_columns: list[str] = []
        self._hide_columns: list[str] = []

        self.tool_layout = QHBoxLayout()
        self.tool_layout.addWidget(self.btn_add)
        self.tool_layout.addWidget(self.btn_save)
        self.tool_layout.addWidget(self.btn_delete)
        self.tool_layout.addStretch()
        self.tool_layout.addWidget(self.btn_export)
        self.tool_layout.addWidget(self.btn_drag)
        self.tool_layout.addWidget(self.btn_hide)
        self.tool_layout.addWidget(self.btn_frozen)
        self.tool_layout.addWidget(self.btn_refresh)

        self._layout = QVBoxLayout(self)
        self._layout.addLayout(self.tool_layout)
        self._layout.addWidget(self.view)
        self._layout.addWidget(self.page_widget)

        self.set_datatable(self.model.source)

    def showEvent(self, a0: QShowEvent | None) -> None:
        QTimer.singleShot(1, partial(self.page_widget.go_to, 1))
        return super().showEvent(a0)

    def add_row(self):
        self.model.setRowCount(self.model.rowCount() + 1)

    def open_frozen_dialog(self):
        items = [Item(name=x.name, label=x.label) for x in self.model.source.headers]
        dialog = MultiSelectDialog(
            items,
            title="选择冻结的列",
            selected=[i for i, x in enumerate(items) if x.name in self._frozen_columns],
            parent=self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        self._frozen_columns = dialog.get_selected_items()
        self.set_datatable(self.model.source)

    def open_hide_dialog(self):
        """隐藏列选择器"""
        items = [Item(name=x.name, label=x.label) for x in self.model.source.headers]
        dialog = MultiSelectDialog(
            [Item(name=x.name, label=x.label) for x in self.model.source.headers],
            title="选择隐藏的列",
            selected=[i for i, x in enumerate(items) if x.name in self._hide_columns],
            parent=self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        self._hide_columns = dialog.get_selected_items()
        self.set_datatable(self.model.source)

    def refresh(self):
        self.page_widget.go_to(self.page_widget.current_page)

    def set_datatable(self, dt: DataTable):
        # 调整冻结列
        self.model = DataModel(dt, top_headers=self._frozen_columns)
        self.view.frozen_columns = len(self._frozen_columns)

        self.view.set_model(self.model)

        for i, header in enumerate(self.model.display_headers):
            self.view.setColumnHidden(i, header.name in self._hide_columns)
            self.view.frozen_tableview.setColumnHidden(
                i, header.name in self._hide_columns
            )
        self.page_widget.set_total_page(dt.max_page)

    def delete_selected_row(self):
        """删除当前选中行"""
        selected_indexes = self.view.selectedIndexes()

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
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            rows_to_delete = sorted(rows, reverse=True)
            for row in rows_to_delete:
                self.model.removeRow(row - 1)
            # QMessageBox.information(self, "成功", f"已删除第行 {rows_to_delete}")

    def iterrows(self, role=Qt.ItemDataRole.DisplayRole):
        if self.model is None:
            return
        for row in range(self.model.rowCount()):
            yield [
                self.model.index(row, col).data(role=role) or ""
                for col in range(self.model.columnCount())
            ]

    def _page_changed(self, page: int):
        """页码改变时触发"""
        if not self.func_fetch:
            return
        DataTableThread(self, self.func_fetch, page).on_started(
            partial(self.setEnabled, False)
        ).on_finished(partial(self.setEnabled, True)).on_success(
            self.set_datatable
        ).start()

    def save(self):
        if not self.func_update:
            return
        changes = self.model.compare()
        if not changes:
            logger.info("没有数据被修改")
            return
        logger.info("变化的数据: {}", changes)
        ListThread(self, self.func_update, changes).on_started(
            partial(self.setEnabled, False)
        ).on_finished(partial(self.setEnabled, True)).on_exception(
            lambda e: logger.error("更新失败: {}", e), self._save_failed
        ).start()

    def _save_failed(self, e: Exception):
        QMessageBox.warning(self, "更新失败", str(e))

    def export(self):
        """导出数据"""
        output: Optional[str] = None
        format: Optional[str] = None
        export_io = sys.stdout if output is None else open(output, "w")
        if format == "csv":
            split_char = ","
        else:
            split_char = "\t"

        export_io.write(split_char.join(self.model.header_labels()) + "\n")
        for row in self.iterrows():
            export_io.write(split_char.join(row) + "\n")

        if export_io is not sys.stdout:
            export_io.close()

    def drag_columns(self):
        dialog = DraggableListDialog(
            "调整列顺序",
            [
                Item(name=x.name, label=x.text())
                for x in self.model.display_headers
                if x.name not in self._frozen_columns
            ],
            parent=self,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        items = dialog.get_current_order()

        headers_map = {x.name: x for x in self.model.display_headers}
        display_headers = [headers_map[x] for x in self._frozen_columns] + [
            headers_map[x] for x in items
        ]
        self.model.display_headers = display_headers
        self.model.refresh()

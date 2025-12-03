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
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QInputDialog,
)
from PyQt6.QtCore import (
    Qt,
    QItemSelection,
    QItemSelectionModel,
    QSortFilterProxyModel,
    pyqtSignal,
    QThread,
    QTimer,
)
from PyQt6.QtGui import (
    QShowEvent,
    QStandardItem,
    QStandardItemModel,
    QStandardItem,QPalette, QColor
)
from pydashboard.models import DataTable


class DataModel(QStandardItemModel):
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
                self.setItem(row_idx, col_idx, item)

    def header_names(self) -> List[str]:
        return [x.name for x in self.source.headers]

    def header_labels(self) -> List[str]:
        return [x.label or x.name for x in self.source.headers]

    def _row_data(self, n: int) -> Mapping[str, Any]:
        """获取第n行数据, 转化为dict"""
        row_data = {}
        for col in range(self.columnCount()):
            col_data = self.data(self.index(n, col), role=Qt.ItemDataRole.UserRole)
            if col_data is None:
                continue
            row_data[self.source.header_names()[col]] = col_data
        return row_data

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
                {"id": key}
                for key, row_data in source_data_map.items()
                if key in (source_data_map.keys() - model_data_map.keys())
            ]
        )
        print("新增数据:", add_data)
        print("更新数据:", update_data)
        print("删除数据:", remove_data)
        print()


class TableView(QTableView):
    """自定义数据表视图"""

    def __init__(self, frozen_columns: int = 0):
        super().__init__()
        self.frozen_columns = frozen_columns
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
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(model)

        proxy_model.setFilterKeyColumn(1)

        super().setModel(proxy_model)

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


class PagesWidget(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.btn_first = QPushButton("首页")
        self.btn_first.clicked.connect(self.first_page)
        self.btn_prev = QPushButton("上一页")
        self.btn_prev.clicked.connect(self.pre_page)

        self.label_current = QLineEdit()
        self.label_current.setText("0")
        self.label_current.setMaximumWidth(50)
        self.label_total = QLabel("1")

        self.btn_next = QPushButton("下一页")
        self.btn_next.clicked.connect(self.next_page)
        self.btn_last = QPushButton("尾页")
        self.btn_last.clicked.connect(self.last_page)

        self._layout = QHBoxLayout(self)
        self._layout.addStretch(1)
        self._layout.addWidget(self.btn_first)
        self._layout.addWidget(self.btn_prev)
        self._layout.addWidget(QLabel("第"))
        self._layout.addWidget(self.label_current)
        self._layout.addWidget(QLabel("/"))
        self._layout.addWidget(self.label_total)
        self._layout.addWidget(QLabel("页"))
        self._layout.addWidget(self.btn_next)
        self._layout.addWidget(self.btn_last)
        self._layout.addStretch(1)

    @property
    def current_page(self) -> int:
        return int(self.label_current.text() or 0)

    @property
    def total_page(self) -> int:
        return int(self.label_total.text() or 1)

    def go_to(self, page: int):
        if page == self.current_page or page < 1 or page > self.total_page:
            return
        self.label_current.setText(str(page))
        self.page_changed.emit(self.current_page)

        if self.current_page <= 1:
            self.btn_first.setEnabled(False)
            self.btn_prev.setEnabled(False)
        else:
            self.btn_first.setEnabled(True)
            self.btn_prev.setEnabled(True)

    def set_total_page(self, max_page: int):
        """设置最大页数"""
        self.label_total.setText(str(max_page))

        if self.current_page >= self.total_page:
            self.btn_next.setEnabled(False)
            self.btn_last.setEnabled(False)
        else:
            self.btn_next.setEnabled(True)
            self.btn_last.setEnabled(True)

    def pre_page(self):
        """上一页"""
        if self.current_page <= 1:
            return
        self.go_to(self.current_page - 1)

    def next_page(self):
        """下一页"""
        if self.current_page >= self.total_page:
            return
        self.go_to(self.current_page + 1)

    def first_page(self):
        """首页"""
        self.go_to(1)

    def last_page(self):
        """尾页"""
        self.go_to(self.total_page)


class ServerTable(QWidget):

    def __init__(
        self,
        frozen_columns=0,
        hide_columns: list[int]=[],
        resize_mode=QHeaderView.ResizeMode.ResizeToContents,
        selection_mode=QAbstractItemView.SelectionMode.MultiSelection,
        fetch_func: Optional[Callable[[int], DataTable]] = None,
    ) -> None:
        super().__init__()
        self.resize_mode = resize_mode
        self.selection_mode = selection_mode
        self.frozen_columns = frozen_columns
        self.hide_columns = hide_columns

        self.model = DataModel(DataTable())

        # 设置选中颜色
        self.btn_add = QPushButton("新增")
        self.btn_add.clicked.connect(self.add_row)
        self.btn_add.setStyleSheet("background-color: green; color: white;")

        self.btn_save = QPushButton("保存")
        self.btn_save.clicked.connect(self.export)
        self.btn_save.setStyleSheet("background-color: blue; color: white;")

        self.btn_delete = QPushButton("删除")
        self.btn_delete.setStyleSheet("background-color: red; color: white;")
        self.btn_delete.clicked.connect(self.delete_selected_row)

        self.btn_frozen = QPushButton("冻结")
        self.btn_frozen.clicked.connect(self.open_frozen_dialog)

        self.tool_layout = QHBoxLayout()
        self.tool_layout.addWidget(self.btn_add)
        self.tool_layout.addWidget(self.btn_save)
        self.tool_layout.addWidget(self.btn_delete)
        self.tool_layout.addWidget(self.btn_frozen)

        self.tool_layout.addStretch()

        self.view = TableView()
        # self.view.frozen_columns = self.frozen_columns + len(self.hide_columns)

        self.page_widget = PagesWidget()

        self._layout = QVBoxLayout(self)
        self._layout.addLayout(self.tool_layout)
        self._layout.addWidget(self.view)
        self._layout.addWidget(self.page_widget)

        self.page_widget.page_changed.connect(self._page_changed)

        self.fetch_func = fetch_func

        self.setup_ui()

    def showEvent(self, a0: QShowEvent | None) -> None:
        QTimer.singleShot(1, partial(self.page_widget.go_to, 1))
        return super().showEvent(a0)

    def add_row(self):
        self.model.setRowCount(self.model.rowCount() + 1)

    def open_frozen_dialog(self):
        max_frozen_column = self.model.columnCount() - len(self.hide_columns)
        number, ok = QInputDialog.getInt(
            self,
            "选择冻结列",
            f"请选择0-{max_frozen_column}之间的数字:",
            value=self.view.frozen_columns,
            min=0,
            max=max_frozen_column,
            step=1,
        )
        if ok:
            self.view.frozen_columns = number + len(self.hide_columns)
            self.view.setModel(self.model)

    def setup_ui(self):
        pass

    def set_datatable(self, dt: DataTable):
        self.model = DataModel(dt)
        self.view.setModel(self.model)
        for c in self.hide_columns:
            self.view.hideColumn(c)
        header = self.view.horizontalHeader()
        if header:
            header.setSectionResizeMode(self.resize_mode)
        self.page_widget.set_total_page(dt.max_page)
        # self.view.frozen_columns = self.frozen_columns + len(self.hide_columns)

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
        if not self.fetch_func:
            return
        FetchThread(self, partial(self.fetch_func, page)).on_started(
            partial(self.setEnabled, False)
        ).on_finished(partial(self.setEnabled, True)).on_success(
            self.set_datatable
        ).start()

    def export(self):
        """导出数据"""
        self.model.compare()
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


class FetchThread(QThread):
    signal_success = pyqtSignal(DataTable)

    def __init__(self, parent, func: Callable[[], DataTable]):
        super().__init__(parent)
        self.func = func

    def on_started(self, *args: Callable[[], None]):
        self.started.connect(*args)
        return self

    def on_finished(self, *args: Callable[[], None]):
        self.finished.connect(*args)
        return self

    def on_success(self, *args: Callable[[DataTable], Any]):
        self.signal_success.connect(*args)
        return self

    def run(self) -> None:
        dt = self.func()
        self.signal_success.emit(dt)

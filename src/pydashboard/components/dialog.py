from collections import OrderedDict
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
)


from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

from pydantic import BaseModel

from pydashboard.components.list import DraggableListWidget


class Item(BaseModel):
    name: str
    label: Optional[str] = None


class MultiSelectDialog(QDialog):
    def __init__(
        self,
        items: list[Item],
        title: Optional[str] = None,
        selected: List[int] = [],
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title or "多选对话框")
        self.resize(300, 400)

        self.items = items
        self.list_widget = QListWidget()
        # 添加项目
        for item in self.items:
            self.list_widget.addItem(item.label or item.name)
        for x in selected:
            item = self.list_widget.item(x)
            if item:
                item.setSelected(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建列表控件
        self.list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )


        # 按钮区域
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        btn_select_all = QPushButton("全选")
        btn_select_all.clicked.connect(self.select_all)

        btn_clear_all = QPushButton("清空")
        btn_clear_all.clicked.connect(self.clear_selection)

        btn_ok = QPushButton("确定")
        btn_ok.clicked.connect(self.accept)

        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)

        top_layout.addStretch()
        top_layout.addWidget(btn_select_all)
        top_layout.addWidget(btn_clear_all)
        bottom_layout.addWidget(btn_ok)
        bottom_layout.addWidget(btn_cancel)

        # 添加到主布局
        layout.addLayout(top_layout)
        layout.addWidget(self.list_widget)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def select_all(self):
        """全选"""
        self.list_widget.selectAll()

    def clear_selection(self):
        """清除选择"""
        self.list_widget.clearSelection()

    def get_selected_items(self):
        """获取选中的项目"""
        selected = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item and item.isSelected():
                selected.append(self.items[index].name)
        return selected


class DraggableListDialog(QDialog):
    """可拖动列表对话框"""

    def __init__(self, title: str, items: List[Item], parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(title or "可拖动列表排序对话框")
        self.resize(300, 500)
        # self.init_ui()
        self.items = OrderedDict()
        for x in items:
            self.items[x.name] = x.label
        self.list_widget = DraggableListWidget()
        self.reset()
        # 重置按钮
        self.reset_button = QPushButton("重置列表")
        self.reset_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        )
        self.ok_button = QPushButton("确定")
        self.ok_button.setStyleSheet(
            """
            QPushButton {
                background-color: orange;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
        """
        )
        self.ok_button.clicked.connect(self.accept)
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """
        )
        self.cancel_button.clicked.connect(self.reject)
        self.reset_button.clicked.connect(self.reset)
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.reset_button)
        main_layout.addLayout(button_layout)

        # 底部按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.cancel_button)
        bottom_layout.addWidget(self.ok_button)

        main_layout.addLayout(bottom_layout)
        # 设置对话框布局
        self.setLayout(main_layout)

    def reset(self):
        """重置列表到初始状态"""
        self.list_widget.clear()
        for k, v in self.items.items():
            item = QListWidgetItem(v)
            item.setData(Qt.ItemDataRole.UserRole, k)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsDragEnabled)
            self.list_widget.addItem(item)

    def get_current_order(self):
        """获取当前列表顺序（供外部调用）"""
        items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if not item:
                continue
            items.append(item.data(Qt.ItemDataRole.UserRole))
        return items

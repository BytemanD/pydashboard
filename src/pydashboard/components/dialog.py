from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QListWidget,
)
from pydantic import BaseModel


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
        self.init_ui()
        for x in selected:
            item = self.list_widget.item(x)
            if item:
                item.setSelected(True)

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建列表控件
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )

        # 添加项目
        for item in self.items:
            self.list_widget.addItem(item.label or item.name)

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

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import pyqtSignal

from pydashboard.components.button import FlatButton


class PagesWidget(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.btn_first = FlatButton("首页", on_click=self.first_page)
        self.btn_prev = FlatButton("上一页", on_click=self.pre_page)

        self.label_current = QLineEdit()
        self.label_current.setText("0")
        self.label_current.setMaximumWidth(50)
        self.label_total = QLabel("1")

        self.btn_next = FlatButton("下一页", on_click=self.next_page)
        self.btn_last = FlatButton("尾页", on_click=self.last_page)

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

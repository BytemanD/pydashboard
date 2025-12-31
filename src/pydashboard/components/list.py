from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag
from PyQt6.QtWidgets import QListWidget


class DraggableListWidget(QListWidget):
    """支持拖拽重新排序的列表组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setStyleSheet(
            """
            QListWidget {
                border: 2px;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                border: 1px solid;
                border-radius: 3px;
                padding: 10px;
                margin: 2px;
                font-size: 14px;
            }
            QListWidget::item:hover {
                background-color: #333333;
                border-color: #4d90fe;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #4d90fe;
                color: white;
                border-color: #3079ed;
            }
        """
        )

    def startDrag(self, supportedActions):
        super().startDrag(supportedActions)
        """自定义拖拽开始时的行为"""
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(item.text())
            drag.setMimeData(mime_data)

            # 设置拖拽时的预览效果
            viewport = self.viewport()
            if viewport:
                drag.setHotSpot(viewport.mapFromGlobal(self.cursor().pos()))
            drag.exec(Qt.DropAction.MoveAction)

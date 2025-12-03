from PyQt6.QtGui import QStandardItem, QStandardItemModel

def make_model(rows: int, cols: int):
    model = QStandardItemModel(rows, cols)
    for row in range(rows):
        for col in range(cols):
            item = QStandardItem(f"数据({row+1},{col+1})")
            model.setItem(row, col, item)
    model.setHorizontalHeaderLabels([f"列{i+1}" for i in range(cols)])
    return model

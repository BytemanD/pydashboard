
import sys
from PyQt6.QtWidgets import QApplication
from pydashboard.dashboard import Dashboard


def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()

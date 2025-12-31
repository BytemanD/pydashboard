from typing import Any, Callable

from PyQt6.QtCore import QThread, pyqtBoundSignal, pyqtSignal

from pydashboard.models import DataTable


class CommonThread(QThread):
    # signal_success = pyqtSignal()
    signal_exception = pyqtSignal(Exception)

    def __init__(self, parent, func: Callable, *args, **kwargs):
        super().__init__(parent)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def on_started(self, *args: Callable[[], None]):
        for func in args:
            self.started.connect(func)
        return self

    def on_finished(self, *args: Callable[[], None]):
        for func in args:
            self.finished.connect(func)
        return self

    def on_success(self, *args: Callable[[DataTable], Any]):
        signal_success = getattr(self, "signal_success", None)
        if not signal_success:
            return self
        if not isinstance(signal_success, pyqtBoundSignal):
            raise ValueError("signal_success is not a pyqtBoundSignal")
        for func in args:
            signal_success.connect(func)
        return self

    def on_exception(self, *args: Callable[[Exception], None]):
        for func in args:
            self.signal_exception.connect(func)
        return self

    def run(self) -> None:
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.signal_exception.emit(e)
        else:
            signal_success = getattr(self, "signal_success", None)
            if signal_success and isinstance(signal_success, pyqtBoundSignal):
                if result is not None:
                    signal_success.emit(result)
                else:
                    signal_success.emit()
        finally:
            self.finished.emit()


class DataTableThread(CommonThread):
    signal_success = pyqtSignal(DataTable)


class ListThread(CommonThread):
    signal_success = pyqtSignal()

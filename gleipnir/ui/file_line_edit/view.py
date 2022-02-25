from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtWidgets import QLineEdit


class FileLineEdit(QLineEdit):
    dropped = Signal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.setText(file_path)
        self.dropped.emit(file_path)
"""
ColorWidget View is a view class for colored buttons that automatically changes
their colors when it is selected in color dialog.

Author: Artem Shepelin
License: GPLv3
"""


from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtWidgets import QPushButton


class ColorButton(QPushButton):
    colorChanged = Signal(object)


    def __init__(self, *args, color=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = None
        self._default = color

        self.pressed.connect(self.onColorPicker)

        self.setColor(self._default)


    def setColor(self, color):
        if self._color != color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            self.setStyleSheet(f"background-color: {self._color};")
        else:
            self.setStyleSheet("")


    @property
    def color(self):
        return self._color


    def onColorPicker(self):
        color = (QColorDialog.getColor(QColor(self._color))
                 if self._color else QColorDialog.getColor(QColor("#000000")))
        if color.isValid():
            self.setColor(color.name())
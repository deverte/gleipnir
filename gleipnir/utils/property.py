"""
Property is a helper class for data binding ability, very useful for Model data.

Author: Artem Shepelin
License: GPLv3
"""

from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtCore import QObject


class Property(QObject):
    changed = Signal(object)


    def __init__(self, value):
        super().__init__()

        self._value = value


    @property
    def value(self):
        return self._value


    def setValue(self, value):
        self._value = value
        self.changed.emit(value)
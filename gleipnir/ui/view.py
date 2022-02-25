"""
MainWindowView View is a view class for application main window.
It loads and shows form designed in Qt Designer.

Author: Artem Shepelin
License: GPLv3
"""

import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow


class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "main.ui"), self)

        theme_file = os.path.join(os.path.dirname(__file__), "dark_theme.qss")
        if os.path.exists(theme_file):
            self.setStyleSheet(open(theme_file, "r").read())

        self.show()
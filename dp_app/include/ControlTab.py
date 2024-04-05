from include.UIs.ControlTab_ui import Ui_ControlTab
from PyQt6.QtWidgets import QWidget


class ControlTab(QWidget, Ui_ControlTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

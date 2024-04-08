from include.UIs.ControlPanelTab_ui import Ui_ControlPanelTab
from PyQt6.QtWidgets import QWidget


class ControlPanelTab(QWidget, Ui_ControlPanelTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
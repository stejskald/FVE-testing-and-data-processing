from include.AbstractDataModels.AbstractTableModel import TableModel
from include.UIs.CSVRawDataTab_ui import Ui_CSVRawDataTab
from PyQt6.QtWidgets import QHeaderView, QWidget


class CSVRawDataTab(QWidget, Ui_CSVRawDataTab):
    def __init__(self, data, headers):  # , headers=[], parent=None
        super(CSVRawDataTab, self).__init__()
        self.setupUi(self)
        # _headers = headers

        # Getting the Model
        self.tableModel = TableModel(data)

        # Creating a QTableView
        self.tableView.setModel(self.tableModel)

        # QTableView Headers
        self.horizHeader = self.tableView.horizontalHeader()
        self.vertHeader = self.tableView.verticalHeader()
        self.horizHeader.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # type: ignore
        self.vertHeader.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # type: ignore
        # self.horizHeader.setStretchLastSection(True)

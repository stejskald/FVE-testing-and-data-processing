from include.AbstractDataModels.AbstractTableModel import TableModel
from dp_app.include.UIs.CSVDataTab_ui import Ui_CSVDataTab
from PyQt6.QtWidgets import QHeaderView, QWidget


class CSVDataTab(QWidget, Ui_CSVDataTab):
    def __init__(self):
        super(CSVDataTab, self).__init__()
        self.setupUi(self)

    # TODO Take a look at QTreeView and optimization uniformRowHeights
    def setTableDataModel(self, data):
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

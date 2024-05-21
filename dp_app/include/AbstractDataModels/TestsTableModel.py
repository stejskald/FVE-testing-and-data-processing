from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt6.QtWidgets import QApplication
import pandas as pd
import os.path as path
import dp_app.include.fileTools as ft
from datetime import datetime

# relative pathing to handle situation when starting the app from different locations
appBaseDir = path.abspath(path.join(__file__, "../../.."))


# TODO Implement add/remove Row <----------------------------------------------------------------
class TableModel(QAbstractTableModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super(TableModel, self).__init__()
        self._data = data

        self.readConfig()

    def rowCount(self, parent=QModelIndex()):
        # return len(self._df.index)
        # return self._data.count().max()
        return self._data.shape[0]  # numpy, pandas

    def columnCount(self, parent=QModelIndex()):
        # return len(self._df.columns)
        return self._data.shape[1]  # numpy, pandas

    # Extension with pandas
    # The headerData method also receives other roles, which can be used to customise
    # the appearance of the headers further.
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._data.columns[section]
            else:  # if orientation == Qt.Orientation.Vertical:
                return self._data.index[section]

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if index.row() >= self._data.shape[0] or index.row() < 0:
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            # The nested-list data structure
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list

            # Get the raw value:
            # pandas .iloc method, for indexed locations — lookup by col and/or row idx
            value = self._data.iloc[index.row(), index.column()]  # pandas

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to HH:MM:SS.ffffff
                return value.strftime("%H:%M:%S.%f")
            elif isinstance(value, float):
                # Render float to 2 dp
                return f"{value:.2f}"
            elif isinstance(value, str):
                # return '"%s"' % value  # Render strings with quotes
                return value  # Render strings without quotes
            # Default (anything not captured above: e.g. int)
            return str(value)  # conversion to string needed for pandas

        # Handles keeping the current value if trying to edit the cell content
        elif role == Qt.ItemDataRole.EditRole:
            return str(self._data.iloc[index.row(), index.column()])

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            value = self._data.iloc[index.row(), index.column()]  # pandas
            if isinstance(value, float):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            # Default (anything not captured above: e.g. datetime, str...)
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        elif role == Qt.ItemDataRole.BackgroundRole:
            return QApplication.palette().base()  # QColor(Qt.GlobalColor.white)

        return QVariant()

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        # if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
        if index.isValid():
            self._data.iloc[index.row(), index.column()] = value
            # the change will be applied to all views dependent on this model
            self.dataChanged.emit(index, index)
            return True
        return False

    # Called by a view to check the cell status
    def flags(self, index):
        fl = super(self.__class__, self).flags(index)
        fl |= Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        # | Qt.ItemFlag.ItemIsDragEnabled
        # | Qt.ItemFlag.ItemIsDropEnabled
        return fl

    def readConfig(self):
        # Read the uncertainty_P from the INI config file
        self.uncertP = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.uncertainties",
                "uncertainty_P",
            )
        )

        # Read the uncertainty_Q from the INI config file
        self.uncertQ = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.uncertainties",
                "uncertainty_Q",
            )
        )

        # Read the real_power_3ph from the INI config file
        self.realPower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.pq_diagram",
            "real_power_3ph",
        )

        # Read the reactive_power_3ph from the INI config file
        self.reactivePower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.pq_diagram",
            "reactive_power_3ph",
        )

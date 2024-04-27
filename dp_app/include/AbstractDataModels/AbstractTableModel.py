from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor, QIcon
import os.path as path
import dp_app.include.fileTools as ft
from datetime import datetime
import numpy as np
from math import ceil

# relative pathing to handle situation when starting the app from different locations
appBaseDir = path.abspath(path.join(__file__, "../../.."))


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

        self.readConfig()

    def rowCount(self, index):  # , parent=QModelIndex()
        return self._data.shape[0]  # numpy, pandas

    def columnCount(self, index):  # , parent=QModelIndex()
        return self._data.shape[1]  # numpy, pandas

    # Extension with pandas
    # The headerData method also receives other roles, which can be used to customise
    # the appearance of the headers further.
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            else:  # if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # The nested-list data structure
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list

            # Get the raw value:
            # value = self._data[index.row()][index.column()] # will also work for numpy
            # value = self._data[index.row(), index.column()]  # numpy
            # pandas .iloc method, for indexed locations — lookup by col and/or row idx
            value = self._data.iloc[index.row(), index.column()]  # pandas

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to HH:MM:SS.ffffff
                return value.strftime("%H:%M:%S.%f")
            elif isinstance(value, float):
                if index.column() == self._data.columns.get_loc(self.realPower3ph):
                    return (
                        f"({value:.2f}±{(ceil(abs(value*100)/100)*self.uncertP):.2f})"  # value*100/100 for precision!
                    )
                elif index.column() == self._data.columns.get_loc(self.reactivePower3ph):
                    return (
                        f"({value:.2f}±{(ceil(abs(value*100)/100)*self.uncertQ):.2f})"  # value*100/100 for precision!
                    )
                else:
                    # Render float to 2 dp
                    return f"{value:.2f}"
            elif isinstance(value, str):
                return value  # Render strings without quotes
                # return '"%s"' % value  # Render strings with quotes
            # Default (anything not captured above: e.g. int)
            # return value
            return str(value)  # conversion to string needed for pandas

        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.white)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        elif role == Qt.ItemDataRole.DecorationRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, np.bool_):
                if value:
                    return QIcon(path.join(appBaseDir, "icons", "check.ico"))
                return QIcon(path.join(appBaseDir, "icons", "exit.ico"))

        # Tooltip message will be shown when hovering over a cell
        elif role == Qt.ItemDataRole.ToolTipRole:
            value = self._data.iloc[index.row(), index.column()]
            # return "row: {}, col: {}".format(index.row() + 1, index.column() + 1)
            return "cell data type: {}".format(type(value))

        return None

    def readConfig(self):
        # Read the uncertainty_P from the INI config file
        self.uncertP = float(
            str(
                ft.iniReadSectionKey(
                    path.join(appBaseDir, "appConfig.ini"),
                    "app.uncertainties",
                    "uncertainty_P",
                )
            )
        )

        # Read the uncertainty_Q from the INI config file
        self.uncertQ = float(
            str(
                ft.iniReadSectionKey(
                    path.join(appBaseDir, "appConfig.ini"),
                    "app.uncertainties",
                    "uncertainty_Q",
                )
            )
        )

        # Read the real_power_3ph from the INI config file
        self.realPower3ph = str(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.pq_diagram",
                "real_power_3ph",
            )
        )

        # Read the reactive_power_3ph from the INI config file
        self.reactivePower3ph = str(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.pq_diagram",
                "reactive_power_3ph",
            )
        )

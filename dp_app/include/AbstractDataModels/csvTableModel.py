from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
import pandas as pd
import os.path as path
import dp_app.include.fileTools as ft
from datetime import datetime
import numpy as np
from math import ceil, sqrt

# relative pathing to handle situation when starting the app from different locations
appBaseDir = path.abspath(path.join(__file__, "../../.."))


# # Read the fetch_data_sequentially from the INI config file
# fetchDataSeq = ft.iniReadSectionKey(
#     path.join(appBaseDir, "appConfig.ini"),
#     "app.csv_data",
#     "fetch_data_sequentially",
# )
# # Enable fetching data sequentially to the table view
# FETCH_DATA_SEQUENTIALLY = False if fetchDataSeq == "False" else True
FETCH_DATA_SEQUENTIALLY = True


class TableModel(QAbstractTableModel):
    def __init__(self, data=pd.DataFrame(), parent=None):
        super(TableModel, self).__init__()
        self._data = data

        if FETCH_DATA_SEQUENTIALLY:
            self.rowsLoaded = 0
            # self.numberPopulated = pyqtSignal(int)

        self.readConfig()

    def rowCount(self, parent=QModelIndex()):
        if FETCH_DATA_SEQUENTIALLY:
            return 0 if parent.isValid() else self.rowsLoaded
        else:
            return self._data.shape[0]  # numpy, pandas

    def columnCount(self, parent=QModelIndex()):
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
        if not index.isValid():
            return QVariant()

        if index.row() >= self._data.shape[0] or index.row() < 0:
            return QVariant()

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
                if index.column() == self._data.columns.get_loc(self.voltagePh2PhMean):
                    uncertMeanU = sqrt(self.uncertU**2 + self.uncertU**2 + self.uncertU**2)  # geometric sum
                    return f"({value:.2f}±{(ceil(abs(value))*uncertMeanU):.2f})"
                elif index.column() == self._data.columns.get_loc(self.realPower3ph):
                    return f"({value:.2f}±{(ceil(abs(value))*self.uncertP):.2f})"
                elif index.column() == self._data.columns.get_loc(self.reactivePower3ph):
                    return f"({value:.2f}±{(ceil(abs(value))*self.uncertQ):.2f})"
                elif index.column() == self._data.columns.get_loc(self.signalizationU):
                    return f"({value:.2f}±{(ceil(abs(value))*self.uncertU):.2f})"
                elif index.column() == self._data.columns.get_loc(self.frequency):
                    return f"({value:.3f}±{self.uncertFreq:.3f})"
                elif index.column() == self._data.columns.get_loc(self.cosPhi):
                    return f"({value:.2f}±{self.uncertFreq:.2f})"
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
            return QApplication.palette().base()  # QColor(Qt.GlobalColor.white)

        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        elif role == Qt.ItemDataRole.DecorationRole:
            value = self._data.iloc[index.row(), index.column()]
            if isinstance(value, np.bool_):
                if value:
                    return QIcon(path.join(appBaseDir, "icons", "check.ico"))
                return QIcon(path.join(appBaseDir, "icons", "exit.ico"))

        # # Tooltip message will be shown when hovering over a cell
        # elif role == Qt.ItemDataRole.ToolTipRole:
        #     value = self._data.iloc[index.row(), index.column()]
        #     # return "row: {}, col: {}".format(index.row() + 1, index.column() + 1)
        #     return "cell data type: {}".format(type(value))

        return QVariant()

    if FETCH_DATA_SEQUENTIALLY:

        def canFetchMore(self, parent: QModelIndex) -> bool:
            if parent.isValid():
                return False
            return self.rowsLoaded < self._data.shape[0]

        def fetchMore(self, parent: QModelIndex) -> None:
            if parent.isValid():
                return

            remainder = self._data.shape[0] - self.rowsLoaded
            itemsToFetch = min(20, remainder)

            if itemsToFetch <= 0:
                return

            self.beginInsertRows(parent, self.rowsLoaded, self.rowsLoaded + itemsToFetch - 1)

            self.rowsLoaded += itemsToFetch

            self.endInsertRows()

            # self.numberPopulated.emit(itemsToFetch)  # is not working

    def readConfig(self):
        # Read the avg_u_ph2ph_mean from the INI config file
        self.voltagePh2PhMean = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "avg_u_ph2ph_mean",
        )

        # Read the real_power_3ph from the INI config file
        self.realPower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "real_power_3ph",
        )

        # Read the reactive_power_3ph from the INI config file
        self.reactivePower3ph = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "reactive_power_3ph",
        )

        # Read the signalization_U from the INI config file
        self.signalizationU = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "signalization_U",
        )

        # Read the frequency from the INI config file
        self.frequency = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "frequency",
        )

        # Read the cos_phi from the INI config file
        self.cosPhi = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "cos_phi",
        )

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

        # Read the uncertainty_U from the INI config file
        self.uncertU = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.uncertainties",
                "uncertainty_U",
            )
        )

        # Read the uncertainty_cos_phi from the INI config file
        self.uncertCosPhi = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.uncertainties",
                "uncertainty_cos_phi",
            )
        )

        # Read the uncertainty_freq from the INI config file
        self.uncertFreq = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.uncertainties",
                "uncertainty_freq",
            )
        )

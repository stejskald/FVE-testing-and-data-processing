from datetime import datetime
import numpy as np
import os.path as path
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor, QIcon

# relative pathing to handle situation when starting the app from different locations
appBaseDir = path.abspath(path.join(__file__, "../../.."))


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

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
                # Render time to YYYY-MM-DD.
                return value.strftime("%Y-%m-%d")
            elif isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            elif isinstance(value, str):
                return value  # Render strings without quotes
                return '"%s"' % value  # Render strings with quotes
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
            return "row: {}, col: {}".format(index.row() + 1, index.column() + 1)
            # return "cell data type: {}".format(type(value))

        return None


# class TableModel(QAbstractTableModel):
#     def __init__(self, data, headers=[]):
#         super(TableModel, self).__init__()
#         self._data = data
#         self._headers = headers

#     def rowCount(self):
#         # returns the length of the outer list - number of rows
#         return len(self._data)

#     def columnCount(self):
#         # takes the longest row from data and returns the length - number of columns
#         return len(max(self._data, key=len))

#     def data(self, index, role=Qt.ItemDataRole.DisplayRole):
#         if role == Qt.ItemDataRole.DisplayRole:
#             try:
#                 return self._data[index.row()][index.column()]
#             except IndexError:
#                 return ""

#         # Entire cell content will NOT disappear if double clicked for editting
#         if role == Qt.ItemDataRole.EditRole:
#             return self._data[index.row()][index.column()]

#         # Tooltip message will be shown when hovering over a cell
#         if role == Qt.ItemDataRole.ToolTipRole:
#             return "row: {}, col: {}".format(index.row(), index.column())

#     def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
#         if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
#             if not value:  # if value is blank
#                 return False
#             self._data[index.row()][index.column()] = value
#             # the change will be applied to all views dependent on this model
#             self.dataChanged.emit(index, index)
#         return True

#     # Called by a view to check the cell status
#     def flags(self, index):
#         return super().flags(index) | Qt.ItemFlag.ItemIsEditable

#     def headerData(self, section, orientation, role):
#         if role == Qt.ItemDataRole.DisplayRole:
#             if orientation == Qt.Orientation.Horizontal:
#                 if section < len(self._headers):
#                     return self._headers[section]
#                 else:
#                     return "#"
#             else:
#                 return "Row {}".format(section)

#     def insertRows(self, row, count, parent=QModelIndex()):
#         self.beginInsertRows(parent, row, row + count - 1)

#         defaultValues = [0 for i in range(self.columnCount(None))]
#         for r in range(count):
#             self._data.insert(row, defaultValues)

#         self.endInsertRows()
#         return super().insertRows(row, count, parent)

#     # TODO: Implement removeRows() method
#     def removeRows(self, row, count, parent=QModelIndex()):
#         # self.beginRemoveRows(parent, row, row + count - 1)

#         # for r in range(count):
#         #     self._data.remove(self._data[r])

#         # self.endRemoveRows()
#         # return super().removeRows(row, count, parent=QModelIndex())
#         pass

#     def insertColumns(self, column, count, parent=QModelIndex()):
#         self.beginInsertColumns(parent, column, column + count - 1)

#         rowCount = len(self._data)
#         for c in range(count):
#             for r in range(rowCount):
#                 self._data[r].insert(column, 0)

#         self.endInsertColumns()
#         return super().insertColumns(column, count, parent)

#     # TODO: Implement removeColumns() method
#     def removeColumns(self, column, count, parent=QModelIndex()):
#         pass

# --------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     app = QApplication([])

#     headers = ["A", "B", "C", "D", "E"]

#     data = [
#         ["A1", "A2", "A3"],
#         ["B1", "B2", "B3", "B4"],
#         ["C1", "C2", "C3", "C4", "C5"],
#         ["D1", "D2"],
#     ]

#     window = QMainWindow()
#     window.setMinimumSize(900, 600)
#     table = QTableView()
#     window.setCentralWidget(table)
#     window.show()

#     dataModel = TableModel(data, headers)
#     table.setModel(dataModel)

#     # Practicing Model-View Model - mutual interaction of widgets
#     listView = QListView()
#     listView.setModel(dataModel)
#     listView.show()

#     # dataModel.insertRows(2, 1)
#     # dataModel.insertColumns(1, 2)

#     # Not implemented:
#     # dataModel.removeRows(1, 1)
#     # dataModel.removeColumns(1, 2)

#     app.exec()
# --------------------------------------------------------------------------------------

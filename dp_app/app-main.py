import sys
import os.path as path

import dp_app.include.fileTools as ft
from include.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication

# Allows to assign icon to the app
try:
    from ctypes import windll

    myappid = "cz.vut.FVE-testing.1-0-0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def main():
    appBaseDir = path.dirname(__file__)

    # Read the data_separator from the INI config file
    data_separator = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "data_separator",
    )

    # Read the filtered_columns from the INI config file
    filtered_columns = ft.iniReadSectionKey(
        path.join(appBaseDir, "appConfig.ini"),
        "app.csv_data",
        "filtered_columns",
    )

    data = ft.readCSVdata(path.join(appBaseDir, "data", "data.csv"), data_separator, filtered_columns)
    # print(data)

    # headersAll = ft.csvReadOnlyHeaders(path.join(appBaseDir, "data", "data.csv"), data_separator)
    # print(headersAll)

    #
    #
    #
    #

    app = QApplication(sys.argv)
    app.setOrganizationName("VUT")
    app.setApplicationName("Application-for-data-processing-of-FVE")

    window = MainWindow(data, filtered_columns)

    # window.csvRawData = read_csv_data(path.join(appBaseDir, "data.csv"), filtered_columns)
    # window.csvRawDataHeaders = filtered_columns

    window.show()
    app.exec()


if __name__ == "__main__":
    main()

from datetime import datetime
import pandas as pd
import os.path as path
import dp_app.include.fileTools as ft
import numpy as np
from include.ControlPanelTab import ControlPanelTab
from include.CSVDataTab import CSVDataTab
from include.PQDiagramTab import PQDiagramTab
from include.XYGraphTab import XYGraphTab
from PyQt6.QtCore import QSize, pyqtSlot, QStringListModel
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QToolBar, QFileDialog, QMessageBox

# relative pathing to handle situation when starting the app from different locations
includeDir = path.dirname(__file__)
# print(f"includeDir: {includeDir}")
appBaseDir = path.abspath(path.join(__file__, "../.."))
# print(f"appBaseDir: {appBaseDir}")


class MainWindow(QMainWindow):
    def __init__(self):  # , data, columns):
        super(MainWindow, self).__init__()
        # Read settings from configuration file
        self.mWinReadConfig()

        self.setWindowTitle("The application for data processing of FVE testing")
        self.setWindowIcon(QIcon(path.join(appBaseDir, "icons", "solar-panel.ico")))

        # Scale Main Window relatively to the Main Display size
        screenGeom = self.screen().availableGeometry()  # type: ignore
        self.setFixedSize(int(screenGeom.width() * 0.5), int(screenGeom.height() * 0.5))
        self.setMinimumSize(QSize(800, 600))
        # self.showMaximized() #Full screen

        # Initialize the Menu Bar
        self.mWinMenuInit()

        # Initialize the Toolbar
        self.mWinToolbarInit()

        # Initialize the Tabs
        self.mWinTabsInit()

        # Initialize the Status Bar
        self.mWinStatusBarInit()

        # Initialize the App Shortcuts
        self.mWinShortcutsInit()

        # Initialize the Open CSV Dialog
        self.mWinOpenFileDialogInit()

        self.setCentralWidget(self.tabs)

    def mWinReadConfig(self):
        # Read the csvDataSeparator from the INI config file
        self.csvDataSeparator = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "data_separator",
        )

        # Read the date_time_format from the INI config file
        self.csvDateTimeFmt = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "date_time_format",
        )

        # Read the filtered_columns from the INI config file
        self.csvSamplePeriod = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "sample_period_s",
        )

        # Read the filtered_columns from the INI config file
        self.csvHeaders = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "filtered_columns",
        )

    def mWinMenuInit(self):
        # Menu Bar
        self.mainMenuBar = self.menuBar()

        # Menu Bar - File Menu
        self.fileMenu = self.mainMenuBar.addMenu("&File")  # type: ignore

        fileSubmenu1 = self.fileMenu.addMenu("&Submenu")  # type: ignore
        fileSubmenu1.addAction(QAction("Hello!", self))  # type: ignore

        # Menu Bar - File Menu - Exit QAction
        btnExitApp = QAction(
            QIcon(path.join(appBaseDir, "icons", "exit.ico")),
            "E&xit Application",
            self,
        )
        btnExitApp.setShortcut(QKeySequence("Ctrl+Q"))
        # btnExitApp.setShortcut(QKeySequence.StandardKey.Quit) # e.g. Apple platforms
        btnExitApp.setStatusTip("Push to exit the application.")
        btnExitApp.triggered.connect(self.close)  # type: ignore
        self.fileMenu.addAction(btnExitApp)  # type: ignore

        # Menu Bar - View Menu
        viewMenu = self.mainMenuBar.addMenu("&View")  # type: ignore

        # Menu Bar - View Menu - Show/Hide Toolbar
        self.btnShowToolbar = QAction("Show Toolbar", self)
        self.btnShowToolbar.setStatusTip("Toggle to show/hide the Toolbar.")
        self.btnShowToolbar.triggered.connect(self.setToolbarVisibility)
        self.btnShowToolbar.setCheckable(True)
        self.btnShowToolbar.setChecked(False)
        viewMenu.addAction(self.btnShowToolbar)  # type: ignore

        # Menu Bar - CSV Menu - Import CSV
        csvMenu = self.mainMenuBar.addMenu("&CSV")  # type: ignore
        self.btnImportCSV = QAction(
            QIcon(path.join(appBaseDir, "icons", "import-csv.ico")),
            "&Import CSV Data",
            self,
        )
        self.btnImportCSV.triggered.connect(self.btnClicked)
        csvMenu.addAction(self.btnImportCSV)  # type: ignore

        # Menu Bar - CSV Menu - Show CSV Data
        self.btnCSVShowData = QAction(
            QIcon(path.join(appBaseDir, "icons", "table.ico")),
            "&Show CSV Data",
            self,
        )
        self.btnCSVShowData.triggered.connect(self.btnClicked)
        csvMenu.addAction(self.btnCSVShowData)  # type: ignore

        graphMenu = self.mainMenuBar.addMenu("&Graph Analysis")  # type: ignore
        self.btnShowCSVDataInGraph = QAction(
            QIcon(path.join(appBaseDir, "icons", "xy-graph.ico")),
            "Show &XY Graph",
            self,
        )
        self.btnShowCSVDataInGraph.triggered.connect(self.btnClicked)
        graphMenu.addAction(self.btnShowCSVDataInGraph)  # type: ignore

        self.btnShowPQDiagram = QAction(
            QIcon(path.join(appBaseDir, "icons", "pq-diagram.ico")),
            "Show &PQ Diagram",
            self,
        )
        self.btnShowPQDiagram.triggered.connect(self.btnClicked)
        graphMenu.addAction(self.btnShowPQDiagram)  # type: ignore

        reportMenu = self.mainMenuBar.addMenu("&Reports")  # type: ignore
        self.btnGenerateFinalReport = QAction("Generate Final &Report", self)
        self.btnGenerateFinalReport = QAction(
            QIcon(path.join(appBaseDir, "icons", "printer.ico")),
            "Generate Final &Report",
            self,
        )
        self.btnGenerateFinalReport.triggered.connect(self.btnClicked)
        reportMenu.addAction(self.btnGenerateFinalReport)  # type: ignore

    def mWinToolbarInit(self):
        self.mainToolbar = QToolBar("Toolbar")
        self.mainToolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.mainToolbar)
        self.mainToolbar.hide()  # Hide as default

        self.mainToolbar.visibilityChanged.connect(self.checkToolbarVisibility)

        btnBugAction = QAction(
            QIcon(path.join(appBaseDir, "icons", "bug.ico")),
            "&Bug simulation",
            self,
        )
        btnBugAction.setStatusTip("Simulate a Bug.")
        btnBugAction.setCheckable(True)
        self.mainToolbar.addAction(btnBugAction)
        btnBugAction.setShortcut(QKeySequence("Ctrl+B"))
        self.mainToolbar.addSeparator()

    def mWinTabsInit(self):
        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab - Control Panel
        self.controlTab = ControlPanelTab()
        self.controlTabIdx = self.tabs.addTab(self.controlTab, "Control Panel")
        self.tabs.setTabIcon(
            self.controlTabIdx,
            QIcon(path.join(appBaseDir, "icons", "control-panel.ico")),
        )
        self.controlTab.btnImportCSV.clicked.connect(self.btnClicked)
        self.controlTab.btnImportCSV.setIcon(QIcon(path.join(appBaseDir, "icons", "import-csv.ico")))
        self.controlTab.btnImportCSV.setIconSize(QSize(30, 30))

        self.controlTab.btnShowCSVtable.clicked.connect(self.btnClicked)
        self.controlTab.btnShowCSVtable.setIcon(QIcon(path.join(appBaseDir, "icons", "table.ico")))
        self.controlTab.btnShowCSVtable.setIconSize(QSize(30, 30))

        self.controlTab.btnShowXYgraph.clicked.connect(self.btnClicked)
        self.controlTab.btnShowXYgraph.setIcon(QIcon(path.join(appBaseDir, "icons", "xy-graph.ico")))
        self.controlTab.btnShowXYgraph.setIconSize(QSize(30, 30))

        self.controlTab.btnShowPQdiagram.clicked.connect(self.btnClicked)
        self.controlTab.btnShowPQdiagram.setIcon(QIcon(path.join(appBaseDir, "icons", "pq-diagram.ico")))
        self.controlTab.btnShowPQdiagram.setIconSize(QSize(30, 30))

        self.controlTab.btnGenerateFinalReports.clicked.connect(self.btnClicked)
        self.controlTab.btnGenerateFinalReports.setIcon(QIcon(path.join(appBaseDir, "icons", "printer.ico")))
        self.controlTab.btnGenerateFinalReports.setIconSize(QSize(30, 30))

        # Tab - CSV Data
        self.csvDataTab = CSVDataTab()  # (self.csvData, self.csvHeaders)
        self.csvDataTabIdx = self.tabs.addTab(self.csvDataTab, "CSV Data")
        self.tabs.setTabIcon(self.csvDataTabIdx, QIcon(path.join(appBaseDir, "icons", "table.ico")))

        # Tab - XY Graph
        self.xyGraphTab = XYGraphTab()
        self.xyGraphTabIdx = self.tabs.addTab(self.xyGraphTab, "XY Graph")
        self.tabs.setTabIcon(self.xyGraphTabIdx, QIcon(path.join(appBaseDir, "icons", "xy-graph.ico")))

        self.comboBoxXDataModel = QStringListModel(self.csvHeaders)
        self.xyGraphTab.comboBoxXData.setModel(self.comboBoxXDataModel)
        self.xyGraphTab.comboBoxXData.setCurrentIndex(0)

        self.comboBoxYDataModel = QStringListModel(self.csvHeaders)
        self.xyGraphTab.comboBoxYData.setModel(self.comboBoxYDataModel)
        self.xyGraphTab.comboBoxYData.setCurrentIndex(1)
        # self.comboBoxXData.currentTextChanged.connect(self.adcChannelChanged)

        # Tab - PQ Diagram
        # TODO Get all header names and insert them into list with checkboxes -> selected will be showed in the table
        # and in 2 combo boxes for PQ diagram source data
        self.pqDiagramTab = PQDiagramTab()
        self.pqDiagramTabIdx = self.tabs.addTab(self.pqDiagramTab, "PQ Diagram")
        self.tabs.setTabIcon(
            self.pqDiagramTabIdx,
            QIcon(path.join(appBaseDir, "icons", "pq-diagram.ico")),
        )

        self.tabs.setCurrentIndex(self.controlTabIdx)

    def mWinStatusBarInit(self):
        self.mainStatusBar = QStatusBar(self)
        self.setStatusBar(self.mainStatusBar)
        self.mainStatusBar.showMessage("Welcome Operator! Let's load a CSV file")

    def mWinOpenFileDialogInit(self):
        self.openFileDialog = QFileDialog(self)
        self.openFileDialog.setWindowTitle("Open a CSV file with the data")
        self.openFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.openFileDialog.setNameFilter("CSV Files (*.csv)")
        self.openFileDialog.setViewMode(QFileDialog.ViewMode.Detail)
        self.openFileDialog.setDirectory(path.join(appBaseDir, "data"))

    def mWinShortcutsInit(self):
        # Print Final Report Shortcut
        self.shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut.activated.connect(self.printReport)

    # @pyqtSlot() <- TypeError: missing 1 required positional argument: 'visibility'
    def setToolbarVisibility(self, visibility):
        if visibility:
            self.addToolBar(self.mainToolbar)
            self.mainToolbar.show()
        else:
            self.removeToolBar(self.mainToolbar)

    # @pyqtSlot() <- TypeError: missing 1 required positional argument: 'visibility'
    def checkToolbarVisibility(self, visibility):
        if not visibility:
            self.btnShowToolbar.setChecked(False)
        else:
            self.btnShowToolbar.setChecked(True)

    @pyqtSlot()
    def printReport(self):
        self.mainStatusBar.showMessage("Printing!")

    @pyqtSlot()
    def btnClicked(self):
        sender = self.sender().text()  # .objectName()  # type: ignore
        # print(sender)

        if sender == "&Import CSV Data":  # or btn from CSV Menu
            # Open CSV File dialog
            if self.openFileDialog.exec():
                self.csvFilePath = self.openFileDialog.selectedFiles()[0]
                # self.csvFilePath = QFileDialog.getOpenFileName(
                #     self, "Open a CSV file", path.join(appBaseDir, "data"), "CSV files (*.csv)"
                # )

                # Check if all columns listed in the configuration file are in the data file
                self.csvAllHeaders = ft.csvReadHeaders(self.csvFilePath, self.csvDataSeparator)

                incorrectHeaders = []
                for header in self.csvHeaders:
                    if header not in self.csvAllHeaders:
                        incorrectHeaders.append(header)
                if not incorrectHeaders:  # List is empty
                    # Read data from CSV file
                    self.csvData = ft.readCSVdata(self.csvFilePath, self.csvDataSeparator, self.csvHeaders)

                    # Adjust the data in the Time column "2023-08-31 11:15:24" -> "11:15:24.00" ... "11:15:24.80"
                    # TODO Move to a method
                    # --------------------------------------------------------------------------------------------------
                    # Find and select only first column with "Time"
                    timeColName = [col for col in self.csvData.columns if "Time" in col][0]
                    # Get a date from datetime format (RRRR-MM-DD HH:MM:SS)
                    self.measurementDate = self.csvData[timeColName].str.split(" ").str[0][0]
                    self.xyGraphTab.labelMeasDateValue.setText(self.measurementDate)
                    # Update values in timeColName column with trimming the date part
                    self.csvData[timeColName] = self.csvData[timeColName].str.split(" ").str[1]

                    timeValues = self.csvData[timeColName].values
                    ptimeSecs = []
                    for timestr in timeValues:
                        pt = datetime.strptime(timestr, "%H:%M:%S")  # parsed time
                        ptimeSecs.append(pt.second + pt.minute * 60 + pt.hour * 3600)
                    # Detect differences in the time (list ptimeSecs)
                    timeDiffs = np.array(ptimeSecs[:-1]) - np.array(ptimeSecs[1:])

                    # Some first rows need to be deleted because of adding .00 .20 .40 .60 .80 to the time column data
                    iter = 0
                    while timeDiffs[iter] == 0:
                        # Drop the first row
                        self.csvData = self.csvData.iloc[1:]
                        iter += 1
                    if timeDiffs[iter] == -1:
                        self.csvData = self.csvData.iloc[1:]
                    print(self.csvData)

                    timeColIdx = self.csvData.columns.get_loc(timeColName)
                    dt = float(str(self.csvSamplePeriod))
                    runIter = 0
                    runCount = 1 / dt
                    for idx, row in self.csvData.iterrows():  # Iterate over rows
                        self.csvData.iat[self.csvData.index.get_loc(idx), timeColIdx] = (
                            row[timeColName] + f"{runIter*dt:.2f}"[1:]
                        )
                        print(row[timeColName] + f"{runIter*dt:.2f}"[1:])
                        runIter += 1
                        if runIter == runCount:
                            runIter = 0
                    # --------------------------------------------------------------------------------------------------

                    # Adjust the data in the 3Cosφ[] column "C -0.18" -> float(-0.18)
                    # TODO Move to a method
                    # --------------------------------------------------------------------------------------------------
                    # TODO Finish
                    # Find and select only first column with "3Cos"
                    cosPhiColName = [col for col in self.csvData.columns if "3Cos" in col][0]
                    # Update values in cosPhiColName column with trimming the "C"/"L" part and converting to float64
                    self.csvData[cosPhiColName] = self.csvData[cosPhiColName].str.split(" ").str[1]
                    self.csvData[cosPhiColName] = self.csvData[cosPhiColName].apply(pd.to_numeric, errors="coerce")

                    # --------------------------------------------------------------------------------------------------

                    # Convert the data in the DOI1[] and DOI4[] columns to boolean "False" -> bool(False)
                    # TODO Move to a method
                    # --------------------------------------------------------------------------------------------------
                    # TODO Finish
                    # Find all columns with "DOI"
                    # DOIcolNames = [col for col in self.csvData.columns if "DOI" in col]
                    # Update values in DOIcolNames columns with converting the "True"/"False" to booleans
                    # # Convert the string column 'x1' to boolean
                    # for DOIcol in DOIcolNames:
                    #     self.csvData[DOIcol] = self.csvData[DOIcol].map({'True': True, 'False': False})
                    # --------------------------------------------------------------------------------------------------

                    # Set the TableView Data Model and upload the loaded data
                    self.csvDataTab.csvDataTabSetTableDataModel(self.csvData)

                    # Show CSV Data tab
                    self.tabs.setCurrentIndex(self.csvDataTabIdx)
                    self.mainStatusBar.showMessage("The CSV file has been loaded")

                    # Load data to the xyGraphTab
                    self.xyGraphTab.loadData(self.csvData)

                else:
                    # A critical message shown
                    QMessageBox.critical(
                        self,
                        "Incorrect Configuration File - Wrong headers",
                        "The following headers listed in the configuration file were not found in the CSV Data file: "
                        + f"{incorrectHeaders}. Close the application, edit the configuration file and start the "
                        + "application again.",
                        buttons=QMessageBox.StandardButton.Ok,
                        defaultButton=QMessageBox.StandardButton.Ok,
                    )

        # TODO Finish all button functions
        elif sender == "&Show CSV Data":
            # Show CSV Data tab
            self.tabs.setCurrentIndex(self.csvDataTabIdx)

        elif sender == "Show &XY Graph":
            # Show XY-Graph tab
            self.tabs.setCurrentIndex(self.xyGraphTabIdx)

        elif sender == "Show &PQ Diagram":
            # Show PQ-Diagram tab
            self.tabs.setCurrentIndex(self.pqDiagramTabIdx)

        elif sender == "Generate Final &Report":
            self.mainStatusBar.showMessage("Generate Final Report button has been pressed")

import os.path as path
import dp_app.include.fileTools as ft
from include.ControlPanelTab import ControlPanelTab
from include.CSVRawDataTab import CSVRawDataTab
from include.PQDiagramTab import PQDiagramTab
from include.XYGraphTab import XYGraphTab
from PyQt6.QtCore import QDateTime, QSize, pyqtSlot, QStringListModel
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QToolBar, QFileDialog, QMessageBox

# relative pathing to handle situation when starting the app from different locations
includeDir = path.dirname(__file__)
# print(f"includeDir: {includeDir}")
appBaseDir = path.abspath(path.join(__file__, "../.."))
# print(f"appBaseDir: {appBaseDir}")


def transform_timeDate(utc, timezone=None):
    dateTime_fmt = "yyyy-MM-dd HH:mm:ss"
    newDateTime = QDateTime().fromString(utc, dateTime_fmt)
    if timezone:
        newDateTime.setTimeZone(timezone)
    return newDateTime


class MainWindow(QMainWindow):
    def __init__(self):  # , data, columns):
        super(MainWindow, self).__init__()
        # Read the csvDataSeparator from the INI config file
        self.csvDataSeparator = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "data_separator",
        )

        # Read the filtered_columns from the INI config file
        self.csvHeaders = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "filtered_columns",
        )

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

        # Menu Bar - CSV Menu - Show CSV Raw Data
        self.btnCSVShowRawData = QAction(
            QIcon(path.join(appBaseDir, "icons", "table.ico")),
            "&Show CSV Raw Data",
            self,
        )
        self.btnCSVShowRawData.triggered.connect(self.btnClicked)
        csvMenu.addAction(self.btnCSVShowRawData)  # type: ignore

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
        self.controlTab = ControlPanelTab(self)
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

        # Tab - CSV Raw Data
        self.csvRawDataTab = CSVRawDataTab()  # (self.csvRawData, self.csvHeaders)
        self.csvRawDataTabIdx = self.tabs.addTab(self.csvRawDataTab, "CSV Raw Data")
        self.tabs.setTabIcon(self.csvRawDataTabIdx, QIcon(path.join(appBaseDir, "icons", "table.ico")))

        # Tab - XY Graph
        self.xyGraphTab = XYGraphTab(self)
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
        self.pqDiagramTab = PQDiagramTab(self)
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
                    self.csvRawData = ft.readCSVdata(self.csvFilePath, self.csvDataSeparator, self.csvHeaders)

                    # Set the TableView Data Model and upload the loaded data
                    self.csvRawDataTab.csvRawDataTabSetTableDataModel(self.csvRawData)

                    # Show CSV Raw Data tab
                    self.tabs.setCurrentIndex(self.csvRawDataTabIdx)
                    self.mainStatusBar.showMessage("The CSV file has been loaded")

                else:
                    # A critical message shown
                    QMessageBox.critical(
                        self,
                        "Incorrect Configuration File - Wrong headers",
                        f"The following headers listed in the configuration file were not found in the CSV Data file: \
                            {incorrectHeaders}. Close the application, edit the configuration file and start the \
                            application again.",
                        buttons=QMessageBox.StandardButton.Ok,
                        defaultButton=QMessageBox.StandardButton.Ok,
                    )

        # TODO Finish all button functions
        elif sender == "&Show CSV Raw Data":
            # Show CSV Raw Data tab
            self.tabs.setCurrentIndex(self.csvRawDataTabIdx)

        elif sender == "Show &XY Graph":
            # Show CSV Raw Data tab
            self.tabs.setCurrentIndex(self.xyGraphTabIdx)

        elif sender == "Show &PQ Diagram":
            # Show CSV Raw Data tab
            self.tabs.setCurrentIndex(self.pqDiagramTabIdx)

        elif sender == "Generate Final &Report":
            self.mainStatusBar.showMessage("Generate Final Report button has been pressed")

import os.path as path

from include.ControlPanelTab import ControlPanelTab
from include.CSVRawDataTab import CSVRawDataTab
from include.PQDiagramTab import PQDiagramTab
from include.XYGraphTab import XYGraphTab
from PyQt6.QtCore import QDateTime, QSize, pyqtSlot
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QToolBar

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
    def __init__(self, data, columns):
        super(MainWindow, self).__init__()
        self.csvRawData = data
        self.csvRawDataHeaders = columns

        self.setWindowTitle("The application for data processing of FVE testing")
        self.setWindowIcon(QIcon(path.join(appBaseDir, "icons", "solar-panel.ico")))

        screenGeom = self.screen().availableGeometry()  # type: ignore
        self.setFixedSize(int(screenGeom.width() * 0.5), int(screenGeom.height() * 0.5))
        self.setMinimumSize(QSize(900, 600))
        # self.showMaximized() #Full screen

        # Initialize the Menu Bar
        self.MainWindowMenuInit()

        # Initialize the Toolbar
        self.MainWindowToolbarInit()

        # Initialize the Tabs
        self.MainWindowTabsInit()

        # Initialize the Status Bar
        self.MainWindowStatusBarInit()

        # Initialize the App Shortcuts
        self.MainWindowShortcutsInit()

        self.setCentralWidget(self.tabs)

    def MainWindowMenuInit(self):
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
        self.btnCSVImport = QAction(
            QIcon(path.join(appBaseDir, "icons", "import-csv.ico")),
            "&Import CSV Data",
            self,
        )

        # Menu Bar - CSV Menu - Show CSV Raw Data
        self.btnCSVShowRawData = QAction(
            QIcon(path.join(appBaseDir, "icons", "table.ico")),
            "&Show CSV Raw Data",
            self,
        )
        # TODO
        # self.btnCSVRawData.triggered.connect(
        #     open widget with table of raw data loaded from CSV
        # )
        csvMenu.addAction(self.btnCSVImport)  # type: ignore
        csvMenu.addAction(self.btnCSVShowRawData)  # type: ignore

        graphMenu = self.mainMenuBar.addMenu("&Graph Analysis")  # type: ignore
        self.btnShowCSVDataInGraph = QAction(
            QIcon(path.join(appBaseDir, "icons", "xy-graph.ico")),
            "Show CSV Data in &XY Graph",
            self,
        )
        self.btnShowPQDiagram = QAction(
            QIcon(path.join(appBaseDir, "icons", "pq-diagram.ico")),
            "Show &PQ Diagram",
            self,
        )
        graphMenu.addAction(self.btnShowCSVDataInGraph)  # type: ignore
        graphMenu.addAction(self.btnShowPQDiagram)  # type: ignore

        reportMenu = self.mainMenuBar.addMenu("&Reports")  # type: ignore
        self.btnGenerateFinalReport = QAction("Generate Final Report", self)
        self.btnGenerateFinalReport = QAction(
            QIcon(path.join(appBaseDir, "icons", "printer.ico")),
            "Generate Final &Report",
            self,
        )
        reportMenu.addAction(self.btnGenerateFinalReport)  # type: ignore

    def MainWindowToolbarInit(self):
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

    def MainWindowTabsInit(self):
        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab - Control Panel
        self.controlTab = ControlPanelTab(self)
        controlTabIdx = self.tabs.addTab(self.controlTab, "Control &Panel")
        self.tabs.setTabIcon(
            controlTabIdx,
            QIcon(path.join(appBaseDir, "icons", "control-panel.ico")),
        )

        # Tab - CSV Raw Data
        # TODO Get all header names and insert them into list with checkboxes -> selected will be showed in the table
        # and in 2 combo boxes for XY graph source data (also PQ Diagram?)
        self.csvRawDataTab = CSVRawDataTab(self.csvRawData, self.csvRawDataHeaders)
        csvRawDataTabIdx = self.tabs.addTab(self.csvRawDataTab, "&CSV Raw Data")
        self.tabs.setTabIcon(csvRawDataTabIdx, QIcon(path.join(appBaseDir, "icons", "table.ico")))

        # Tab - XY Graph
        self.xyGraphTab = XYGraphTab(self)
        xyGraphTabIdx = self.tabs.addTab(self.xyGraphTab, "XY &Graph")
        self.tabs.setTabIcon(xyGraphTabIdx, QIcon(path.join(appBaseDir, "icons", "xy-graph.ico")))

        # Tab - PQ Diagram
        self.pqDiagramTab = PQDiagramTab(self)
        pqDiagramTabIdx = self.tabs.addTab(self.pqDiagramTab, "PQ &Diagram")
        self.tabs.setTabIcon(
            pqDiagramTabIdx,
            QIcon(path.join(appBaseDir, "icons", "pq-diagram.ico")),
        )

        self.tabs.setCurrentIndex(controlTabIdx)

    def MainWindowStatusBarInit(self):
        self.mainStatusBar = QStatusBar(self)
        self.setStatusBar(self.mainStatusBar)
        self.mainStatusBar.showMessage("Welcome Operator! Let's load a CSV file.")

    def MainWindowShortcutsInit(self):
        # Print Final Report Shortcut
        self.shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut.activated.connect(self.printReport)

    @pyqtSlot()
    def setToolbarVisibility(self, visibility):
        if visibility:
            self.addToolBar(self.mainToolbar)
            self.mainToolbar.show()
        else:
            self.removeToolBar(self.mainToolbar)

    @pyqtSlot()
    def checkToolbarVisibility(self, visibility):
        if not visibility:
            self.btnShowToolbar.setChecked(False)
        else:
            self.btnShowToolbar.setChecked(True)

    @pyqtSlot()
    def printReport(self):
        self.mainStatusBar.showMessage("Printing!")

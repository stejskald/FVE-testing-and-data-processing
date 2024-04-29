from include.ControlPanelTab import ControlPanelTab
from include.CSVDataTab import CSVDataTab
from include.XYGraphTab import XYGraphTab
from include.PQDiagramTab import PQDiagramTab
from PyQt6.QtCore import QSize, pyqtSlot, QProcess, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QToolBar, QFileDialog, QMessageBox
import dp_app.include.fileTools as ft
from os import path
from datetime import datetime
import pandas as pd
import numpy as np

# relative pathing to handle situation when starting the app from different locations
includeDir = path.dirname(__file__)
# print(f"includeDir: {includeDir}")
appBaseDir = path.abspath(path.join(__file__, "../.."))
# print(f"appBaseDir: {appBaseDir}")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Read settings from configuration file
        self.readConfig()

        self.setWindowTitle("The application for data processing of FVE testing")
        self.setWindowIcon(QIcon(path.join(appBaseDir, "icons", "solar-panel.ico")))

        # Scale Main Window relatively to the Main Display size
        screenGeom = self.screen().availableGeometry()  # type: ignore
        self.setFixedSize(int(screenGeom.width() * 0.8), int(screenGeom.height() * 0.8))
        self.setMinimumSize(QSize(1200, 800))
        # self.showMaximized() #Full screen

        # Initialize the Menu Bar
        self.mWinMenuInit()

        # Initialize the Tabs
        self.mWinTabsInit()

        # Initialize the Toolbar
        self.mWinToolbarInit()

        # Initialize the Status Bar
        self.mWinStatusBarInit()

        # Initialize the App Shortcuts
        # self.mWinShortcutsInit()

        # Initialize the Open CSV Dialog
        self.mWinOpenFileDialogInit()

        # Initialize the Progress Bar
        # self.mWinProgressBarInit() #REVIEW Finish the Progress Bar if needed

        self.processNotepad = None

        self.setCentralWidget(self.tabs)

    def readConfig(self):
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

        # Read the sample_period_s from the INI config file
        self.csv_dt = float(
            ft.iniReadSectionKey(
                path.join(appBaseDir, "appConfig.ini"),
                "app.csv_data",
                "sample_period_s",
            )
        )

        # Read the filtered_columns from the INI config file
        self.csvHeaders = ft.iniReadSectionKeyItems(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "filtered_columns",
        )

        # Read the avg_voltages_ph2ph from the INI config file
        self.avgVoltagesPh2Ph = ft.iniReadSectionKeyItems(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "avg_voltages_ph2ph",
        )

        # Read the avg_u_ph2ph_mean from the INI config file
        self.avgVoltPh2PhMean = ft.iniReadSectionKey(
            path.join(appBaseDir, "appConfig.ini"),
            "app.csv_data",
            "avg_u_ph2ph_mean",
        )

    def mWinMenuInit(self):
        # Menu Bar
        self.mainMenuBar = self.menuBar()

        # Menu Bar - File Menu
        self.fileMenu = self.mainMenuBar.addMenu("&File")  # type: ignore
        self.btnOpenConfigFile = QAction(
            QIcon(path.join(appBaseDir, "icons", "settings.ico")),
            "Open App &Config File",
            self,
        )
        self.btnOpenConfigFile.setShortcut(QKeySequence("Ctrl+I"))
        self.btnOpenConfigFile.setStatusTip("Push to open the application configuration file.")
        self.btnOpenConfigFile.triggered.connect(self.openNotepad)  # type: ignore
        self.fileMenu.addAction(self.btnOpenConfigFile)  # type: ignore

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
        self.btnGenerateFinalReport.setShortcut(QKeySequence("Ctrl+P"))
        self.btnGenerateFinalReport.triggered.connect(self.btnClicked)
        reportMenu.addAction(self.btnGenerateFinalReport)  # type: ignore

    def mWinToolbarInit(self):
        self.mainToolbar = QToolBar("Toolbar")
        self.mainToolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.mainToolbar)
        self.mainToolbar.hide()  # Hide as default

        self.mainToolbar.visibilityChanged.connect(self.checkToolbarVisibility)

        self.mainToolbar.addAction(self.btnOpenConfigFile)
        self.mainToolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.mainToolbar.addSeparator()
        self.mainToolbar.addAction(self.btnImportCSV)
        self.mainToolbar.addSeparator()
        self.mainToolbar.addAction(self.btnGenerateFinalReport)

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

        # Tab - PQ Diagram
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
        self.mainStatusBar.showMessage("Welcome Operator! Let's load a CSV file.")

    def mWinOpenFileDialogInit(self):
        self.openFileDialog = QFileDialog(self)
        self.openFileDialog.setWindowTitle("Open a CSV file with the data")
        self.openFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.openFileDialog.setNameFilter("CSV Files (*.csv)")
        self.openFileDialog.setViewMode(QFileDialog.ViewMode.Detail)
        self.openFileDialog.setDirectory(path.join(appBaseDir, "data"))

    def mWinShortcutsInit(self):
        # Print Final Report Shortcut - without a need of initializing the button
        self.shortcutPrint = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutPrint.activated.connect(self.printReport)

    # REVIEW Finish the Progress Bar if needed
    # def mWinProgressBarInit(self):
    #     self.progressBar = QProgressBar(self)
    #     self.progressBar.setGeometry(180, 200, 250, 20)
    #     self.controlTab.btnImportCSV.clicked.connect(self.updateProgressBar)
    #     self.progressBar.hide()

    @pyqtSlot()
    def openNotepad(self):
        if self.processNotepad is None:  # No process running.
            self.processNotepad = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running
            self.processNotepad.finished.connect(self.processNotepadFinished)  # Clean up once complete.
            self.processNotepad.start("Notepad", [path.join(appBaseDir, "appConfig.ini")])
            self.mainStatusBar.showMessage("The configuration file has been opened.")

    @pyqtSlot()
    def processNotepadFinished(self):
        self.processNotepad = None
        self.mainStatusBar.showMessage("The configuration file has been closed.")

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
        self.mainStatusBar.showMessage("Printing called...")

    @pyqtSlot()
    def btnClicked(self):
        sender = self.sender().text()  # type: ignore

        if sender == "&Import CSV Data":  # or btn from CSV Menu
            self.importCSVdata()

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
            self.mainStatusBar.showMessage("The Generate Final Report button has been pressed.")
            self.printReport()

    def importCSVdata(self):
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
                # An informative message shown # REVIEW Uncomment to show a MessageBox
                # QMessageBox.information(
                #     self,
                #     "Informative - CSV loading time",
                #     "The file is loading, please wait, it may take a few minutes if the file is too large "
                #     + "(10 MB takes about 40 sec).",
                #     buttons=QMessageBox.StandardButton.Ok,
                #     defaultButton=QMessageBox.StandardButton.Ok,
                # )

                # self.mainStatusBar.showMessage(
                #     "The file is loading, please wait, it may take a few minutes if the file is too large "
                #     + "(10MB takes about 40 sec)."
                # )

                # self.progressBar.show()

                # Read data from CSV file
                self.csvData = ft.readCSVdata(self.csvFilePath, self.csvDataSeparator, self.csvHeaders)

                # REVIEW Progress bar -----------------------------
                # from tqdm import tqdm

                # LINES_TO_READ_FOR_EST = 20
                # CHUNK_SIZE_PER_ITER = 10**5

                # temp = pd.read_csv(self.csvFilePath, nrows=LINES_TO_READ_FOR_EST)
                # N = len(temp.to_csv(index=False))
                # df = [temp[:0]]
                # t = int(path.getsize(self.csvFilePath) / N * LINES_TO_READ_FOR_EST / CHUNK_SIZE_PER_ITER) + 1

                # with tqdm(total=t, file=sys.stdout) as pbar:
                #     for i, chunk in enumerate(
                #         pd.read_csv(self.csvFilePath, chunksize=CHUNK_SIZE_PER_ITER, low_memory=False)
                #     ):
                #         df.append(chunk)
                #         pbar.set_description("Importing: %d" % (1 + i))
                #         pbar.update(1)

                # data = temp[:0].append(df)
                # del df
                # ----------------------------------------------------------

                # Adjust the DateTime column to have info about milliseconds and the time zone
                # e.g.: "2023-08-31 11:15:24" -> "2023-08-31 11:15:24.200000 +0200"
                self.adjustDateTimeColumn()

                # Adjust the data in the 3Cosφ[] column "C -0.18" -> float(-0.18)
                self.adjust3CosPhiColumn()

                # Mean of 3 Ph2Ph Voltages columns
                self.makeMeanOfPh2PhAvgVoltages()

                # Set the TableView Data Model and upload the loaded data
                self.csvDataTab.setTableDataModel(self.csvData)

                # Show info about CSV file was loaded
                self.mainStatusBar.showMessage("The CSV file has been loaded.")

                # Set the TableView Data Model and upload the loaded data
                self.xyGraphTab.setComboBoxesDataModel(self.csvData.columns.to_list())

                # Load CSV data to the xyGraphTab ans set the date
                self.xyGraphTab.loadData(self.csvData)
                self.xyGraphTab.setMeasurementDate(self.measDate)

                # Load CSV data to the pqDiagramTab ans set the date
                self.pqDiagramTab.loadData(self.csvData)
                self.pqDiagramTab.setMeasurementDate(self.measDate)

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

    def adjustDateTimeColumn(self):
        # Find name of the first column with "Time"
        self.timeColName = [col for col in self.csvData.columns if "Time" in col][0]
        # Get str values in list
        timeValues = self.csvData[self.timeColName].tolist()

        # Check if the time starts at the whole second
        runCount = int(1 / self.csv_dt)  # run count per each second (5 times if dt is 0.2 sec)
        pt2Secs = []
        for dateTimeStr in timeValues[:runCount]:
            pt = datetime.strptime(dateTimeStr, self.csvDateTimeFmt)  # parsed datetime
            pt2Secs.append(pt.second + pt.minute * 60 + pt.hour * 3600)
        # Detect differences in the time (list pt2Secs)
        timeDiffs = list(np.array(pt2Secs[:-1]) - np.array(pt2Secs[1:]))

        # Adding .00 .20 .40 .60 .80 (mSec) and timezone (UTC+2) to the time data
        timeColIdx = self.csvData.columns.get_loc(self.timeColName)
        runIter = runCount - (timeDiffs.index(-1) + 1)  # Initial multiplier (for time not starting at the whole second)
        # prevIdx = 0
        for idx, row in self.csvData.iterrows():  # Iterate over rows
            # prevIdx = idx
            self.csvData.iat[self.csvData.index.get_loc(idx), timeColIdx] = (
                row[self.timeColName] + f"{runIter*self.csv_dt:.3f}"[1:] + " +0200"
            )
            runIter += 1
            if runIter == runCount:
                runIter = 0

                # TODO Add checking if there are more rows for a second than "runCount"
                # dtStrActRow = self.csvData.iat[self.csvData.index.get_loc(idx), timeColIdx]
                # ptActRow = datetime.strptime(dtStrActRow, "%Y-%m-%d %H:%M:%S.%f %z")  # parsed datetime
                # pt2SecsActRow = ptActRow.second
                # dtStrPrevRow = self.csvData.iat[self.csvData.index.get_loc(idx), timeColIdx]
                # ptPrevRow = datetime.strptime(dtStrPrevRow, self.csvDateTimeFmt)  # parsed datetime
                # pt2SecsPrevRow = ptPrevRow.second

                # # Here check if the second val of the following row is same -> then remove the following row!
                # if pt2SecsPrevRow == pt2SecsActRow:
                #     print(ptPrevRow)
                #     print(dtStrActRow)
                #     # self.csvData.drop(row)

        # Convert Pandas column of datetime strings to DateTimes
        self.csvData[self.timeColName] = pd.to_datetime(
            self.csvData[self.timeColName], format="%Y-%m-%d %H:%M:%S.%f %z", errors="coerce"
        )

        # # Get date from the first element in the DateTime column as string
        self.measDate = str(self.csvData[self.timeColName].dt.date[0])

    def adjust3CosPhiColumn(self):
        # Find and select only first column with "3Cos"
        cosPhiColName = [col for col in self.csvData.columns if "3Cos" in col][0]
        # Update values in cosPhiColName column with trimming the "C"/"L" part and converting to float64
        self.csvData[cosPhiColName] = self.csvData[cosPhiColName].str.split(" ").str[1]
        self.csvData[cosPhiColName] = pd.to_numeric(self.csvData[cosPhiColName], errors="coerce")

    def makeMeanOfPh2PhAvgVoltages(self):
        # Average for each row in Avg Voltage Ph2Ph columns
        AvgU_Ph2Ph = np.array(self.csvData[self.avgVoltagesPh2Ph]).mean(axis=1)
        # Delete these 3 columns in the DataFrame
        self.csvData = self.csvData.drop(self.avgVoltagesPh2Ph, axis=1)
        # Add a new column as the 1st
        self.csvData.insert(1, self.avgVoltPh2PhMean, AvgU_Ph2Ph, True)

    # @pyqtSlot()
    # def updateProgressBar(self):
    #     self.completed = 0

    #     while self.completed < 100:
    #         self.completed += 0.0001
    #         self.progressBar.setValue(int(self.completed))
    #     self.progressBar.hide()

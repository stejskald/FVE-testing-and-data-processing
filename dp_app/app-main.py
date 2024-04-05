import os
import sys

from PyQt6.QtCore import QCoreApplication, QSize
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStatusBar, QTabWidget,
                             QToolBar)

from dp_app.include.ControlTab import ControlTab

# relative pathing to handle situation when starting the app from different locations
baseDir = os.path.dirname(__file__)

# Allows to assign icon to the app
try:
    from ctypes import windll

    myappid = "cz.vut.FVE-testing.1-0-0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("The Application for data processing of FVE testing")
        self.setWindowIcon(QIcon(os.path.join(baseDir, "icons", "pcb.png")))
        self.setMinimumSize(QSize(1200, 900))
        self.showMaximized()

        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        btnBugAction = QAction(
            QIcon(os.path.join(baseDir, "icons", "bug.png")),
            "&Bug simulation",
            self,
        )
        btnBugAction.setStatusTip("Simulate a Bug.")
        btnBugAction.setCheckable(True)
        self.toolbar.addAction(btnBugAction)
        btnBugAction.setShortcut(QKeySequence("Ctrl+b"))
        self.toolbar.addSeparator()

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileSubmenu = fileMenu.addMenu("&Submenu")
        fileSubmenu.addAction(btnBugAction)
        btnExitApplication = QAction(
            QIcon(os.path.join(baseDir, "icons", "cross.png")),
            "E&xit Application",
            self,
        )
        btnExitApplication.setStatusTip("Push to exit the Application.")
        btnExitApplication.triggered.connect(QCoreApplication.instance().quit)
        fileMenu.addAction(btnExitApplication)

        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(btnBugAction)

        viewMenu = menuBar.addMenu("&View")
        self.btnShowMainToolbar = QAction("Show Main Toolbar", self)
        self.btnShowMainToolbar.setStatusTip("Push to show the Main Toolbar.")
        self.btnShowMainToolbar.triggered.connect(
            self.setMainToolbarVisibility
        )
        self.toolbar.visibilityChanged.connect(self.checkMainToolbarVisibility)
        self.btnShowMainToolbar.setCheckable(True)
        self.btnShowMainToolbar.setChecked(True)
        viewMenu.addAction(self.btnShowMainToolbar)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        self.controlTab = ControlTab(self)
        controlTabIdx = tabs.addTab(self.controlTab, "Control Panel")

        tabs.setCurrentIndex(controlTabIdx)  # DEBUG
        self.setCentralWidget(tabs)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def setMainToolbarVisibility(self, visibility):
        if visibility:
            self.addToolBar(self.toolbar)
            self.toolbar.show()
        else:
            self.removeToolBar(self.toolbar)

    def checkMainToolbarVisibility(self, visibility):
        if not visibility:
            self.btnShowMainToolbar.setChecked(False)

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("VUT")
    app.setApplicationName("Application-for-data-processing-of-FVE")

    # appDataLoc = QStandardPaths.standardLocations(
    #     QStandardPaths.StandardLocation.AppDataLocation
    # )[0]
    # appConfigLoc = QStandardPaths.standardLocations(
    #     QStandardPaths.StandardLocation.AppConfigLocation
    # )[0]
    # print(appDataLoc)
    # print(appConfigLoc)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
import sys

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
    app = QApplication(sys.argv)
    app.setOrganizationName("VUT")
    app.setApplicationName("Application-for-data-processing-of-FVE")

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\CSVDataTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CSVDataTab(object):
    def setupUi(self, CSVDataTab):
        CSVDataTab.setObjectName("CSVDataTab")
        CSVDataTab.resize(573, 423)
        self.verticalLayout = QtWidgets.QVBoxLayout(CSVDataTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(parent=CSVDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(CSVDataTab)
        QtCore.QMetaObject.connectSlotsByName(CSVDataTab)

    def retranslateUi(self, CSVDataTab):
        _translate = QtCore.QCoreApplication.translate
        CSVDataTab.setWindowTitle(_translate("CSVDataTab", "Form"))

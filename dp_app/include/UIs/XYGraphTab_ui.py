# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\XYGraphTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_XYGraphTab(object):
    def setupUi(self, XYGraphTab):
        XYGraphTab.setObjectName("XYGraphTab")
        XYGraphTab.resize(765, 543)
        self.verticalLayout = QtWidgets.QVBoxLayout(XYGraphTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.gLayout = QtWidgets.QGridLayout()
        self.gLayout.setObjectName("gLayout")
        self.labelXdata = QtWidgets.QLabel(parent=XYGraphTab)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelXdata.setFont(font)
        self.labelXdata.setObjectName("labelXdata")
        self.gLayout.addWidget(self.labelXdata, 0, 1, 1, 1)
        self.labelYdata = QtWidgets.QLabel(parent=XYGraphTab)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelYdata.setFont(font)
        self.labelYdata.setObjectName("labelYdata")
        self.gLayout.addWidget(self.labelYdata, 1, 1, 1, 1)
        self.comboBoxXData = QtWidgets.QComboBox(parent=XYGraphTab)
        self.comboBoxXData.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBoxXData.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBoxXData.setObjectName("comboBoxXData")
        self.gLayout.addWidget(self.comboBoxXData, 0, 2, 1, 1)
        self.comboBoxYData = QtWidgets.QComboBox(parent=XYGraphTab)
        self.comboBoxYData.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBoxYData.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBoxYData.setObjectName("comboBoxYData")
        self.gLayout.addWidget(self.comboBoxYData, 1, 2, 1, 1)
        self.hLayout.addLayout(self.gLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.hLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.XYGraph = PlotWidget(parent=XYGraphTab)
        self.XYGraph.setMinimumSize(QtCore.QSize(0, 400))
        self.XYGraph.setMaximumSize(QtCore.QSize(16777215, 500))
        self.XYGraph.setObjectName("XYGraph")
        self.verticalLayout.addWidget(self.XYGraph)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(XYGraphTab)
        QtCore.QMetaObject.connectSlotsByName(XYGraphTab)

    def retranslateUi(self, XYGraphTab):
        _translate = QtCore.QCoreApplication.translate
        XYGraphTab.setWindowTitle(_translate("XYGraphTab", "Form"))
        self.labelXdata.setText(_translate("XYGraphTab", "Data on X axis:"))
        self.labelYdata.setText(_translate("XYGraphTab", "Data on X axis:"))
from pyqtgraph import PlotWidget
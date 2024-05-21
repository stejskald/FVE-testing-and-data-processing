# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\GradientTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GradientTab(object):
    def setupUi(self, GradientTab):
        GradientTab.setObjectName("GradientTab")
        GradientTab.resize(1000, 950)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GradientTab.sizePolicy().hasHeightForWidth())
        GradientTab.setSizePolicy(sizePolicy)
        GradientTab.setMinimumSize(QtCore.QSize(500, 900))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(GradientTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.setObjectName("vLayout")
        self.hLayoutTop = QtWidgets.QHBoxLayout()
        self.hLayoutTop.setSpacing(6)
        self.hLayoutTop.setObjectName("hLayoutTop")
        self.vLayoutButtons = QtWidgets.QVBoxLayout()
        self.vLayoutButtons.setContentsMargins(-1, -1, 20, -1)
        self.vLayoutButtons.setObjectName("vLayoutButtons")
        self.btnTest = QtWidgets.QPushButton(parent=GradientTab)
        self.btnTest.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnTest.setCheckable(True)
        self.btnTest.setObjectName("btnTest")
        self.vLayoutButtons.addWidget(self.btnTest)
        self.btnCancelLastSeq = QtWidgets.QPushButton(parent=GradientTab)
        self.btnCancelLastSeq.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnCancelLastSeq.setCheckable(False)
        self.btnCancelLastSeq.setObjectName("btnCancelLastSeq")
        self.vLayoutButtons.addWidget(self.btnCancelLastSeq)
        self.hLayoutTop.addLayout(self.vLayoutButtons)
        self.textTestInfo = QtWidgets.QPlainTextEdit(parent=GradientTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textTestInfo.sizePolicy().hasHeightForWidth())
        self.textTestInfo.setSizePolicy(sizePolicy)
        self.textTestInfo.setMinimumSize(QtCore.QSize(125, 24))
        self.textTestInfo.setMaximumSize(QtCore.QSize(200, 56))
        self.textTestInfo.setUndoRedoEnabled(False)
        self.textTestInfo.setReadOnly(True)
        self.textTestInfo.setPlainText("")
        self.textTestInfo.setObjectName("textTestInfo")
        self.hLayoutTop.addWidget(self.textTestInfo)
        self.gridLayoutTop = QtWidgets.QGridLayout()
        self.gridLayoutTop.setContentsMargins(20, -1, -1, -1)
        self.gridLayoutTop.setHorizontalSpacing(6)
        self.gridLayoutTop.setObjectName("gridLayoutTop")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem1, 0, 3, 1, 1)
        self.labelGradient = QtWidgets.QLabel(parent=GradientTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelGradient.sizePolicy().hasHeightForWidth())
        self.labelGradient.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelGradient.setFont(font)
        self.labelGradient.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelGradient.setObjectName("labelGradient")
        self.gridLayoutTop.addWidget(self.labelGradient, 0, 0, 1, 1)
        self.labelGradientVal = QtWidgets.QLabel(parent=GradientTab)
        self.labelGradientVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelGradientVal.setObjectName("labelGradientVal")
        self.gridLayoutTop.addWidget(self.labelGradientVal, 0, 2, 1, 1)
        self.cBoxPlots = QtWidgets.QComboBox(parent=GradientTab)
        self.cBoxPlots.setMinimumSize(QtCore.QSize(110, 0))
        self.cBoxPlots.setObjectName("cBoxPlots")
        self.gridLayoutTop.addWidget(self.cBoxPlots, 0, 5, 1, 1)
        self.labelSelectedPlot = QtWidgets.QLabel(parent=GradientTab)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelSelectedPlot.setFont(font)
        self.labelSelectedPlot.setObjectName("labelSelectedPlot")
        self.gridLayoutTop.addWidget(self.labelSelectedPlot, 0, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem2, 0, 6, 1, 1)
        self.hLayoutTop.addLayout(self.gridLayoutTop)
        self.vLayout.addLayout(self.hLayoutTop)
        self.vLayoutPlotsTable = QtWidgets.QVBoxLayout()
        self.vLayoutPlotsTable.setSpacing(12)
        self.vLayoutPlotsTable.setObjectName("vLayoutPlotsTable")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelMeasDate = QtWidgets.QLabel(parent=GradientTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMeasDate.sizePolicy().hasHeightForWidth())
        self.labelMeasDate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelMeasDate.setFont(font)
        self.labelMeasDate.setObjectName("labelMeasDate")
        self.gridLayout.addWidget(self.labelMeasDate, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(37, 18, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 3, 1, 1)
        self.labelMeasDateValue = QtWidgets.QLabel(parent=GradientTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMeasDateValue.sizePolicy().hasHeightForWidth())
        self.labelMeasDateValue.setSizePolicy(sizePolicy)
        self.labelMeasDateValue.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setBold(False)
        self.labelMeasDateValue.setFont(font)
        self.labelMeasDateValue.setText("")
        self.labelMeasDateValue.setObjectName("labelMeasDateValue")
        self.gridLayout.addWidget(self.labelMeasDateValue, 0, 1, 1, 1)
        self.vLayoutPlotsTable.addLayout(self.gridLayout)
        self.vLayoutPlots = QtWidgets.QVBoxLayout()
        self.vLayoutPlots.setSpacing(6)
        self.vLayoutPlots.setObjectName("vLayoutPlots")
        self.plot0 = PlotWidget(parent=GradientTab)
        self.plot0.setMinimumSize(QtCore.QSize(500, 150))
        self.plot0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot0.setObjectName("plot0")
        self.vLayoutPlots.addWidget(self.plot0)
        self.plot1 = PlotWidget(parent=GradientTab)
        self.plot1.setMinimumSize(QtCore.QSize(500, 150))
        self.plot1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot1.setObjectName("plot1")
        self.vLayoutPlots.addWidget(self.plot1)
        self.vLayoutPlotsTable.addLayout(self.vLayoutPlots)
        self.hLayoutTable = QtWidgets.QHBoxLayout()
        self.hLayoutTable.setObjectName("hLayoutTable")
        self.tableView = QtWidgets.QTableView(parent=GradientTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(800, 350))
        self.tableView.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        self.hLayoutTable.addWidget(self.tableView)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayoutTable.addItem(spacerItem4)
        self.hLayoutTable.setStretch(1, 1)
        self.vLayoutPlotsTable.addLayout(self.hLayoutTable)
        self.vLayoutPlotsTable.setStretch(1, 1)
        self.vLayout.addLayout(self.vLayoutPlotsTable)
        self.verticalLayout_2.addLayout(self.vLayout)

        self.retranslateUi(GradientTab)
        QtCore.QMetaObject.connectSlotsByName(GradientTab)
        GradientTab.setTabOrder(self.btnTest, self.btnCancelLastSeq)
        GradientTab.setTabOrder(self.btnCancelLastSeq, self.textTestInfo)
        GradientTab.setTabOrder(self.textTestInfo, self.plot0)
        GradientTab.setTabOrder(self.plot0, self.plot1)

    def retranslateUi(self, GradientTab):
        _translate = QtCore.QCoreApplication.translate
        GradientTab.setWindowTitle(_translate("GradientTab", "Form"))
        self.btnTest.setText(_translate("GradientTab", "Start gradient test"))
        self.btnCancelLastSeq.setText(_translate("GradientTab", "Cancel last sequence"))
        self.labelGradient.setToolTip(_translate("GradientTab", "The gradient represents the slope with which the process variable rises to the setpoint."))
        self.labelGradient.setText(_translate("GradientTab", "Gradient:"))
        self.labelGradientVal.setText(_translate("GradientTab", "?"))
        self.labelSelectedPlot.setToolTip(_translate("GradientTab", "Select the plot you want to click in."))
        self.labelSelectedPlot.setText(_translate("GradientTab", "Selected plot:"))
        self.labelMeasDate.setText(_translate("GradientTab", "Measurement date:"))
from pyqtgraph import PlotWidget

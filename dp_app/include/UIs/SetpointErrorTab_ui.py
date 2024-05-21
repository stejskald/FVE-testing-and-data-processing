# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\SetpointErrorTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SetpointErrorTab(object):
    def setupUi(self, SetpointErrorTab):
        SetpointErrorTab.setObjectName("SetpointErrorTab")
        SetpointErrorTab.resize(1000, 950)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SetpointErrorTab.sizePolicy().hasHeightForWidth())
        SetpointErrorTab.setSizePolicy(sizePolicy)
        SetpointErrorTab.setMinimumSize(QtCore.QSize(500, 900))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SetpointErrorTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.setObjectName("vLayout")
        self.hLayoutTop = QtWidgets.QHBoxLayout()
        self.hLayoutTop.setSpacing(6)
        self.hLayoutTop.setObjectName("hLayoutTop")
        self.vLayoutButtons = QtWidgets.QVBoxLayout()
        self.vLayoutButtons.setContentsMargins(-1, -1, 20, -1)
        self.vLayoutButtons.setObjectName("vLayoutButtons")
        self.btnTest = QtWidgets.QPushButton(parent=SetpointErrorTab)
        self.btnTest.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnTest.setCheckable(True)
        self.btnTest.setObjectName("btnTest")
        self.vLayoutButtons.addWidget(self.btnTest)
        self.btnCancelLastPt = QtWidgets.QPushButton(parent=SetpointErrorTab)
        self.btnCancelLastPt.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnCancelLastPt.setCheckable(False)
        self.btnCancelLastPt.setObjectName("btnCancelLastPt")
        self.vLayoutButtons.addWidget(self.btnCancelLastPt)
        self.hLayoutTop.addLayout(self.vLayoutButtons)
        self.textTestInfo = QtWidgets.QPlainTextEdit(parent=SetpointErrorTab)
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
        self.labelPowerSetpoint = QtWidgets.QLabel(parent=SetpointErrorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPowerSetpoint.sizePolicy().hasHeightForWidth())
        self.labelPowerSetpoint.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelPowerSetpoint.setFont(font)
        self.labelPowerSetpoint.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelPowerSetpoint.setObjectName("labelPowerSetpoint")
        self.gridLayoutTop.addWidget(self.labelPowerSetpoint, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem, 0, 2, 1, 1)
        self.labelPwrSetpointErr = QtWidgets.QLabel(parent=SetpointErrorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPwrSetpointErr.sizePolicy().hasHeightForWidth())
        self.labelPwrSetpointErr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelPwrSetpointErr.setFont(font)
        self.labelPwrSetpointErr.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelPwrSetpointErr.setObjectName("labelPwrSetpointErr")
        self.gridLayoutTop.addWidget(self.labelPwrSetpointErr, 0, 3, 1, 1)
        self.dblSpinBoxPwrSetpoint = QtWidgets.QDoubleSpinBox(parent=SetpointErrorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dblSpinBoxPwrSetpoint.sizePolicy().hasHeightForWidth())
        self.dblSpinBoxPwrSetpoint.setSizePolicy(sizePolicy)
        self.dblSpinBoxPwrSetpoint.setMinimumSize(QtCore.QSize(0, 0))
        self.dblSpinBoxPwrSetpoint.setMaximumSize(QtCore.QSize(125, 16777215))
        self.dblSpinBoxPwrSetpoint.setDecimals(3)
        self.dblSpinBoxPwrSetpoint.setMaximum(1000000.0)
        self.dblSpinBoxPwrSetpoint.setProperty("value", 1200.0)
        self.dblSpinBoxPwrSetpoint.setObjectName("dblSpinBoxPwrSetpoint")
        self.gridLayoutTop.addWidget(self.dblSpinBoxPwrSetpoint, 0, 1, 1, 1)
        self.dblSpinBoxCosPhiSetpoint = QtWidgets.QDoubleSpinBox(parent=SetpointErrorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dblSpinBoxCosPhiSetpoint.sizePolicy().hasHeightForWidth())
        self.dblSpinBoxCosPhiSetpoint.setSizePolicy(sizePolicy)
        self.dblSpinBoxCosPhiSetpoint.setMinimumSize(QtCore.QSize(0, 0))
        self.dblSpinBoxCosPhiSetpoint.setMaximumSize(QtCore.QSize(125, 16777215))
        self.dblSpinBoxCosPhiSetpoint.setDecimals(2)
        self.dblSpinBoxCosPhiSetpoint.setMinimum(-1.0)
        self.dblSpinBoxCosPhiSetpoint.setMaximum(1.0)
        self.dblSpinBoxCosPhiSetpoint.setSingleStep(0.01)
        self.dblSpinBoxCosPhiSetpoint.setProperty("value", 0.8)
        self.dblSpinBoxCosPhiSetpoint.setObjectName("dblSpinBoxCosPhiSetpoint")
        self.gridLayoutTop.addWidget(self.dblSpinBoxCosPhiSetpoint, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem1, 0, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem2, 1, 5, 1, 1)
        self.labelPwrSetpointErrVal = QtWidgets.QLabel(parent=SetpointErrorTab)
        self.labelPwrSetpointErrVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelPwrSetpointErrVal.setObjectName("labelPwrSetpointErrVal")
        self.gridLayoutTop.addWidget(self.labelPwrSetpointErrVal, 0, 4, 1, 1)
        self.labelCosPhiSetpoint = QtWidgets.QLabel(parent=SetpointErrorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCosPhiSetpoint.sizePolicy().hasHeightForWidth())
        self.labelCosPhiSetpoint.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelCosPhiSetpoint.setFont(font)
        self.labelCosPhiSetpoint.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelCosPhiSetpoint.setObjectName("labelCosPhiSetpoint")
        self.gridLayoutTop.addWidget(self.labelCosPhiSetpoint, 1, 0, 1, 1)
        self.labelCosPhiSetpointErrVal = QtWidgets.QLabel(parent=SetpointErrorTab)
        self.labelCosPhiSetpointErrVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelCosPhiSetpointErrVal.setObjectName("labelCosPhiSetpointErrVal")
        self.gridLayoutTop.addWidget(self.labelCosPhiSetpointErrVal, 1, 4, 1, 1)
        self.labelSelectedPlot = QtWidgets.QLabel(parent=SetpointErrorTab)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelSelectedPlot.setFont(font)
        self.labelSelectedPlot.setObjectName("labelSelectedPlot")
        self.gridLayoutTop.addWidget(self.labelSelectedPlot, 0, 6, 1, 1)
        self.cBoxPlots = QtWidgets.QComboBox(parent=SetpointErrorTab)
        self.cBoxPlots.setMinimumSize(QtCore.QSize(110, 0))
        self.cBoxPlots.setObjectName("cBoxPlots")
        self.gridLayoutTop.addWidget(self.cBoxPlots, 0, 7, 1, 1)
        self.labelCosPhiSetpointErr = QtWidgets.QLabel(parent=SetpointErrorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCosPhiSetpointErr.sizePolicy().hasHeightForWidth())
        self.labelCosPhiSetpointErr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelCosPhiSetpointErr.setFont(font)
        self.labelCosPhiSetpointErr.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelCosPhiSetpointErr.setObjectName("labelCosPhiSetpointErr")
        self.gridLayoutTop.addWidget(self.labelCosPhiSetpointErr, 1, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem3, 0, 8, 1, 1)
        self.hLayoutTop.addLayout(self.gridLayoutTop)
        self.vLayout.addLayout(self.hLayoutTop)
        self.vLayoutPlotsTable = QtWidgets.QVBoxLayout()
        self.vLayoutPlotsTable.setSpacing(12)
        self.vLayoutPlotsTable.setObjectName("vLayoutPlotsTable")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelMeasDate = QtWidgets.QLabel(parent=SetpointErrorTab)
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
        spacerItem4 = QtWidgets.QSpacerItem(37, 18, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 3, 1, 1)
        self.labelMeasDateValue = QtWidgets.QLabel(parent=SetpointErrorTab)
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
        self.plot0 = PlotWidget(parent=SetpointErrorTab)
        self.plot0.setMinimumSize(QtCore.QSize(500, 150))
        self.plot0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot0.setObjectName("plot0")
        self.vLayoutPlots.addWidget(self.plot0)
        self.plot1 = PlotWidget(parent=SetpointErrorTab)
        self.plot1.setMinimumSize(QtCore.QSize(500, 150))
        self.plot1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot1.setObjectName("plot1")
        self.vLayoutPlots.addWidget(self.plot1)
        self.plot2 = PlotWidget(parent=SetpointErrorTab)
        self.plot2.setMinimumSize(QtCore.QSize(500, 150))
        self.plot2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot2.setObjectName("plot2")
        self.vLayoutPlots.addWidget(self.plot2)
        self.vLayoutPlotsTable.addLayout(self.vLayoutPlots)
        self.hLayoutTable = QtWidgets.QHBoxLayout()
        self.hLayoutTable.setObjectName("hLayoutTable")
        self.tableView = QtWidgets.QTableView(parent=SetpointErrorTab)
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
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayoutTable.addItem(spacerItem5)
        self.hLayoutTable.setStretch(1, 1)
        self.vLayoutPlotsTable.addLayout(self.hLayoutTable)
        self.vLayoutPlotsTable.setStretch(1, 1)
        self.vLayout.addLayout(self.vLayoutPlotsTable)
        self.verticalLayout_2.addLayout(self.vLayout)

        self.retranslateUi(SetpointErrorTab)
        QtCore.QMetaObject.connectSlotsByName(SetpointErrorTab)
        SetpointErrorTab.setTabOrder(self.btnTest, self.btnCancelLastPt)
        SetpointErrorTab.setTabOrder(self.btnCancelLastPt, self.textTestInfo)
        SetpointErrorTab.setTabOrder(self.textTestInfo, self.dblSpinBoxPwrSetpoint)
        SetpointErrorTab.setTabOrder(self.dblSpinBoxPwrSetpoint, self.dblSpinBoxCosPhiSetpoint)
        SetpointErrorTab.setTabOrder(self.dblSpinBoxCosPhiSetpoint, self.plot0)
        SetpointErrorTab.setTabOrder(self.plot0, self.plot1)
        SetpointErrorTab.setTabOrder(self.plot1, self.plot2)

    def retranslateUi(self, SetpointErrorTab):
        _translate = QtCore.QCoreApplication.translate
        SetpointErrorTab.setWindowTitle(_translate("SetpointErrorTab", "Form"))
        self.btnTest.setText(_translate("SetpointErrorTab", "Start setpoint error test"))
        self.btnCancelLastPt.setText(_translate("SetpointErrorTab", "Cancel last point"))
        self.labelPowerSetpoint.setToolTip(_translate("SetpointErrorTab", "<html><head/><body><p>A setpoint is the desired value of a process variable. The power type (P/Q) is determined by the data on the Y1 axis.</p></body></html>"))
        self.labelPowerSetpoint.setText(_translate("SetpointErrorTab", "Power setpoint:"))
        self.labelPwrSetpointErr.setToolTip(_translate("SetpointErrorTab", "A realtive error to the setpoint value."))
        self.labelPwrSetpointErr.setText(_translate("SetpointErrorTab", "Power setpoint error:"))
        self.dblSpinBoxPwrSetpoint.setSuffix(_translate("SetpointErrorTab", " (kW/kvar)"))
        self.labelPwrSetpointErrVal.setText(_translate("SetpointErrorTab", "?"))
        self.labelCosPhiSetpoint.setToolTip(_translate("SetpointErrorTab", "<html><head/><body><p>A setpoint is the desired value of a process variable. The power type (P/Q) is determined by the data on the Y1 axis.</p></body></html>"))
        self.labelCosPhiSetpoint.setText(_translate("SetpointErrorTab", "cos(φ) setpoint:"))
        self.labelCosPhiSetpointErrVal.setText(_translate("SetpointErrorTab", "?"))
        self.labelSelectedPlot.setToolTip(_translate("SetpointErrorTab", "Select the plot you want to click in."))
        self.labelSelectedPlot.setText(_translate("SetpointErrorTab", "Selected plot:"))
        self.labelCosPhiSetpointErr.setToolTip(_translate("SetpointErrorTab", "A realtive error to the setpoint value."))
        self.labelCosPhiSetpointErr.setText(_translate("SetpointErrorTab", "cos(φ) setpoint error:"))
        self.labelMeasDate.setText(_translate("SetpointErrorTab", "Measurement date:"))
from pyqtgraph import PlotWidget
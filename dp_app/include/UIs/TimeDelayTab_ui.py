# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\TimeDelayTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TimeDelayTab(object):
    def setupUi(self, TimeDelayTab):
        TimeDelayTab.setObjectName("TimeDelayTab")
        TimeDelayTab.resize(1000, 950)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TimeDelayTab.sizePolicy().hasHeightForWidth())
        TimeDelayTab.setSizePolicy(sizePolicy)
        TimeDelayTab.setMinimumSize(QtCore.QSize(500, 900))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(TimeDelayTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(parent=TimeDelayTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 900))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 963, 1101))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(1, 1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLayoutTop = QtWidgets.QHBoxLayout()
        self.hLayoutTop.setObjectName("hLayoutTop")
        self.vLayoutButtons = QtWidgets.QVBoxLayout()
        self.vLayoutButtons.setContentsMargins(-1, -1, 20, -1)
        self.vLayoutButtons.setObjectName("vLayoutButtons")
        self.btnTest = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.btnTest.setMinimumSize(QtCore.QSize(0, 24))
        self.btnTest.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnTest.setCheckable(True)
        self.btnTest.setObjectName("btnTest")
        self.vLayoutButtons.addWidget(self.btnTest)
        self.btnCancelLastSeq = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
        self.btnCancelLastSeq.setMinimumSize(QtCore.QSize(0, 24))
        self.btnCancelLastSeq.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnCancelLastSeq.setCheckable(False)
        self.btnCancelLastSeq.setObjectName("btnCancelLastSeq")
        self.vLayoutButtons.addWidget(self.btnCancelLastSeq)
        self.hLayoutTop.addLayout(self.vLayoutButtons)
        self.textTestInfo = QtWidgets.QPlainTextEdit(parent=self.scrollAreaWidgetContents)
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
        self.gridLayoutTop.setObjectName("gridLayoutTop")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem, 0, 8, 1, 1)
        self.labelTimeDelayVal = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.labelTimeDelayVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelTimeDelayVal.setObjectName("labelTimeDelayVal")
        self.gridLayoutTop.addWidget(self.labelTimeDelayVal, 0, 3, 1, 1)
        self.cBoxPlots = QtWidgets.QComboBox(parent=self.scrollAreaWidgetContents)
        self.cBoxPlots.setMinimumSize(QtCore.QSize(110, 0))
        self.cBoxPlots.setObjectName("cBoxPlots")
        self.gridLayoutTop.addWidget(self.cBoxPlots, 0, 7, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem2, 0, 5, 1, 1)
        self.labelTimeDelay = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTimeDelay.sizePolicy().hasHeightForWidth())
        self.labelTimeDelay.setSizePolicy(sizePolicy)
        self.labelTimeDelay.setMinimumSize(QtCore.QSize(0, 22))
        font = QtGui.QFont()
        font.setBold(True)
        self.labelTimeDelay.setFont(font)
        self.labelTimeDelay.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelTimeDelay.setObjectName("labelTimeDelay")
        self.gridLayoutTop.addWidget(self.labelTimeDelay, 0, 2, 1, 1)
        self.labelSelectedPlot = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelSelectedPlot.setFont(font)
        self.labelSelectedPlot.setObjectName("labelSelectedPlot")
        self.gridLayoutTop.addWidget(self.labelSelectedPlot, 0, 6, 1, 1)
        self.hLayoutTop.addLayout(self.gridLayoutTop)
        self.verticalLayout.addLayout(self.hLayoutTop)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelMeasDate = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMeasDate.sizePolicy().hasHeightForWidth())
        self.labelMeasDate.setSizePolicy(sizePolicy)
        self.labelMeasDate.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.labelMeasDate.setFont(font)
        self.labelMeasDate.setObjectName("labelMeasDate")
        self.gridLayout.addWidget(self.labelMeasDate, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(37, 18, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 3, 1, 1)
        self.labelMeasDateValue = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
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
        self.verticalLayout.addLayout(self.gridLayout)
        self.vLayoutPlotsTable = QtWidgets.QVBoxLayout()
        self.vLayoutPlotsTable.setSpacing(12)
        self.vLayoutPlotsTable.setObjectName("vLayoutPlotsTable")
        self.vLayoutPlots = QtWidgets.QVBoxLayout()
        self.vLayoutPlots.setSpacing(6)
        self.vLayoutPlots.setObjectName("vLayoutPlots")
        self.plot0 = PlotWidget(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plot0.sizePolicy().hasHeightForWidth())
        self.plot0.setSizePolicy(sizePolicy)
        self.plot0.setMinimumSize(QtCore.QSize(500, 100))
        self.plot0.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot0.setObjectName("plot0")
        self.vLayoutPlots.addWidget(self.plot0)
        self.plot1 = PlotWidget(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plot1.sizePolicy().hasHeightForWidth())
        self.plot1.setSizePolicy(sizePolicy)
        self.plot1.setMinimumSize(QtCore.QSize(500, 100))
        self.plot1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot1.setObjectName("plot1")
        self.vLayoutPlots.addWidget(self.plot1)
        self.plot2 = PlotWidget(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plot2.sizePolicy().hasHeightForWidth())
        self.plot2.setSizePolicy(sizePolicy)
        self.plot2.setMinimumSize(QtCore.QSize(500, 100))
        self.plot2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.plot2.setObjectName("plot2")
        self.vLayoutPlots.addWidget(self.plot2)
        self.plot3 = PlotWidget(parent=self.scrollAreaWidgetContents)
        self.plot3.setMinimumSize(QtCore.QSize(500, 120))
        self.plot3.setMaximumSize(QtCore.QSize(16777215, 125))
        self.plot3.setObjectName("plot3")
        self.vLayoutPlots.addWidget(self.plot3)
        self.plot4 = PlotWidget(parent=self.scrollAreaWidgetContents)
        self.plot4.setMinimumSize(QtCore.QSize(500, 120))
        self.plot4.setMaximumSize(QtCore.QSize(16777215, 125))
        self.plot4.setObjectName("plot4")
        self.vLayoutPlots.addWidget(self.plot4)
        self.plot5 = PlotWidget(parent=self.scrollAreaWidgetContents)
        self.plot5.setMinimumSize(QtCore.QSize(500, 120))
        self.plot5.setMaximumSize(QtCore.QSize(16777215, 125))
        self.plot5.setObjectName("plot5")
        self.vLayoutPlots.addWidget(self.plot5)
        self.vLayoutPlotsTable.addLayout(self.vLayoutPlots)
        self.hLayoutTable = QtWidgets.QHBoxLayout()
        self.hLayoutTable.setObjectName("hLayoutTable")
        self.tableView = QtWidgets.QTableView(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMinimumSize(QtCore.QSize(800, 300))
        self.tableView.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        self.hLayoutTable.addWidget(self.tableView)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayoutTable.addItem(spacerItem4)
        self.hLayoutTable.setStretch(1, 1)
        self.vLayoutPlotsTable.addLayout(self.hLayoutTable)
        self.vLayoutPlotsTable.setStretch(0, 1)
        self.verticalLayout.addLayout(self.vLayoutPlotsTable)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)

        self.retranslateUi(TimeDelayTab)
        QtCore.QMetaObject.connectSlotsByName(TimeDelayTab)
        TimeDelayTab.setTabOrder(self.btnTest, self.btnCancelLastSeq)
        TimeDelayTab.setTabOrder(self.btnCancelLastSeq, self.textTestInfo)
        TimeDelayTab.setTabOrder(self.textTestInfo, self.cBoxPlots)
        TimeDelayTab.setTabOrder(self.cBoxPlots, self.plot0)
        TimeDelayTab.setTabOrder(self.plot0, self.plot1)
        TimeDelayTab.setTabOrder(self.plot1, self.plot2)
        TimeDelayTab.setTabOrder(self.plot2, self.plot3)
        TimeDelayTab.setTabOrder(self.plot3, self.plot4)
        TimeDelayTab.setTabOrder(self.plot4, self.plot5)
        TimeDelayTab.setTabOrder(self.plot5, self.scrollArea)

    def retranslateUi(self, TimeDelayTab):
        _translate = QtCore.QCoreApplication.translate
        TimeDelayTab.setWindowTitle(_translate("TimeDelayTab", "Form"))
        self.btnTest.setText(_translate("TimeDelayTab", "Start time delay test"))
        self.btnCancelLastSeq.setText(_translate("TimeDelayTab", "Cancel last sequence"))
        self.labelTimeDelayVal.setText(_translate("TimeDelayTab", "?"))
        self.labelTimeDelay.setToolTip(_translate("TimeDelayTab", "The time delay represents the time that elapses between the execution of the control command and the response of the controlled system."))
        self.labelTimeDelay.setText(_translate("TimeDelayTab", "Time Delay:"))
        self.labelSelectedPlot.setToolTip(_translate("TimeDelayTab", "Select the plot you want to click in."))
        self.labelSelectedPlot.setText(_translate("TimeDelayTab", "Selected plot:"))
        self.labelMeasDate.setText(_translate("TimeDelayTab", "Measurement date:"))
from pyqtgraph import PlotWidget

# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\AutoReconnectTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AutoReconnectTab(object):
    def setupUi(self, AutoReconnectTab):
        AutoReconnectTab.setObjectName("AutoReconnectTab")
        AutoReconnectTab.resize(704, 610)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AutoReconnectTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 50, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnAutoReconnect = QtWidgets.QPushButton(parent=AutoReconnectTab)
        self.btnAutoReconnect.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnAutoReconnect.setCheckable(True)
        self.btnAutoReconnect.setObjectName("btnAutoReconnect")
        self.verticalLayout.addWidget(self.btnAutoReconnect)
        self.textTestInfo = QtWidgets.QPlainTextEdit(parent=AutoReconnectTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textTestInfo.sizePolicy().hasHeightForWidth())
        self.textTestInfo.setSizePolicy(sizePolicy)
        self.textTestInfo.setMinimumSize(QtCore.QSize(125, 22))
        self.textTestInfo.setMaximumSize(QtCore.QSize(200, 44))
        self.textTestInfo.setUndoRedoEnabled(False)
        self.textTestInfo.setReadOnly(True)
        self.textTestInfo.setPlainText("")
        self.textTestInfo.setObjectName("textTestInfo")
        self.verticalLayout.addWidget(self.textTestInfo)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayoutTop = QtWidgets.QGridLayout()
        self.gridLayoutTop.setObjectName("gridLayoutTop")
        self.labelGradient = QtWidgets.QLabel(parent=AutoReconnectTab)
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
        self.gridLayoutTop.addWidget(self.labelGradient, 1, 1, 1, 1)
        self.labelGradientVal = QtWidgets.QLabel(parent=AutoReconnectTab)
        self.labelGradientVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelGradientVal.setObjectName("labelGradientVal")
        self.gridLayoutTop.addWidget(self.labelGradientVal, 1, 2, 1, 1)
        self.labelSystemDelayVal = QtWidgets.QLabel(parent=AutoReconnectTab)
        self.labelSystemDelayVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelSystemDelayVal.setObjectName("labelSystemDelayVal")
        self.gridLayoutTop.addWidget(self.labelSystemDelayVal, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem, 0, 4, 1, 1)
        self.labelRiseTime = QtWidgets.QLabel(parent=AutoReconnectTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRiseTime.sizePolicy().hasHeightForWidth())
        self.labelRiseTime.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelRiseTime.setFont(font)
        self.labelRiseTime.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelRiseTime.setObjectName("labelRiseTime")
        self.gridLayoutTop.addWidget(self.labelRiseTime, 2, 1, 1, 1)
        self.labelRiseTimeVal = QtWidgets.QLabel(parent=AutoReconnectTab)
        self.labelRiseTimeVal.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelRiseTimeVal.setObjectName("labelRiseTimeVal")
        self.gridLayoutTop.addWidget(self.labelRiseTimeVal, 2, 2, 1, 1)
        self.labelTest1Info = QtWidgets.QLabel(parent=AutoReconnectTab)
        self.labelTest1Info.setMinimumSize(QtCore.QSize(150, 0))
        self.labelTest1Info.setText("")
        self.labelTest1Info.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelTest1Info.setObjectName("labelTest1Info")
        self.gridLayoutTop.addWidget(self.labelTest1Info, 0, 5, 1, 1)
        self.labelSystemDelay = QtWidgets.QLabel(parent=AutoReconnectTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSystemDelay.sizePolicy().hasHeightForWidth())
        self.labelSystemDelay.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.labelSystemDelay.setFont(font)
        self.labelSystemDelay.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.labelSystemDelay.setObjectName("labelSystemDelay")
        self.gridLayoutTop.addWidget(self.labelSystemDelay, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayoutTop.addItem(spacerItem1, 0, 6, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayoutTop)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem2 = QtWidgets.QSpacerItem(37, 18, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.labelMeasDateValue = QtWidgets.QLabel(parent=AutoReconnectTab)
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
        self.labelMeasDate = QtWidgets.QLabel(parent=AutoReconnectTab)
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
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.XYGraph = PlotWidget(parent=AutoReconnectTab)
        self.XYGraph.setMinimumSize(QtCore.QSize(0, 400))
        self.XYGraph.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.XYGraph.setObjectName("XYGraph")
        self.verticalLayout_2.addWidget(self.XYGraph)

        self.retranslateUi(AutoReconnectTab)
        QtCore.QMetaObject.connectSlotsByName(AutoReconnectTab)

    def retranslateUi(self, AutoReconnectTab):
        _translate = QtCore.QCoreApplication.translate
        AutoReconnectTab.setWindowTitle(_translate("AutoReconnectTab", "Form"))
        self.btnAutoReconnect.setText(_translate("AutoReconnectTab", "Start automatic reconnection test"))
        self.labelGradient.setToolTip(_translate("AutoReconnectTab", "The gradient represents the slope with which the process variable rises to the setpoint."))
        self.labelGradient.setText(_translate("AutoReconnectTab", "Gradient:"))
        self.labelGradientVal.setText(_translate("AutoReconnectTab", "?"))
        self.labelSystemDelayVal.setText(_translate("AutoReconnectTab", "?"))
        self.labelRiseTime.setToolTip(_translate("AutoReconnectTab", "The rise time indicates the time elapsed during the rise from 0 % to 100 % of the setpoint value."))
        self.labelRiseTime.setText(_translate("AutoReconnectTab", "Rise time:"))
        self.labelRiseTimeVal.setText(_translate("AutoReconnectTab", "?"))
        self.labelSystemDelay.setToolTip(_translate("AutoReconnectTab", "The system delay represents the time that elapses between the execution of the control command and the response of the controlled system."))
        self.labelSystemDelay.setText(_translate("AutoReconnectTab", "System delay:"))
        self.labelMeasDate.setText(_translate("AutoReconnectTab", "Measurement date:"))
from pyqtgraph import PlotWidget
# Form implementation generated from reading ui file 'c:\Data\Projekty\GitHub\FVE-testing-and-data-processing\dp_app\include\UIs\ControlPanelTab.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ControlPanelTab(object):
    def setupUi(self, ControlPanelTab):
        ControlPanelTab.setObjectName("ControlPanelTab")
        ControlPanelTab.resize(651, 458)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ControlPanelTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle_2 = QtWidgets.QLabel(parent=ControlPanelTab)
        self.labelTitle_2.setMinimumSize(QtCore.QSize(155, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.labelTitle_2.setFont(font)
        self.labelTitle_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelTitle_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle_2.setObjectName("labelTitle_2")
        self.verticalLayout.addWidget(self.labelTitle_2)
        self.line = QtWidgets.QFrame(parent=ControlPanelTab)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.pushBtbVoltMeas = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtbVoltMeas.setObjectName("pushBtbVoltMeas")
        self.verticalLayout.addWidget(self.pushBtbVoltMeas)
        self.pushBtnRS485Meas = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtnRS485Meas.setObjectName("pushBtnRS485Meas")
        self.verticalLayout.addWidget(self.pushBtnRS485Meas)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.vLayoutBtns_2 = QtWidgets.QVBoxLayout()
        self.vLayoutBtns_2.setContentsMargins(20, -1, 0, -1)
        self.vLayoutBtns_2.setObjectName("vLayoutBtns_2")
        self.labelTitle_3 = QtWidgets.QLabel(parent=ControlPanelTab)
        self.labelTitle_3.setMinimumSize(QtCore.QSize(155, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.labelTitle_3.setFont(font)
        self.labelTitle_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelTitle_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle_3.setObjectName("labelTitle_3")
        self.vLayoutBtns_2.addWidget(self.labelTitle_3)
        self.line_2 = QtWidgets.QFrame(parent=ControlPanelTab)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.vLayoutBtns_2.addWidget(self.line_2)
        self.pushBtbVoltMeas_2 = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtbVoltMeas_2.setObjectName("pushBtbVoltMeas_2")
        self.vLayoutBtns_2.addWidget(self.pushBtbVoltMeas_2)
        self.pushBtnRS485Meas_2 = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtnRS485Meas_2.setObjectName("pushBtnRS485Meas_2")
        self.vLayoutBtns_2.addWidget(self.pushBtnRS485Meas_2)
        self.pushBtnDiDoMeas_3 = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtnDiDoMeas_3.setObjectName("pushBtnDiDoMeas_3")
        self.vLayoutBtns_2.addWidget(self.pushBtnDiDoMeas_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayoutBtns_2.addItem(spacerItem1)
        self.pushBtnDiDoMeas_4 = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtnDiDoMeas_4.setObjectName("pushBtnDiDoMeas_4")
        self.vLayoutBtns_2.addWidget(self.pushBtnDiDoMeas_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vLayoutBtns_2.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.vLayoutBtns_2)
        self.vLayoutBtns_3 = QtWidgets.QVBoxLayout()
        self.vLayoutBtns_3.setContentsMargins(20, -1, 0, -1)
        self.vLayoutBtns_3.setObjectName("vLayoutBtns_3")
        self.labelTitle_4 = QtWidgets.QLabel(parent=ControlPanelTab)
        self.labelTitle_4.setMinimumSize(QtCore.QSize(155, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.labelTitle_4.setFont(font)
        self.labelTitle_4.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.labelTitle_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle_4.setObjectName("labelTitle_4")
        self.vLayoutBtns_3.addWidget(self.labelTitle_4)
        self.line_3 = QtWidgets.QFrame(parent=ControlPanelTab)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.vLayoutBtns_3.addWidget(self.line_3)
        self.pushBtbVoltMeas_3 = QtWidgets.QPushButton(parent=ControlPanelTab)
        self.pushBtbVoltMeas_3.setObjectName("pushBtbVoltMeas_3")
        self.vLayoutBtns_3.addWidget(self.pushBtbVoltMeas_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.vLayoutBtns_3.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.vLayoutBtns_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(ControlPanelTab)
        QtCore.QMetaObject.connectSlotsByName(ControlPanelTab)
        ControlPanelTab.setTabOrder(self.pushBtbVoltMeas, self.pushBtnRS485Meas)

    def retranslateUi(self, ControlPanelTab):
        _translate = QtCore.QCoreApplication.translate
        ControlPanelTab.setWindowTitle(_translate("ControlPanelTab", "Form"))
        self.labelTitle_2.setText(_translate("ControlPanelTab", "CSV Operations"))
        self.pushBtbVoltMeas.setText(_translate("ControlPanelTab", "Import CSV Data"))
        self.pushBtnRS485Meas.setText(_translate("ControlPanelTab", "Show CSV Raw Data"))
        self.labelTitle_3.setText(_translate("ControlPanelTab", "Graph Analysis"))
        self.pushBtbVoltMeas_2.setText(_translate("ControlPanelTab", "Show XY Graph"))
        self.pushBtnRS485Meas_2.setText(_translate("ControlPanelTab", "Show PQ Diagram"))
        self.pushBtnDiDoMeas_3.setText(_translate("ControlPanelTab", "Active PQ Diagram"))
        self.pushBtnDiDoMeas_4.setText(_translate("ControlPanelTab", "Measured Profiles"))
        self.labelTitle_4.setText(_translate("ControlPanelTab", "Reports"))
        self.pushBtbVoltMeas_3.setText(_translate("ControlPanelTab", "Generate Final Report"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_map_graph.ui'
#
# Created: Sun Jun 29 20:05:39 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RightWidget(object):
    def setupUi(self, RightWidget):
        RightWidget.setObjectName("RightWidget")
        RightWidget.resize(QtCore.QSize(QtCore.QRect(0,0,225,615).size()).expandedTo(RightWidget.minimumSizeHint()))
        RightWidget.setMinimumSize(QtCore.QSize(225,615))

        self.box_status = QtGui.QFrame(RightWidget)
        self.box_status.setGeometry(QtCore.QRect(0,165,225,131))
        self.box_status.setFrameShape(QtGui.QFrame.NoFrame)
        self.box_status.setObjectName("box_status")

        self.layoutWidget = QtGui.QWidget(self.box_status)
        self.layoutWidget.setGeometry(QtCore.QRect(0,5,226,121))
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridlayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout.setContentsMargins(5,-1,2,-1)
        self.gridlayout.setHorizontalSpacing(0)
        self.gridlayout.setVerticalSpacing(5)
        self.gridlayout.setObjectName("gridlayout")

        self.label_health = QtGui.QLabel(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_health.sizePolicy().hasHeightForWidth())
        self.label_health.setSizePolicy(sizePolicy)
        self.label_health.setMinimumSize(QtCore.QSize(80,0))
        self.label_health.setObjectName("label_health")
        self.gridlayout.addWidget(self.label_health,0,0,1,1)

        self.bar_health = QtGui.QProgressBar(self.layoutWidget)
        self.bar_health.setMinimumSize(QtCore.QSize(0,22))
        self.bar_health.setMaximumSize(QtCore.QSize(16777215,22))
        self.bar_health.setProperty("value",QtCore.QVariant(100))
        self.bar_health.setTextVisible(False)
        self.bar_health.setObjectName("bar_health")
        self.gridlayout.addWidget(self.bar_health,0,1,1,1)

        self.label_mana = QtGui.QLabel(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_mana.sizePolicy().hasHeightForWidth())
        self.label_mana.setSizePolicy(sizePolicy)
        self.label_mana.setMinimumSize(QtCore.QSize(80,0))
        self.label_mana.setObjectName("label_mana")
        self.gridlayout.addWidget(self.label_mana,1,0,1,1)

        self.bar_mana = QtGui.QProgressBar(self.layoutWidget)
        self.bar_mana.setMinimumSize(QtCore.QSize(0,22))
        self.bar_mana.setMaximumSize(QtCore.QSize(16777215,22))
        self.bar_mana.setProperty("value",QtCore.QVariant(100))
        self.bar_mana.setTextVisible(False)
        self.bar_mana.setObjectName("bar_mana")
        self.gridlayout.addWidget(self.bar_mana,1,1,1,1)

        self.label_movement = QtGui.QLabel(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_movement.sizePolicy().hasHeightForWidth())
        self.label_movement.setSizePolicy(sizePolicy)
        self.label_movement.setMinimumSize(QtCore.QSize(80,0))
        self.label_movement.setObjectName("label_movement")
        self.gridlayout.addWidget(self.label_movement,2,0,1,1)

        self.bar_movement = QtGui.QProgressBar(self.layoutWidget)
        self.bar_movement.setMinimumSize(QtCore.QSize(0,22))
        self.bar_movement.setMaximumSize(QtCore.QSize(16777215,22))
        self.bar_movement.setProperty("value",QtCore.QVariant(100))
        self.bar_movement.setTextVisible(False)
        self.bar_movement.setObjectName("bar_movement")
        self.gridlayout.addWidget(self.bar_movement,2,1,1,1)

        self.graph_map = QtGui.QLabel(RightWidget)
        self.graph_map.setGeometry(QtCore.QRect(4,0,218,154))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph_map.sizePolicy().hasHeightForWidth())
        self.graph_map.setSizePolicy(sizePolicy)
        self.graph_map.setMinimumSize(QtCore.QSize(218,154))
        self.graph_map.setMaximumSize(QtCore.QSize(218,154))
        self.graph_map.setAutoFillBackground(False)
        self.graph_map.setObjectName("graph_map")

        self.retranslateUi(RightWidget)
        QtCore.QMetaObject.connectSlotsByName(RightWidget)

    def retranslateUi(self, RightWidget):
        RightWidget.setWindowTitle(QtGui.QApplication.translate("RightWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_health.setText(QtGui.QApplication.translate("RightWidget", "Health", None, QtGui.QApplication.UnicodeUTF8))
        self.bar_health.setStyleSheet(QtGui.QApplication.translate("RightWidget", "QProgressBar { border: 2px solid gray; border-radius: 5px; }\n"
        "QProgressBar::chunk {background-color:#FF3333;}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_mana.setText(QtGui.QApplication.translate("RightWidget", "Mana", None, QtGui.QApplication.UnicodeUTF8))
        self.bar_mana.setStyleSheet(QtGui.QApplication.translate("RightWidget", "QProgressBar { border: 2px solid gray; border-radius: 5px; }\n"
        "QProgressBar::chunk {background-color:#0066FF}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_movement.setText(QtGui.QApplication.translate("RightWidget", "Movement", None, QtGui.QApplication.UnicodeUTF8))
        self.bar_movement.setStyleSheet(QtGui.QApplication.translate("RightWidget", "QProgressBar { border: 2px solid gray; border-radius: 5px; }\n"
        "QProgressBar::chunk {background-color:#33CC33;}", None, QtGui.QApplication.UnicodeUTF8))
        self.graph_map.setStyleSheet(QtGui.QApplication.translate("RightWidget", "QLabel {background-color:#D0D0D0;}", None, QtGui.QApplication.UnicodeUTF8))

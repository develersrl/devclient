# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_map.ui'
#
# Created: Thu Jan 31 18:46:39 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RightWidget(object):
    def setupUi(self, RightWidget):
        RightWidget.setObjectName("RightWidget")
        RightWidget.resize(QtCore.QSize(QtCore.QRect(0,0,230,615).size()).expandedTo(RightWidget.minimumSizeHint()))

        self.layoutWidget = QtGui.QWidget(RightWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0,235,226,121))
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridlayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout.setContentsMargins(5,-1,-1,-1)
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

        self.wild_map = QtGui.QTextEdit(RightWidget)
        self.wild_map.setGeometry(QtCore.QRect(0,0,225,231))
        self.wild_map.setFocusPolicy(QtCore.Qt.NoFocus)
        self.wild_map.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.wild_map.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.wild_map.setReadOnly(True)
        self.wild_map.setProperty("char_width",QtCore.QVariant(27))
        self.wild_map.setProperty("char_height",QtCore.QVariant(11))
        self.wild_map.setObjectName("wild_map")

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
        self.wild_map.setStyleSheet(QtGui.QApplication.translate("RightWidget", "QTextEdit { background-color: #000000; font: 10pt \"Courier\"; color: #FFFFFF;}", None, QtGui.QApplication.UnicodeUTF8))
        self.wild_map.setHtml(QtGui.QApplication.translate("RightWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Courier\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Mon Mar 24 12:55:29 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dev_client(object):
    def setupUi(self, dev_client):
        dev_client.setObjectName("dev_client")
        dev_client.resize(QtCore.QSize(QtCore.QRect(0,0,935,698).size()).expandedTo(dev_client.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(dev_client)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(5)
        self.gridlayout.setHorizontalSpacing(5)
        self.gridlayout.setVerticalSpacing(3)
        self.gridlayout.setObjectName("gridlayout")

        self.toppanel = QtGui.QFrame(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toppanel.sizePolicy().hasHeightForWidth())
        self.toppanel.setSizePolicy(sizePolicy)
        self.toppanel.setMinimumSize(QtCore.QSize(925,30))
        self.toppanel.setMaximumSize(QtCore.QSize(16777215,30))
        self.toppanel.setFrameShape(QtGui.QFrame.NoFrame)
        self.toppanel.setFrameShadow(QtGui.QFrame.Raised)
        self.toppanel.setObjectName("toppanel")

        self.list_conn = QtGui.QComboBox(self.toppanel)
        self.list_conn.setGeometry(QtCore.QRect(85,2,145,26))
        self.list_conn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_conn.setObjectName("list_conn")

        self.list_account = QtGui.QComboBox(self.toppanel)
        self.list_account.setGeometry(QtCore.QRect(325,2,145,26))
        self.list_account.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list_account.setObjectName("list_account")

        self.top_label_conn = QtGui.QLabel(self.toppanel)
        self.top_label_conn.setGeometry(QtCore.QRect(0,0,80,30))
        self.top_label_conn.setObjectName("top_label_conn")

        self.top_label_account = QtGui.QLabel(self.toppanel)
        self.top_label_account.setGeometry(QtCore.QRect(240,0,80,30))
        self.top_label_account.setObjectName("top_label_account")

        self.button_connect = QtGui.QPushButton(self.toppanel)
        self.button_connect.setGeometry(QtCore.QRect(475,2,105,26))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_connect.sizePolicy().hasHeightForWidth())
        self.button_connect.setSizePolicy(sizePolicy)
        self.button_connect.setMinimumSize(QtCore.QSize(105,26))
        self.button_connect.setMaximumSize(QtCore.QSize(105,26))
        self.button_connect.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_connect.setIcon(QtGui.QIcon(":/images/connect.png"))
        self.button_connect.setIconSize(QtCore.QSize(16,16))
        self.button_connect.setObjectName("button_connect")

        self.button_option = QtGui.QPushButton(self.toppanel)
        self.button_option.setGeometry(QtCore.QRect(585,2,105,26))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_option.sizePolicy().hasHeightForWidth())
        self.button_option.setSizePolicy(sizePolicy)
        self.button_option.setMinimumSize(QtCore.QSize(105,26))
        self.button_option.setMaximumSize(QtCore.QSize(105,26))
        self.button_option.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button_option.setIcon(QtGui.QIcon(":/images/option.png"))
        self.button_option.setIconSize(QtCore.QSize(16,16))
        self.button_option.setObjectName("button_option")
        self.gridlayout.addWidget(self.toppanel,0,0,1,2)

        self.text_output = QtGui.QTextEdit(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.text_output.sizePolicy().hasHeightForWidth())
        self.text_output.setSizePolicy(sizePolicy)
        self.text_output.setMinimumSize(QtCore.QSize(690,0))
        self.text_output.setFocusPolicy(QtCore.Qt.NoFocus)
        self.text_output.setUndoRedoEnabled(False)
        self.text_output.setReadOnly(True)
        self.text_output.setObjectName("text_output")
        self.gridlayout.addWidget(self.text_output,1,0,1,1)

        self.rightpanel = QtGui.QFrame(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightpanel.sizePolicy().hasHeightForWidth())
        self.rightpanel.setSizePolicy(sizePolicy)
        self.rightpanel.setMinimumSize(QtCore.QSize(230,615))
        self.rightpanel.setFrameShape(QtGui.QFrame.NoFrame)
        self.rightpanel.setObjectName("rightpanel")
        self.gridlayout.addWidget(self.rightpanel,1,1,2,1)

        self.text_input = QtGui.QComboBox(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.text_input.sizePolicy().hasHeightForWidth())
        self.text_input.setSizePolicy(sizePolicy)
        self.text_input.setMinimumSize(QtCore.QSize(690,0))
        self.text_input.setEditable(True)
        self.text_input.setObjectName("text_input")
        self.text_input.addItem("")
        self.gridlayout.addWidget(self.text_input,2,0,1,1)
        dev_client.setCentralWidget(self.centralwidget)

        self.retranslateUi(dev_client)
        QtCore.QMetaObject.connectSlotsByName(dev_client)

    def retranslateUi(self, dev_client):
        dev_client.setWindowTitle(QtGui.QApplication.translate("dev_client", "DevClient", None, QtGui.QApplication.UnicodeUTF8))
        self.top_label_conn.setText(QtGui.QApplication.translate("dev_client", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.top_label_account.setText(QtGui.QApplication.translate("dev_client", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.button_connect.setText(QtGui.QApplication.translate("dev_client", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.button_connect.setShortcut(QtGui.QApplication.translate("dev_client", "Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.button_option.setText(QtGui.QApplication.translate("dev_client", "Option", None, QtGui.QApplication.UnicodeUTF8))
        self.button_option.setShortcut(QtGui.QApplication.translate("dev_client", "Alt+O", None, QtGui.QApplication.UnicodeUTF8))
        self.text_output.setStyleSheet(QtGui.QApplication.translate("dev_client", "QTextEdit { background-color: #000000; font: 10pt \"Courier\"; color: #FFFFFF;}", None, QtGui.QApplication.UnicodeUTF8))

import gui_rc

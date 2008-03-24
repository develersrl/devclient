# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_option.ui'
#
# Created: Mon Mar 24 19:45:26 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_option(object):
    def setupUi(self, option):
        option.setObjectName("option")
        option.setWindowModality(QtCore.Qt.ApplicationModal)
        option.resize(QtCore.QSize(QtCore.QRect(0,0,414,290).size()).expandedTo(option.minimumSizeHint()))

        self.list_option = QtGui.QListWidget(option)
        self.list_option.setGeometry(QtCore.QRect(5,5,100,280))
        self.list_option.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_option.setTextElideMode(QtCore.Qt.ElideNone)
        self.list_option.setMovement(QtGui.QListView.Static)
        self.list_option.setFlow(QtGui.QListView.TopToBottom)
        self.list_option.setProperty("isWrapping",QtCore.QVariant(False))
        self.list_option.setSpacing(2)
        self.list_option.setViewMode(QtGui.QListView.IconMode)
        self.list_option.setModelColumn(0)
        self.list_option.setUniformItemSizes(True)
        self.list_option.setObjectName("list_option")

        self.page_container = QtGui.QStackedWidget(option)
        self.page_container.setGeometry(QtCore.QRect(105,0,306,290))
        self.page_container.setObjectName("page_container")

        self.conn_page = QtGui.QWidget()
        self.conn_page.setObjectName("conn_page")

        self.layoutWidget = QtGui.QWidget(self.conn_page)
        self.layoutWidget.setGeometry(QtCore.QRect(4,6,301,281))
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label_conn = QtGui.QLabel(self.layoutWidget)
        self.label_conn.setObjectName("label_conn")
        self.gridlayout.addWidget(self.label_conn,0,0,1,2)

        self.list_conn = QtGui.QComboBox(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_conn.sizePolicy().hasHeightForWidth())
        self.list_conn.setSizePolicy(sizePolicy)
        self.list_conn.setObjectName("list_conn")
        self.gridlayout.addWidget(self.list_conn,0,2,1,2)

        self.label_name_conn = QtGui.QLabel(self.layoutWidget)
        self.label_name_conn.setMinimumSize(QtCore.QSize(45,0))
        self.label_name_conn.setMaximumSize(QtCore.QSize(45,16777215))
        self.label_name_conn.setObjectName("label_name_conn")
        self.gridlayout.addWidget(self.label_name_conn,1,0,1,1)

        spacerItem = QtGui.QSpacerItem(45,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,1,1,1)

        self.name_conn = QtGui.QLineEdit(self.layoutWidget)
        self.name_conn.setObjectName("name_conn")
        self.gridlayout.addWidget(self.name_conn,1,2,1,2)

        self.label_host_conn = QtGui.QLabel(self.layoutWidget)
        self.label_host_conn.setMinimumSize(QtCore.QSize(45,0))
        self.label_host_conn.setMaximumSize(QtCore.QSize(45,16777215))
        self.label_host_conn.setObjectName("label_host_conn")
        self.gridlayout.addWidget(self.label_host_conn,2,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(45,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,2,1,1,1)

        self.host_conn = QtGui.QLineEdit(self.layoutWidget)
        self.host_conn.setObjectName("host_conn")
        self.gridlayout.addWidget(self.host_conn,2,2,1,2)

        self.label_port_conn = QtGui.QLabel(self.layoutWidget)
        self.label_port_conn.setMinimumSize(QtCore.QSize(45,0))
        self.label_port_conn.setMaximumSize(QtCore.QSize(45,16777215))
        self.label_port_conn.setObjectName("label_port_conn")
        self.gridlayout.addWidget(self.label_port_conn,3,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(135,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,3,1,1,2)

        self.port_conn = QtGui.QLineEdit(self.layoutWidget)
        self.port_conn.setMaxLength(8)
        self.port_conn.setObjectName("port_conn")
        self.gridlayout.addWidget(self.port_conn,3,3,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        spacerItem3 = QtGui.QSpacerItem(271,30,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem3)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(5)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem4 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem4)

        self.save_conn = QtGui.QPushButton(self.layoutWidget)
        self.save_conn.setIcon(QtGui.QIcon(":/images/button-save.png"))
        self.save_conn.setObjectName("save_conn")
        self.hboxlayout.addWidget(self.save_conn)

        self.delete_conn = QtGui.QPushButton(self.layoutWidget)
        self.delete_conn.setIcon(QtGui.QIcon(":/images/button-cancel.png"))
        self.delete_conn.setObjectName("delete_conn")
        self.hboxlayout.addWidget(self.delete_conn)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.page_container.addWidget(self.conn_page)

        self.account_page = QtGui.QWidget()
        self.account_page.setObjectName("account_page")

        self.frame_account_pwd = QtGui.QFrame(self.account_page)
        self.frame_account_pwd.setGeometry(QtCore.QRect(4,124,301,161))
        self.frame_account_pwd.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_account_pwd.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_account_pwd.setObjectName("frame_account_pwd")

        self.layoutWidget1 = QtGui.QWidget(self.frame_account_pwd)
        self.layoutWidget1.setGeometry(QtCore.QRect(5,5,296,156))
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.gridlayout1 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridlayout1.setHorizontalSpacing(5)
        self.gridlayout1.setVerticalSpacing(8)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.lineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.gridlayout1.addWidget(self.lineEdit,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.lineEdit_2 = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridlayout1.addWidget(self.lineEdit_2,1,1,1,1)

        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,2,0,1,1)

        self.lineEdit_3 = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_3.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridlayout1.addWidget(self.lineEdit_3,2,1,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem5 = QtGui.QSpacerItem(171,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem5)

        self.save_pwd_account = QtGui.QPushButton(self.layoutWidget1)
        self.save_pwd_account.setIcon(QtGui.QIcon(":/images/button-save.png"))
        self.save_pwd_account.setObjectName("save_pwd_account")
        self.hboxlayout1.addWidget(self.save_pwd_account)
        self.gridlayout1.addLayout(self.hboxlayout1,3,0,1,2)

        self.layoutWidget2 = QtGui.QWidget(self.account_page)
        self.layoutWidget2.setGeometry(QtCore.QRect(10,7,296,116))
        self.layoutWidget2.setObjectName("layoutWidget2")

        self.gridlayout2 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridlayout2.setHorizontalSpacing(0)
        self.gridlayout2.setVerticalSpacing(8)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_conn_account = QtGui.QLabel(self.layoutWidget2)
        self.label_conn_account.setObjectName("label_conn_account")
        self.gridlayout2.addWidget(self.label_conn_account,0,0,1,1)

        self.list_conn_account = QtGui.QComboBox(self.layoutWidget2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_conn_account.sizePolicy().hasHeightForWidth())
        self.list_conn_account.setSizePolicy(sizePolicy)
        self.list_conn_account.setMinimumSize(QtCore.QSize(150,0))
        self.list_conn_account.setObjectName("list_conn_account")
        self.gridlayout2.addWidget(self.list_conn_account,0,1,1,1)

        self.label_account_account = QtGui.QLabel(self.layoutWidget2)
        self.label_account_account.setObjectName("label_account_account")
        self.gridlayout2.addWidget(self.label_account_account,1,0,1,1)

        self.list_account = QtGui.QComboBox(self.layoutWidget2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_account.sizePolicy().hasHeightForWidth())
        self.list_account.setSizePolicy(sizePolicy)
        self.list_account.setMinimumSize(QtCore.QSize(150,0))
        self.list_account.setObjectName("list_account")
        self.gridlayout2.addWidget(self.list_account,1,1,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(3)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem6 = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem6)

        self.pwd_account = QtGui.QPushButton(self.layoutWidget2)
        self.pwd_account.setEnabled(False)
        self.pwd_account.setIcon(QtGui.QIcon(":/images/button-pwd.png"))
        self.pwd_account.setObjectName("pwd_account")
        self.hboxlayout2.addWidget(self.pwd_account)

        self.delete_account = QtGui.QPushButton(self.layoutWidget2)
        self.delete_account.setEnabled(False)
        self.delete_account.setIcon(QtGui.QIcon(":/images/button-cancel.png"))
        self.delete_account.setObjectName("delete_account")
        self.hboxlayout2.addWidget(self.delete_account)
        self.gridlayout2.addLayout(self.hboxlayout2,2,0,1,2)
        self.page_container.addWidget(self.account_page)

        self.alias_page = QtGui.QWidget()
        self.alias_page.setObjectName("alias_page")

        self.layoutWidget_2 = QtGui.QWidget(self.alias_page)
        self.layoutWidget_2.setGeometry(QtCore.QRect(5,5,301,281))
        self.layoutWidget_2.setObjectName("layoutWidget_2")

        self.gridlayout3 = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridlayout3.setObjectName("gridlayout3")

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_conn_alias = QtGui.QLabel(self.layoutWidget_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_conn_alias.sizePolicy().hasHeightForWidth())
        self.label_conn_alias.setSizePolicy(sizePolicy)
        self.label_conn_alias.setMinimumSize(QtCore.QSize(66,0))
        self.label_conn_alias.setObjectName("label_conn_alias")
        self.gridlayout4.addWidget(self.label_conn_alias,0,0,1,2)

        self.list_conn_alias = QtGui.QComboBox(self.layoutWidget_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_conn_alias.sizePolicy().hasHeightForWidth())
        self.list_conn_alias.setSizePolicy(sizePolicy)
        self.list_conn_alias.setObjectName("list_conn_alias")
        self.gridlayout4.addWidget(self.list_conn_alias,0,2,1,2)

        self.label_alias_alias = QtGui.QLabel(self.layoutWidget_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_alias_alias.sizePolicy().hasHeightForWidth())
        self.label_alias_alias.setSizePolicy(sizePolicy)
        self.label_alias_alias.setMinimumSize(QtCore.QSize(66,0))
        self.label_alias_alias.setObjectName("label_alias_alias")
        self.gridlayout4.addWidget(self.label_alias_alias,1,0,1,1)

        spacerItem7 = QtGui.QSpacerItem(80,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem7,1,1,1,2)

        self.list_alias = QtGui.QComboBox(self.layoutWidget_2)
        self.list_alias.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_alias.sizePolicy().hasHeightForWidth())
        self.list_alias.setSizePolicy(sizePolicy)
        self.list_alias.setObjectName("list_alias")
        self.gridlayout4.addWidget(self.list_alias,1,3,1,1)

        self.label_label_alias = QtGui.QLabel(self.layoutWidget_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_label_alias.sizePolicy().hasHeightForWidth())
        self.label_label_alias.setSizePolicy(sizePolicy)
        self.label_label_alias.setMinimumSize(QtCore.QSize(66,0))
        self.label_label_alias.setObjectName("label_label_alias")
        self.gridlayout4.addWidget(self.label_label_alias,2,0,1,1)

        spacerItem8 = QtGui.QSpacerItem(80,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem8,2,1,1,2)

        self.label_alias = QtGui.QLineEdit(self.layoutWidget_2)
        self.label_alias.setEnabled(False)
        self.label_alias.setObjectName("label_alias")
        self.gridlayout4.addWidget(self.label_alias,2,3,1,1)

        self.label_body_alias = QtGui.QLabel(self.layoutWidget_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_body_alias.sizePolicy().hasHeightForWidth())
        self.label_body_alias.setSizePolicy(sizePolicy)
        self.label_body_alias.setMinimumSize(QtCore.QSize(66,0))
        self.label_body_alias.setObjectName("label_body_alias")
        self.gridlayout4.addWidget(self.label_body_alias,3,0,1,1)

        self.body_alias = QtGui.QLineEdit(self.layoutWidget_2)
        self.body_alias.setEnabled(False)
        self.body_alias.setObjectName("body_alias")
        self.gridlayout4.addWidget(self.body_alias,3,1,1,3)
        self.gridlayout3.addLayout(self.gridlayout4,0,0,1,2)

        spacerItem9 = QtGui.QSpacerItem(271,66,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem9,1,0,1,2)

        spacerItem10 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem10,2,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.save_alias = QtGui.QPushButton(self.layoutWidget_2)
        self.save_alias.setIcon(QtGui.QIcon(":/images/button-save.png"))
        self.save_alias.setObjectName("save_alias")
        self.hboxlayout3.addWidget(self.save_alias)

        self.delete_alias = QtGui.QPushButton(self.layoutWidget_2)
        self.delete_alias.setIcon(QtGui.QIcon(":/images/button-cancel.png"))
        self.delete_alias.setObjectName("delete_alias")
        self.hboxlayout3.addWidget(self.delete_alias)
        self.gridlayout3.addLayout(self.hboxlayout3,2,1,1,1)
        self.page_container.addWidget(self.alias_page)

        self.macro_page = QtGui.QWidget()
        self.macro_page.setObjectName("macro_page")

        self.layoutWidget_3 = QtGui.QWidget(self.macro_page)
        self.layoutWidget_3.setGeometry(QtCore.QRect(5,5,301,281))
        self.layoutWidget_3.setObjectName("layoutWidget_3")

        self.gridlayout5 = QtGui.QGridLayout(self.layoutWidget_3)
        self.gridlayout5.setObjectName("gridlayout5")

        self.gridlayout6 = QtGui.QGridLayout()
        self.gridlayout6.setObjectName("gridlayout6")

        self.label_conn_macro = QtGui.QLabel(self.layoutWidget_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_conn_macro.sizePolicy().hasHeightForWidth())
        self.label_conn_macro.setSizePolicy(sizePolicy)
        self.label_conn_macro.setMinimumSize(QtCore.QSize(66,0))
        self.label_conn_macro.setObjectName("label_conn_macro")
        self.gridlayout6.addWidget(self.label_conn_macro,0,0,1,2)

        self.list_conn_macro = QtGui.QComboBox(self.layoutWidget_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_conn_macro.sizePolicy().hasHeightForWidth())
        self.list_conn_macro.setSizePolicy(sizePolicy)
        self.list_conn_macro.setObjectName("list_conn_macro")
        self.gridlayout6.addWidget(self.list_conn_macro,0,2,1,2)

        self.label_macro_macro = QtGui.QLabel(self.layoutWidget_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_macro_macro.sizePolicy().hasHeightForWidth())
        self.label_macro_macro.setSizePolicy(sizePolicy)
        self.label_macro_macro.setMinimumSize(QtCore.QSize(66,0))
        self.label_macro_macro.setObjectName("label_macro_macro")
        self.gridlayout6.addWidget(self.label_macro_macro,1,0,1,1)

        spacerItem11 = QtGui.QSpacerItem(80,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem11,1,1,1,2)

        self.list_macro = QtGui.QComboBox(self.layoutWidget_3)
        self.list_macro.setEnabled(False)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_macro.sizePolicy().hasHeightForWidth())
        self.list_macro.setSizePolicy(sizePolicy)
        self.list_macro.setObjectName("list_macro")
        self.gridlayout6.addWidget(self.list_macro,1,3,1,1)

        self.label_keys_macro = QtGui.QLabel(self.layoutWidget_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_keys_macro.sizePolicy().hasHeightForWidth())
        self.label_keys_macro.setSizePolicy(sizePolicy)
        self.label_keys_macro.setMinimumSize(QtCore.QSize(66,0))
        self.label_keys_macro.setObjectName("label_keys_macro")
        self.gridlayout6.addWidget(self.label_keys_macro,2,0,1,1)

        self.keys_macro = QtGui.QLineEdit(self.layoutWidget_3)
        self.keys_macro.setEnabled(False)
        self.keys_macro.setProperty("highlight_color",QtCore.QVariant(QtGui.QApplication.translate("option", "#e0e0e0", None, QtGui.QApplication.UnicodeUTF8)))
        self.keys_macro.setObjectName("keys_macro")
        self.gridlayout6.addWidget(self.keys_macro,2,3,1,1)

        self.label_command_macro = QtGui.QLabel(self.layoutWidget_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_command_macro.sizePolicy().hasHeightForWidth())
        self.label_command_macro.setSizePolicy(sizePolicy)
        self.label_command_macro.setMinimumSize(QtCore.QSize(66,0))
        self.label_command_macro.setObjectName("label_command_macro")
        self.gridlayout6.addWidget(self.label_command_macro,3,0,1,1)

        self.command_macro = QtGui.QLineEdit(self.layoutWidget_3)
        self.command_macro.setEnabled(False)
        self.command_macro.setObjectName("command_macro")
        self.gridlayout6.addWidget(self.command_macro,3,1,1,3)

        self.register_macro = QtGui.QPushButton(self.layoutWidget_3)
        self.register_macro.setEnabled(False)
        self.register_macro.setObjectName("register_macro")
        self.gridlayout6.addWidget(self.register_macro,2,1,1,2)
        self.gridlayout5.addLayout(self.gridlayout6,0,0,1,2)

        spacerItem12 = QtGui.QSpacerItem(271,66,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem12,1,0,1,2)

        spacerItem13 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem13,2,0,1,1)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.save_macro = QtGui.QPushButton(self.layoutWidget_3)
        self.save_macro.setIcon(QtGui.QIcon(":/images/button-save.png"))
        self.save_macro.setObjectName("save_macro")
        self.hboxlayout4.addWidget(self.save_macro)

        self.delete_macro = QtGui.QPushButton(self.layoutWidget_3)
        self.delete_macro.setIcon(QtGui.QIcon(":/images/button-cancel.png"))
        self.delete_macro.setObjectName("delete_macro")
        self.hboxlayout4.addWidget(self.delete_macro)
        self.gridlayout5.addLayout(self.hboxlayout4,2,1,1,1)
        self.page_container.addWidget(self.macro_page)

        self.pref_page = QtGui.QWidget()
        self.pref_page.setObjectName("pref_page")

        self.groupBox = QtGui.QGroupBox(self.pref_page)
        self.groupBox.setGeometry(QtCore.QRect(5,10,301,96))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")

        self.layoutWidget3 = QtGui.QWidget(self.groupBox)
        self.layoutWidget3.setGeometry(QtCore.QRect(2,10,296,81))
        self.layoutWidget3.setObjectName("layoutWidget3")

        self.gridlayout7 = QtGui.QGridLayout(self.layoutWidget3)
        self.gridlayout7.setHorizontalSpacing(5)
        self.gridlayout7.setObjectName("gridlayout7")

        self.echo_text = QtGui.QCheckBox(self.layoutWidget3)
        self.echo_text.setMinimumSize(QtCore.QSize(90,0))
        self.echo_text.setObjectName("echo_text")
        self.gridlayout7.addWidget(self.echo_text,0,0,1,1)

        self.echo_color_button = QtGui.QPushButton(self.layoutWidget3)
        self.echo_color_button.setMinimumSize(QtCore.QSize(80,26))
        self.echo_color_button.setMaximumSize(QtCore.QSize(80,26))
        self.echo_color_button.setIcon(QtGui.QIcon(":/images/button-color.png"))
        self.echo_color_button.setObjectName("echo_color_button")
        self.gridlayout7.addWidget(self.echo_color_button,0,1,1,1)

        self.echo_color = QtGui.QLineEdit(self.layoutWidget3)
        self.echo_color.setEnabled(False)
        self.echo_color.setMinimumSize(QtCore.QSize(80,0))
        self.echo_color.setMaximumSize(QtCore.QSize(80,16777215))
        self.echo_color.setObjectName("echo_color")
        self.gridlayout7.addWidget(self.echo_color,0,2,1,1)

        self.keep_text = QtGui.QCheckBox(self.layoutWidget3)
        self.keep_text.setMinimumSize(QtCore.QSize(195,0))
        self.keep_text.setObjectName("keep_text")
        self.gridlayout7.addWidget(self.keep_text,1,0,1,2)

        spacerItem14 = QtGui.QSpacerItem(76,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout7.addItem(spacerItem14,1,2,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.pref_page)
        self.groupBox_2.setGeometry(QtCore.QRect(5,109,301,176))
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")

        self.layoutWidget4 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget4.setGeometry(QtCore.QRect(0,19,298,156))
        self.layoutWidget4.setObjectName("layoutWidget4")

        self.gridlayout8 = QtGui.QGridLayout(self.layoutWidget4)
        self.gridlayout8.setObjectName("gridlayout8")

        self.save_log = QtGui.QCheckBox(self.layoutWidget4)
        self.save_log.setMinimumSize(QtCore.QSize(100,0))
        self.save_log.setObjectName("save_log")
        self.gridlayout8.addWidget(self.save_log,0,0,1,1)

        spacerItem15 = QtGui.QSpacerItem(156,22,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout8.addItem(spacerItem15,0,1,1,1)

        self.checkBox = QtGui.QCheckBox(self.layoutWidget4)
        self.checkBox.setObjectName("checkBox")
        self.gridlayout8.addWidget(self.checkBox,1,0,1,1)

        spacerItem16 = QtGui.QSpacerItem(156,22,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout8.addItem(spacerItem16,1,1,1,1)

        spacerItem17 = QtGui.QSpacerItem(294,56,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout8.addItem(spacerItem17,2,0,1,2)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setObjectName("hboxlayout5")

        spacerItem18 = QtGui.QSpacerItem(209,26,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout5.addItem(spacerItem18)

        self.save_preferences = QtGui.QPushButton(self.layoutWidget4)
        self.save_preferences.setIcon(QtGui.QIcon(":/images/button-save.png"))
        self.save_preferences.setObjectName("save_preferences")
        self.hboxlayout5.addWidget(self.save_preferences)
        self.gridlayout8.addLayout(self.hboxlayout5,3,0,1,2)
        self.page_container.addWidget(self.pref_page)

        self.retranslateUi(option)
        self.list_option.setCurrentRow(0)
        self.page_container.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(option)

    def retranslateUi(self, option):
        option.setWindowTitle(QtGui.QApplication.translate("option", "Option", None, QtGui.QApplication.UnicodeUTF8))
        self.list_option.clear()

        item = QtGui.QListWidgetItem(self.list_option)
        item.setText(QtGui.QApplication.translate("option", "Connections", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(QtGui.QIcon(":/images/connections.png"))

        item1 = QtGui.QListWidgetItem(self.list_option)
        item1.setText(QtGui.QApplication.translate("option", "Accounts", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(QtGui.QIcon(":/images/accounts.png"))

        item2 = QtGui.QListWidgetItem(self.list_option)
        item2.setText(QtGui.QApplication.translate("option", "Aliases", None, QtGui.QApplication.UnicodeUTF8))
        item2.setIcon(QtGui.QIcon(":/images/aliases.png"))

        item3 = QtGui.QListWidgetItem(self.list_option)
        item3.setText(QtGui.QApplication.translate("option", "Macros", None, QtGui.QApplication.UnicodeUTF8))
        item3.setIcon(QtGui.QIcon(":/images/macros.png"))

        item4 = QtGui.QListWidgetItem(self.list_option)
        item4.setText(QtGui.QApplication.translate("option", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        item4.setIcon(QtGui.QIcon(":/images/preferences.png"))
        self.label_conn.setText(QtGui.QApplication.translate("option", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.list_conn.addItem(QtGui.QApplication.translate("option", "Create New", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name_conn.setText(QtGui.QApplication.translate("option", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_host_conn.setText(QtGui.QApplication.translate("option", "Host", None, QtGui.QApplication.UnicodeUTF8))
        self.label_port_conn.setText(QtGui.QApplication.translate("option", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.save_conn.setText(QtGui.QApplication.translate("option", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_conn.setText(QtGui.QApplication.translate("option", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("option", "Old password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("option", "New Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("option", "New Password (again)", None, QtGui.QApplication.UnicodeUTF8))
        self.save_pwd_account.setText(QtGui.QApplication.translate("option", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label_conn_account.setText(QtGui.QApplication.translate("option", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_account_account.setText(QtGui.QApplication.translate("option", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.pwd_account.setText(QtGui.QApplication.translate("option", "Change Password", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_account.setText(QtGui.QApplication.translate("option", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label_conn_alias.setText(QtGui.QApplication.translate("option", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_alias_alias.setText(QtGui.QApplication.translate("option", "Alias", None, QtGui.QApplication.UnicodeUTF8))
        self.label_label_alias.setText(QtGui.QApplication.translate("option", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label_body_alias.setText(QtGui.QApplication.translate("option", "Body", None, QtGui.QApplication.UnicodeUTF8))
        self.save_alias.setText(QtGui.QApplication.translate("option", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_alias.setText(QtGui.QApplication.translate("option", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label_conn_macro.setText(QtGui.QApplication.translate("option", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_macro_macro.setText(QtGui.QApplication.translate("option", "Macro", None, QtGui.QApplication.UnicodeUTF8))
        self.label_keys_macro.setText(QtGui.QApplication.translate("option", "Keys", None, QtGui.QApplication.UnicodeUTF8))
        self.label_command_macro.setText(QtGui.QApplication.translate("option", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.register_macro.setText(QtGui.QApplication.translate("option", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.save_macro.setText(QtGui.QApplication.translate("option", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_macro.setText(QtGui.QApplication.translate("option", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("option", "Text inserted", None, QtGui.QApplication.UnicodeUTF8))
        self.echo_text.setText(QtGui.QApplication.translate("option", "Echo text", None, QtGui.QApplication.UnicodeUTF8))
        self.echo_color_button.setText(QtGui.QApplication.translate("option", "Color", None, QtGui.QApplication.UnicodeUTF8))
        self.keep_text.setText(QtGui.QApplication.translate("option", "Keep text entered", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("option", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.save_log.setText(QtGui.QApplication.translate("option", "Save log", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("option", "Save accounts", None, QtGui.QApplication.UnicodeUTF8))
        self.save_preferences.setText(QtGui.QApplication.translate("option", "Save", None, QtGui.QApplication.UnicodeUTF8))

import gui_rc
import gui_option_rc

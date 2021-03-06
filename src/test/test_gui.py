#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright (C) 2007 Gianni Valdambrini, Develer S.r.l (http://www.develer.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Gianni Valdambrini gvaldambrini@develer.com

__version__ = "$Revision$"[11:-2]
__docformat__ = 'restructuredtext'

import os
import sys
import shutil
import socket
import unittest

from PyQt4.QtCore import QObject
from PyQt4.QtGui import QComboBox, QApplication, QLineEdit

sys.path.append('..')
sys.path.append('../configobj')
sys.path.append('../../resources')

import communication
import devclient.storage as storage
from devclient.gui import SocketToCore, AccountManager, ConnectionManager


class GuiMock(object):

    def __init__(self):
        self._warning = None
        self._question = None
        self._text = {}
        self._text['FatalError'] = ''
        self._text['Account'] = ''
        self._text['SaveAccount'] = ''
        self.text_input = QComboBox()
        self.text_input.setEditable(True)
        self.list_account = QComboBox()

    def connect(self, widget, signal, callback):
        pass

    def displayWarning(self, title, message):
        self._warning = (title, message)

    def _displayQuestion(self, title, message):
        self._question = (title, message)
        return True


def fakeStartCore(self, cfg_file):
    self._server.listen()
    port = self._server.serverPort()
    self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._client.connect(("localhost", port))
    self._server.waitForNewConnection(500)
    self._s = self._server.nextPendingConnection()


def fakeDel(self):
    pass


class TestSocketToCore(unittest.TestCase, communication.TestSocket):
    def startCommunication(self):
        SocketToCore._startCore = fakeStartCore
        SocketToCore.__del__ = fakeDel
        s_core = SocketToCore(GuiMock(), '')
        return s_core, s_core._client


class ServerFake:
    cmd_password = 2
    cmd_new_player = 'new'


class TestAccountManager(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(TestAccountManager, self).__init__(methodName)
        if not QApplication.instance():
            self.app = QApplication([])

        self.test_dir = '../../data/storage/test_dir'
        self.cmd_password = ServerFake.cmd_password

    def setUp(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)
        storage.init(os.path.abspath(self.test_dir))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def emptyAccounts(self):
        conn = (0, 'name', 'host', 111)
        storage.setOption('save_account', 1)
        storage.addConnection(list(conn))
        account = AccountManager(GuiMock(), self.cmd_password, 1)
        self.assert_(storage.accounts(1) == [])

    def testNoSaveAccount(self):
        conn = (0, 'name', 'host', 111)
        mock = GuiMock()
        storage.addConnection(list(conn))
        account = AccountManager(mock, self.cmd_password, 1)
        account.commands.append("john")
        account.commands.append("johnpwd")
        account.save()
        self.assert_(storage.accounts(1) == [])
        self.assert_(mock._question is None)

    def testSaveAccount(self):
        conn = (0, 'name', 'host', 111)
        mock = GuiMock()
        storage.setOption('save_account', 1)
        storage.addConnection(list(conn))
        account = AccountManager(mock, self.cmd_password, 1)
        account.commands.append("john")
        account.commands.append("johnpwd")
        account.save()
        self.assert_(storage.accounts(1) == ["john"])
        self.assert_(mock._question is not None)

    def testSaveAccount2(self):
        conn = (0, 'name', 'host', 111)
        storage.setOption('save_account', 1)
        storage.addConnection(list(conn))
        account = AccountManager(GuiMock(), self.cmd_password, 1)
        account.commands.append("john")
        account.commands.append("johnpwd")
        account.save()
        self.assert_(storage.accountDetail(1, "john") == ["john", "johnpwd"])

    def testUpdateAccount(self):
        conn = (0, 'name', 'host', 111)
        mock = GuiMock()
        storage.setOption('save_account', 1)
        storage.addConnection(list(conn))
        storage.saveAccount(['john', 'pwd'], 1, 'john')
        account = AccountManager(mock, self.cmd_password, 1)
        account.commands.append("john")
        account.commands.append("johnpwd")
        account.save()
        self.assert_(storage.accountDetail(1, 'john') == ['john', 'johnpwd'])
        self.assert_(mock._question is None)

    def testDefaultAccount(self):
        conn = (0, 'name', 'host', 111)
        storage.setOption('save_account', 1)
        storage.addConnection(list(conn))
        self.assert_(storage.option('default_account', 1) == '')
        mock = GuiMock()
        mock.list_account.addItem('john')
        account = AccountManager(mock, self.cmd_password, 1)
        self.assert_(storage.option('default_account', 1) == 'john')


class SocketToCoreMock(QObject):
    def __init__(self, widget, cfg_file):
        QObject.__init__(self)
        self._messages = []

    def write(self, cmd, message):
        self._messages.append(message)


def fakeAppendEcho(self, text):
    if not hasattr(self, '_echo'):
        self._echo = []
    self._echo.append(text)


class TestConnectionManager(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(TestConnectionManager, self).__init__(methodName)
        sys.modules['devclient.gui'].SocketToCore = SocketToCoreMock
        if not QApplication.instance():
            self.app = QApplication([])
        self.test_dir = '../../data/storage/test_dir'
        self.cmd_password = ServerFake.cmd_password

    def setUp(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)
        storage.init(os.path.abspath(self.test_dir))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def buildConnManager(self, aliases = []):
        conn = (0, 'name', 'host', 111)
        storage.addConnection(list(conn))
        if aliases:
            storage.saveAliases(conn[1], aliases)
        ConnectionManager._appendEcho = fakeAppendEcho
        c = ConnectionManager(GuiMock(), '')
        c._account = AccountManager(GuiMock(), self.cmd_password, 1)
        c._server = ServerFake
        c.conn_name = conn[1]
        c.reloadConnData(conn[1])
        c._s_core._messages = []
        return c

    def testEchoMode(self):
        c = self.buildConnManager()
        line_edit = c._w.text_input.lineEdit()
        self.assert_(line_edit.echoMode() == QLineEdit.Normal)
        c.sendText("john")
        c._manageLineInput()
        self.assert_(line_edit.echoMode() == QLineEdit.Password)
        c.sendText("johnpwd")
        c._manageLineInput()
        self.assert_(line_edit.echoMode() == QLineEdit.Normal)

    def testEchoMode2(self):
        c = self.buildConnManager()
        line_edit = c._w.text_input.lineEdit()
        self.assert_(line_edit.echoMode() == QLineEdit.Normal)
        c.sendText("new")
        c._manageLineInput()
        self.assert_(line_edit.echoMode() == QLineEdit.Normal)
        c.sendText("fakepwd")
        c._manageLineInput()
        self.assert_(line_edit.echoMode() == QLineEdit.Normal)

    def testSendText(self):
        c = self.buildConnManager()
        c.sendText('who')
        self.assert_(c._s_core._messages == ['who'])
        self.assert_(c._echo == ['who'])

    def testSendText2(self):
        c = self.buildConnManager()
        c.sendText('up;down')
        self.assert_(c._s_core._messages == ['up', 'down'])
        self.assert_(c._echo == ['up;down'])

    def testSendTextWithAlias(self):
        c = self.buildConnManager([('hello', 'hello my friend!')])
        c.sendText('hello')
        self.assert_(c._s_core._messages == ['hello my friend!'])
        self.assert_(c._echo == ['hello'])

    def testSendTextWithAlias2(self):
        c = self.buildConnManager([('hello', 'hello my friend!')])
        c.sendText('look;hello')
        self.assert_(c._s_core._messages == ['look', 'hello my friend!'])
        self.assert_(c._echo == ['look;hello'])

    def testSendTextWithAlias3(self):
        c = self.buildConnManager([('walk', 's;e;e;s;e')])
        c.sendText('walk')
        self.assert_(c._s_core._messages == ['s', 'e', 'e', 's', 'e'])
        self.assert_(c._echo == ['walk'])

    def testSendTextWithAlias4(self):
        c = self.buildConnManager([('goodbye', 'hello;s;s'),
                                   ('hello', 'say Hello!')])
        c.sendText('goodbye;quit')
        self.assert_(c._s_core._messages == ['say Hello!', 's', 's', 'quit'])
        self.assert_(c._echo == ['goodbye;quit'])

if __name__ == '__main__':
    unittest.main()


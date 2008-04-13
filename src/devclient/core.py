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
import select
import socket
import struct
import cPickle
import logging
import os.path
import telnetlib
from os.path import dirname, join
from optparse import OptionParser

import conf
import messages
import exception
import constants
from conf import config
from parse import getParser
from servers import getServer

logger = logging.getLogger('core')


class SocketToServer(object):
    """
    Provide a socket interface to Mud server.
    """

    encoding = "ISO-8859-1"

    def __init__(self, timeout=1):
        # setting a default timeout is the only way to set a timeout for the
        # Telnet object before establish the connection.
        socket.setdefaulttimeout(timeout)
        self.connected = 0
        self._t = telnetlib.Telnet()

    def connect(self, host, port):
        try:
            self._t.open(host, port)
        except socket.error:
            raise exception.ConnectionRefused()
        self.connected = 1

    def fileno(self):
        """
        Return the fileno() of the socket object used internally.
        """

        return self._t.get_socket().fileno()

    def read(self):
        """
        Read data from socket and return a unicode string.
        """

        try:
            return unicode(self._t.read_very_eager(), self.encoding)
        except (EOFError, socket.error):
            # disconnection must be called outside this class to remove
            # the socket from the list of sockets watched.
            raise exception.ConnectionLost()

    def write(self, msg):
        self._t.write(msg.encode(self.encoding) + "\n")

    def disconnect(self):
        if self.connected:
            self._t.close()
            self.connected = 0

    def __del__(self):
        self.disconnect()


class SocketToGui(object):
    """
    Provide a socket interface to `Gui` part of client.
    """

    def __init__(self, port=7890, timeout=.2):
        self._timeout = timeout
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._s.bind(('localhost', port))
        self._s.settimeout(self._timeout)
        self._s.listen(1)

    def fileno(self):
        """
        Return the fileno() of the socket object used internally.
        """

        return self._s.fileno()

    def accept(self):
        """
        Accept a connection.

        :return: the socket object usable to send and receive data.
        """

        self._conn = self._s.accept()[0]
        self._conn.settimeout(self._timeout)
        return self._conn

    def read(self):
        """
        Read a message.

        :return: a tuple of the form (<message type>, <message>)
        """

        size = self._conn.recv(struct.calcsize("L"))
        try:
            size = struct.unpack('>l', size)[0]
        except struct.error:
            return (messages.UNKNOWN, '')

        if size < 0:
            return (messages.UNKNOWN, '')

        data = []
        try:
            while size > 0:
                data.append(self._conn.recv(min(4096, size)))
                size -= len(data[-1])

            return cPickle.loads(''.join(data))

        except (socket.error, cPickle.BadPickleGet):
            return (messages.UNKNOWN, '')

    def write(self, cmd, message):
        """
        Send a message.

        :Parameters:
          cmd : int
            the message type

          message : object
            the message to sent
        """

        buf = cPickle.dumps((cmd, message))
        self._conn.send(struct.pack('>l', len(buf)))
        self._conn.sendall(buf)

    def __del__(self):
        self._conn.close()
        self._s.close()


class Core(object):
    """
    Main class for the core part of client.
    """

    def __init__(self, port):
        """
        Create the `Core` instance.
        """

        self.s_server = SocketToServer()
        """the interface with mud server, an instance of `SocketToServer`"""

        self.s_gui = SocketToGui(port)
        """the interface with `Gui`, an instance of `SocketToGui`"""

        self.parser = None
        """the `Parser` instance, used to parse data from server"""

        self.setupLogger()

    def setupLogger(self):
        """
        Setup the root logger from configuration params.
        """

        level = {'CRITICAL': logging.CRITICAL,
                 'ERROR': logging.ERROR,
                 'WARNING': logging.WARNING,
                 'INFO': logging.INFO,
                 'DEBUG': logging.DEBUG }

        format = '%(asctime)s %(levelname)s %(message)s'
        datefmt = '%d %b %Y %H:%M:%S'

        if int(config['logger']['log_on_file']):
            log_file = join(config['logger']['path'],'devclient.log')
            logging.basicConfig(level=level[config['logger']['level']],
                                format=format,
                                datefmt=datefmt,
                                filename=log_file,
                                filemode='a+')
        else:
            logging.basicConfig(level=level[config['logger']['level']],
                                format=format,
                                datefmt=datefmt,
                                stream=sys.stdout)

        logging.debug('*** START %s ***' % constants.PROJECT_NAME.upper())

    def _readDataFromGui(self, sock_watched):
        """
        Read data from `Gui`

        :Parameters:
          sock_watched : list
            the list of sockets watched for events

        :return: a boolean equal to False when client must exit.
        """

        cmd, msg = self.s_gui.read()
        if cmd == messages.MSG and self.s_server.connected:
            self.s_server.write(msg)
        elif cmd == messages.CUSTOM_PROMPT:
            self.parser.setVars({'custom_prompt': msg})
        elif cmd == messages.END_APP:
            return False
        elif cmd == messages.CONNECT:
            if self.s_server.connected:
                sock_watched.remove(self.s_server)
                self.s_gui.write(messages.CONN_CLOSED, '')
                self.s_server.disconnect()
            try:
                self.s_server.connect(*msg[1:3])
            except exception.ConnectionRefused:
                self.s_gui.write(messages.CONN_REFUSED, "")
            else:
                sock_watched.append(self.s_server)
                self.s_gui.write(messages.CONN_ESTABLISHED, msg[:3])

            self.parser = getParser(getServer(*msg[1:3]), msg[3:])
        elif cmd == messages.UNKNOWN:
            logger.warning('SocketToGui: Unknown message')

        return True

    def _readDataFromServer(self, sock_watched):
        try:
            data = self.s_server.read()
        except exception.ConnectionLost:
            sock_watched.remove(self.s_server)
            self.s_gui.write(messages.CONN_LOST, '')
            self.s_server.disconnect()
        else:
            if data:
                self.s_gui.write(messages.MODEL, self.parser.buildModel(data))

    def mainLoop(self):
        """
        Realize the main loop of core.

        Manage `SocketToServer` input/output and take care of exchange messages
        with the `Gui` part via `SocketToGui` instance object.
        """

        sock_watched = [self.s_gui]

        while 1:
            try:
                r, w, e = select.select(sock_watched, [], [])
            except (select.error, socket.error):
                break

            for s in r:
                if s == self.s_server:
                    self._readDataFromServer(sock_watched)
                # connection request from Gui
                elif s == self.s_gui:
                    sock_watched.append(self.s_gui.accept())
                elif not self._readDataFromGui(sock_watched):
                    return


def main():
    """
    This function is the startup of the process `Core`.
    """

    parser = OptionParser()
    parser.add_option('-c', '--config', help='the configuration file')
    parser.add_option('-p', '--port', type='int', default=7890,
                      help='the port listen for connection (default %default)')
    o, args = parser.parse_args()

    os.chdir(join(os.getcwd(), dirname(o.config)))
    conf.loadConfiguration(os.path.basename(o.config))
    sys.path.append(conf.config['servers']['path'])
    core = Core(o.port)
    core.mainLoop()

if __name__ == '__main__':
    main()
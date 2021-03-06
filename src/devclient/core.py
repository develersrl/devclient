﻿#!/usr/bin/env python
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
import zlib
import select
import socket
import struct
import cPickle
import logging
import os.path
from os.path import dirname, join
from optparse import OptionParser

import conf
import messages
import exception
import constants
from conf import config
from parse import getParser
from servers import getServer
from utils import getExceptionInfo, sendMail

logger = logging.getLogger('core')


# Telnet protocol characters
IAC  = chr(255)
DONT = chr(254)
DO   = chr(253)
WONT = chr(252)
WILL = chr(251)
theNULL = chr(0)

SB =  chr(250)
SE  = chr(240)

MCCP2 = chr(86)
MCCP = chr(85)


class SocketToServer(object):
    """
    Provide a socket interface to Mud server.

    This class handles some of TELNET negoziation sequences (see `RFC854`_ and
    `RFC855`_), however is not intended to replace the telnetlib module of
    standard library, but to provide a fast implementation of some sequences
    specific for MUD, as the `MCCP protocol`_.

.. _RFC854: http://www.rfc-editor.org/rfc/rfc854.txt
.. _RFC855: http://www.rfc-editor.org/rfc/rfc855.txt
.. _MCCP protocol: http://mccp.smaugmuds.org/protocol.html
    """

    encoding = "ISO-8859-1"

    def __init__(self, timeout=1):
        self._timeout = timeout
        self.connected = 0
        self._debug = 0

    def connect(self, host, port):
        self._stats = [0, 0]
        self._mccp_ver = None
        self._compress = 0
        self._rawbuf = ''
        self._buffer = ''
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # timeout on connect is longer than normal to avoid fake connection
        # refused.
        self._s.settimeout(self._timeout * 3)

        try:
            self._s.connect((host, port))
        except socket.error:
            raise exception.ConnectionRefused()

        self._msg('Connection established with %s:%d', host, port)
        self._s.settimeout(self._timeout)
        self.connected = 1

    def fileno(self):
        """
        Return the fileno() of the socket object used internally.
        """

        return self._s.fileno()

    def _msg(self, msg, *args):
        if not self._debug:
            return

        if args:
            msg = msg % args

        print msg

    def _processIACSeq(self):
        """
        Process one or more IAC sequences, refusing all options with the
        exception of the MCCP sequence.
        """

        # the subnegoziation sequence, which is used to mark the start of
        # compresses stream
        MCCP_SUB = (SB + MCCP + WILL + SE, SB + MCCP2 + IAC + SE)

        while len(self._buffer) >= 3 and self._buffer[0] == IAC:
            cmd = self._buffer[1]
            opt = self._buffer[2]

            if cmd in (DO, DONT):
                self._msg('IAC %s %d', ('DO', 'DONT')[cmd == DONT], ord(opt))
                self._s.sendall(IAC + WONT + opt)
                self._buffer = self._buffer[3:]
            elif cmd in (WILL, WONT):
                self._msg('IAC %s %d', ('WILL', 'WONT')[cmd == WONT], ord(opt))
                if cmd == WILL and opt == MCCP2 and not self._mccp_ver:
                    self._s.sendall(IAC + DO + opt)
                    self._msg('ENABLE MCCP v2')
                    self._mccp_ver = 2
                elif cmd == WILL and opt == MCCP and not self._mccp_ver:
                    self._s.sendall(IAC + DO + opt)
                    self._msg('ENABLE MCCP v1')
                    self._mccp_ver = 1
                else:
                    self._s.sendall(IAC + DONT + opt)
                self._buffer = self._buffer[3:]
            elif cmd == SB:
                if self._buffer[1:5] in MCCP_SUB:
                    self._msg('START COMPRESSED STREAM (MCCP v%d)',
                              self._mccp_ver)
                    self._rawbuf = self._buffer[5:] + self._rawbuf
                    self._d = zlib.decompressobj(15)
                    self._compress = 1
                    self._buffer = ''
                    self._processRawBuf()
                else:
                    pos = self._buffer.find(IAC + SE, 2)
                    if pos != -1:
                        self._msg('SUBNEGOZIATION OPTION: %d', ord(opt))
                        self._msg('SUBNEGOZIATION PARAMETERS: %s',
                                  self._buffer[3:pos])
                        self._buffer = self._buffer[pos + 2:]
                    else:
                        # to avoid non-terminating loop (but waiting for SE)
                        # Note that if the server don't send SE the processing
                        # is blocked here!
                        break
            else:
                self._msg('UNKNOWN COMMAND: %d', ord(cmd))
                self._buffer = self._buffer[2:]

    def _processRawBuf(self):
        """Process all data found in `self._rawbuf`"""

        if self._compress and self._rawbuf:
            new_data = self._d.decompress(self._rawbuf) + self._d.unused_data
            if self._d.unused_data:
                self._msg('END OF COMPRESSED STREAM (MCCP v%d)', self._mccp_ver)
                self._compress = 0
                self._d = None
        else:
            new_data = self._rawbuf

        if self._debug:
            self._stats[0] += len(self._rawbuf)
            self._stats[1] += len(new_data)

        self._buffer += new_data
        self._rawbuf = ''

    def _getData(self):
        """
        Return all data in `self._buffer` until IAC char.
        """

        self._processIACSeq()
        pos = self._buffer.find(IAC)
        if pos != -1:
            data = self._buffer[:pos]
            self._buffer = self._buffer[pos:]
        else:
            data, self._buffer = self._buffer, ''
        return data.replace(theNULL, '')

    def _process(self):
        data = []
        self._processRawBuf()
        buf = self._getData()
        while buf:
            data.append(buf)
            buf = self._getData()

        # self._buffer is empty unless it ends with an incomplete IAC sequence.
        return ''.join(data)

    def read(self):
        """
        Read data from socket and return a unicode string.
        """

        try:
            buf = self._s.recv(1024)
            if not buf:
                raise EOFError
            self._rawbuf += buf
            return unicode(self._process(), self.encoding)
        except (EOFError, socket.error):
            # disconnection must be called outside this class to remove
            # the socket from the list of sockets watched.
            raise exception.ConnectionLost()

    def write(self, msg):
        msg = msg.encode(self.encoding).replace(IAC, IAC + IAC)
        self._s.sendall(msg + "\n")

    def disconnect(self):
        if self.connected:
            if self._debug:
                self._msg('%s CONNECTION STATS %s', '*' * 20, '*' * 20)
                self._msg(' Original data received: %d', self._stats[0])
                self._msg(' Uncompress total data: %d', self._stats[1])
                self._msg('*' * 58)
            self._s.close()
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
        self._s.settimeout(None)
        self._s.connect(('localhost', port))
        self._s.settimeout(self._timeout)

    def fileno(self):
        """
        Return the fileno() of the socket object used internally.
        """

        return self._s.fileno()

    def read(self):
        """
        Read a message.

        :return: a tuple of the form (<message type>, <message>) or None if
          the connection with the gui is lost.
        """

        size = self._s.recv(struct.calcsize("L"))
        if not size:
            return None

        try:
            msg_size = struct.unpack('>l', size)[0]
        except struct.error:
            return (messages.UNKNOWN, '')

        if msg_size < 0:
            return (messages.UNKNOWN, '')

        data = []
        try:
            while msg_size > 0:
                msg = self._s.recv(min(4096, msg_size))
                if not msg:
                    return None

                data.append(msg)
                msg_size -= len(msg)

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
        self._s.send(struct.pack('>l', len(buf)))
        self._s.sendall(buf)

    def __del__(self):
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

        self._sock_watched = [self.s_gui]
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

    def _readDataFromGui(self, cmd, msg):
        """
        Read data from the `Gui`.
        :return: a boolean equal to False when client must exit.
        """

        if cmd == messages.MSG and self.s_server.connected:
            self.s_server.write(msg)
        elif cmd == messages.CUSTOM_PROMPT:
            self.parser.setVars({'custom_prompt': msg})
        elif cmd == messages.END_APP:
            return False
        elif cmd == messages.CONNECT:
            if self.s_server.connected:
                self._sock_watched.remove(self.s_server)
                self.s_gui.write(messages.CONN_CLOSED, '')
                self.s_server.disconnect()
            try:
                self.s_server.connect(*msg[1:3])
            except exception.ConnectionRefused:
                self.s_gui.write(messages.CONN_REFUSED, "")
            else:
                self._sock_watched.append(self.s_server)
                self.s_gui.write(messages.CONN_ESTABLISHED, msg[:3])

            self.parser = getParser(getServer(*msg[1:3]), msg[3:])
        elif cmd == messages.UNKNOWN:
            logger.warning('SocketToGui: Unknown message')

        return True

    def _readDataFromServer(self):
        try:
            data = self.s_server.read()
        except exception.ConnectionLost:
            self._sock_watched.remove(self.s_server)
            self.s_gui.write(messages.CONN_LOST, '')
            self.s_server.disconnect()
            return False
        else:
            if data:
                self.s_gui.write(messages.MODEL, self.parser.buildModel(data))
            return True

    def mainLoop(self, exit_on_close=False):
        """
        Realize the main loop of core.

        Manage `SocketToServer` input/output and take care of exchange messages
        with the `Gui` part via `SocketToGui` instance object.
        """

        while 1:
            try:
                r, w, e = select.select(self._sock_watched, [], [])
            except (select.error, socket.error):
                break

            for s in r:
                if s == self.s_server:
                    if not self._readDataFromServer() and exit_on_close:
                        return
                else:
                    data = self.s_gui.read()
                    if not data:
                        logger.warning('Core: exit because of Gui connection lost')
                        return

                    cmd, msg = data
                    if not self._readDataFromGui(cmd, msg):
                        return


def main():
    """
    This function is the startup of the process `Core`.
    """

    parser = OptionParser()
    parser.add_option('-c', '--config', help='the configuration file')
    parser.add_option('-p', '--port', type='int', default=7890,
                      help='the port used to connect to the ui (default %default)')
    o, args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.error("No arguments supplied")
    os.chdir(join(os.getcwd(), dirname(o.config)))
    conf.loadConfiguration(os.path.basename(o.config))
    sys.path.append(conf.config['servers']['path'])
    core = Core(o.port)
    try:
        core.mainLoop()
    except Exception, e:
        print 'Fatal Exception:', e
        info = getExceptionInfo()
        fd = open(join(config['exceptions']['save_path'], 'exception.txt'), 'a+')
        fd.write(info)
        fd.close()
        
        if config['exceptions']['send_email']:
            try:
                sendMail("DevClient fatal exception: %s" % e, info)
            except Exception, e:
                print 'Error while sending email:', e



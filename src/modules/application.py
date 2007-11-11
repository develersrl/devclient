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

import copy
import Queue

from modules.parser import Parser
from modules.socket import Socket
import exception
import event_type

class Application(object):
    """
    Main class for the application part of client.
    """

    def __init__(self, classes, q_app_gui, q_gui_app):
        """
        Create the `Application` instance.

        :Parameters:
          classes : dict
            a dictionary of the form {<className>: <classRef> } that
            contains all the specific classes use in client.
          q_app_gui : Queue
            a Queue used to send message from `Application` to `Gui`
          q_gui_app : Queue
            a Queue used to send message from `Gui` to `Application`
        """

        self.classes = classes
        self.q_app_gui = q_app_gui
        self.q_gui_app = q_gui_app

        self.sock = Socket()

    def mainLoop(self):
        """
        Realize the main loop of application.

        Manage `Socket` input/output and take care of exchange messages with
        the `Gui` part.
        """

        parser = None

        while 1:

            if self.sock.connected:
                data = self.sock.read()
                if data:
                    parser.parse(data)
                    self.q_app_gui.put((event_type.MODEL,
                                        copy.deepcopy(parser.model)))

            try:
                cmd, msg = self.q_gui_app.get(0)
                if cmd == event_type.MSG and self.sock.connected:
                    self.sock.write(msg)
                elif cmd == event_type.END_APP:
                    self.sock.disconnect()
                    return
                elif cmd == event_type.CONNECT and not self.sock.connected:
                    parser = Parser()
                    try:
                        self.sock.connect(*msg)
                    except exception.ConnectionRefused:
                        self.q_app_gui.put((event_type.CONNECTION_REFUSED, ""))
            except Queue.Empty:
                pass

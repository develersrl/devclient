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

import sys
import time
import socket
import optparse


def main():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--port', type='int', default=6666)
    parser.add_option('-d', '--delay', type='int', default=1)
    parser.add_option('-f', '--datafile', default='', dest='datafile')
    o, args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", o.port))
    s.listen(1)
    print 'READY'
    conn, addr = s.accept()

    if o.datafile:
        f = open(o.datafile)
        data = f.read()
        f.close()

        while data:
            conn.send(data[:1024])
            data = data[1024:]
            time.sleep(o.delay / 100.0)
    else:
        while 1:
            data = conn.recv(1024)
            if not data: 
                break

    conn.close()


if __name__ == '__main__':
    main()


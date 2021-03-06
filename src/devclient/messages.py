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

UNKNOWN = 0
MSG = 1
MODEL = 2
END_APP = 3
CONNECT = 4
CONN_REFUSED = 5
CONN_ESTABLISHED = 6
CONN_CLOSED = 7
CONN_LOST = 8
CUSTOM_PROMPT = 9


class Model(object):
    """
    Rappresent a model of data that can be viewed by a viewer.
    """

    def __init__(self):
        self.main_text = ''
        self.main_html = ''
        self.original_text = ''
        self.map_html = ''
        self.map_text = ''
        self.prompt = None
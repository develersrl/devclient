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

from generics import *

class DdE(DikuServer):
    wild_chars = '\^\.xX@\*\s&-\?'
    wild_end_text = '\n[Uscite:'
    room_map = '|\-#?@'
    player_char = 'X'
    cmd_new_player = 'nuovo'
    host = 'dde.homelinux.com'
    port = 5000
    host2 = 'dde.homelinux.com'
    port2 = 4000
    map_width = 27
    map_height = 11


class ADdE(DdE):
    wild_chars = '\^\.xX@\*\s&-\?o'
    host = 'algor.homelinux.com'
    port = 5556
    host2 = None
    port2 = None


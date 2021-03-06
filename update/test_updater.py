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

import unittest

import updater

class TestUpdater(unittest.TestCase):
    def testBadDomain(self):
        url = 'https://www.devler.com/~aleister/devclient/devclient.tgz'
        self.assertRaises(updater.UpdaterError, updater.downloadFile, url)

    def testBadFilename(self):
        url = 'https://www.develer.com/~aleister/devclient/devlient.tgz'
        self.assertRaises(updater.UpdaterError, updater.downloadFile, url)

    def testBadUrl(self):
        url = 'htps://www.develer.com/~aleister/devclient/devclient.tgz'
        self.assertRaises(updater.UpdaterError, updater.downloadFile, url)


if __name__ == '__main__':
    unittest.main()
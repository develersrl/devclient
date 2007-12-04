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
import unittest

sys.path.append('..')

from devclient.parser import Parser, SmaugParser, AfkParser

class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def testParseText(self):
        txt = 'hello'
        self.parser.parse(txt)
        self.assert_([txt] == self.parser.model.main_text.get())

    def testParseTextMultiline(self):
        txt = 'hello\nworld'
        self.parser.parse(txt)
        self.assert_([txt.replace('\n','<br>')] ==
                     self.parser.model.main_html.get())

    def testParseMultiText(self):
        txt1, txt2 = 'hello', 'world'
        self.parser.parse(txt1)
        self.parser.parse(txt2)
        self.assert_([txt1, txt2] == self.parser.model.main_html.get())

    def testParseMultiText2(self):
        txt1, txt2 = 'hello\x1b[0;', '33mworld'
        self.parser.parse(txt1)
        self.parser.parse(txt2)

        self.assert_(['hello', 'world'] == self.parser.model.main_text.get())

        self.assert_(self.parser._normal_color[3] ==
                     self.parser.model.main_fgcolor)

    def testParseMultiText3(self):
        txt1, txt2 = 'hello\x1b', '[0;33mworld'
        self.parser.parse(txt1)
        self.parser.parse(txt2)

        self.assert_(['hello', 'world'] == self.parser.model.main_text.get())

        self.assert_(self.parser._normal_color[3] ==
                     self.parser.model.main_fgcolor)

    def testParseSpace(self):
        txt = 'hello world'
        self.parser.parse(txt)
        self.assert_([txt.replace(' ','&nbsp;')] ==
                     self.parser.model.main_html.get())

    def testEvalStyle1(self):
        self.parser._evalStyle('31')
        self.assert_(self.parser._normal_color[1] ==
                     self.parser.model.main_fgcolor)

    def testEvalStyle2(self):
        self.parser._evalStyle('0;42')
        self.assert_(self.parser._normal_color[2] ==
                     self.parser.model.main_bgcolor)

    def testEvalStyle3(self):
        self.parser._evalStyle('35;40')
        self.assert_(self.parser._normal_color[0] ==
                     self.parser.model.main_bgcolor)
        self.assert_(self.parser._normal_color[5] ==
                     self.parser.model.main_fgcolor)

    def testEvalStyle4(self):
        self.parser._evalStyle('1;36;41')
        self.assert_(self.parser._normal_color[1] ==
                     self.parser.model.main_bgcolor)
        self.assert_(self.parser._bright_color[6] ==
                     self.parser.model.main_fgcolor)

    def testEvalStyle5(self):
        self.parser._evalStyle('0;42')
        style = self.parser._evalStyle('0;42')
        self.assert_(style == '')

    def testEvalStyle6(self):
        self.parser._evalStyle('0;42')
        style = self.parser._evalStyle('0;41')
        self.assert_(style == 'background-color:#%s' %
                               self.parser._normal_color[1])

    def testReplaceAnsiColor(self):
        txt = '\x1b[33mhello'
        html_res, text_res = self.parser._replaceAnsiColor(txt)
        self.assert_(text_res == 'hello' and html_res == 'hello')
        self.assert_(self.parser.model.main_fgcolor ==
                     self.parser._normal_color[3])

    def testReplaceAnsiColor2(self):
        self.parser._evalStyle('31')
        txt = '\x1b[33mhello'
        html_res, text_res = self.parser._replaceAnsiColor(txt)

        self.assert_(html_res == '<span style="color:#%s">hello</span>' %
                     self.parser._normal_color[3])

    def testReplaceAnsiColor3(self):
        self.parser._evalStyle('31')
        txt = '\x1b[33mhello'
        html_res, text_res = self.parser._replaceAnsiColor(txt)

        self.assert_(text_res == 'hello')

    def testReplaceEmptyColor(self):
        txt = '\x1b[mhello'
        html_res, text_res = self.parser._replaceAnsiColor(txt)
        self.assert_(html_res == 'hello' and text_res == 'hello')


class TestSmaugParser(unittest.TestCase):

    def setUp(self):
        self.parser = SmaugParser()

    def testEmptyPrompt(self):
        self.assert_(self.parser.model.prompt is None)

    def testFakePrompt(self):
        stats = {'Hp' : '23/24', 'Mn': '102/102', 'Mv': '26/102'}
        p = 'PF:%(Hp)s Mn:%(Mn)s Mv:%(Mv)s' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        self.assert_(self.parser.model.prompt is None)

    def testPrompt1(self):
        stats = {'Hp' : '23/24', 'Mn': '102/102', 'Mv': '26/102'}
        p = 'PF:%(Hp)s Mn:%(Mn)s Mv:%(Mv)s>' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('/') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)

    def testPrompt2(self):
        stats = {'Hp' : '23/24', 'Mn': '102/102', 'Mv': '26/102'}
        p = 'PF:%(Hp)s Mn:%(Mn)s Mv:%(Mv)s bla bla bla>' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('/') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)

    def testPrompt3(self):
        stats = {'Hp' : '23/24', 'Mn': '102/102', 'Mv': '26/102'}
        p = 'PF:  %(Hp)s Mn:  %(Mn)s Mv:  %(Mv)s>' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('/') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)

    def testPrompt4(self):
        stats = {'Hp' : '23/24', 'Mn': '102/102', 'Mv': '26/102'}
        p = 'pf:  %(Hp)s mn:  %(Mn)s Mv:  %(Mv)s>' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('/') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)


class TestAfkParser(unittest.TestCase):

    def setUp(self):
        self.parser = AfkParser()

    def testEmptyPrompt(self):
        self.assert_(self.parser.model.prompt is None)

    def testFakePrompt(self):
        stats = {'Hp' : '23-24', 'Mn': '102-102', 'Mv': '26-102'}
        p = '[pf: %(Hp)s] [mana:%(Mn)s] [mv:%(Mv)s] [mon:0]' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        self.assert_(self.parser.model.prompt is None)

    def testPrompt1(self):
        stats = {'Hp' : '23-24', 'Mn': '102-102', 'Mv': '26-102'}
        p = '[Pf:%(Hp)s] [Mana:%(Mn)s] [Mv:%(Mv)s] [Mon:0] [S:Xp:0]' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('-') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)

    def testPrompt2(self):
        stats = {'Hp' : '23-24', 'Mn': '102-102', 'Mv': '26-102'}
        p = '[Pf: %(Hp)s] [Mana: %(Mn)s] [Mv: %(Mv)s] [Mon: 0] [S:Xp:0]' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('-') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)

    def testPrompt3(self):
        stats = {'Hp' : '23-24', 'Mn': '102-102', 'Mv': '26-102'}
        p = '[pf: %(Hp)s] [mana:%(Mn)s] [mv:%(Mv)s] [mon:0] [s:xp: 0]' % stats
        self.parser.model.main_text.append(p)
        self.parser._parsePrompt()

        prompt = dict(zip(stats.keys(), [v.split('-') for v in stats.values()]))
        self.assert_(self.parser.model.prompt == prompt)


if __name__ == '__main__':
    unittest.main()

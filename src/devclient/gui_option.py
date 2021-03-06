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

from re import compile
from os.path import join

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, Qt, QVariant, QTimeLine, QPoint
from PyQt4.QtGui import QDialog, QColorDialog, QMessageBox
from PyQt4.QtGui import QPixmap, QWidget, QPainter, QLabel, QVBoxLayout

import storage
from conf import config
from utils import keypad_codes
from gui_src.gui_option import Ui_option


_CLICKED = SIGNAL("clicked()")

def _setLabelColor(label, color):
    """
    Set the background color of a label, or unset if color is empty.
    """

    if not color:
        return _clearLabelColor(label)

    style = unicode(label.styleSheet())
    reg = compile('QLabel\s*{\s*background-color\s*:\s*(#\w{6}).*}')
    m = reg.search(style)
    if m:
        l, r = m.span(1)
        style = style[:l] + color + style[r:]
    else:
        style += "QLabel{background-color:%s;}" % color

    label.setStyleSheet(style)


def _clearLabelColor(label):
    """
    Unset the background color of a label.
    """

    style = unicode(label.styleSheet())
    reg = compile('QLabel\s*{\s*(background-color\s*:\s*#\w{6}\s*;?)(.*)}')
    m = reg.search(style)
    if m:
        l, r = m.span(1 if m.group(2).strip() else 0)
        style = style[:l] + style[r:]
    label.setStyleSheet(style)


def _changeItemSelected(combobox, name):
    """
    Change the selected item of a combobox.
    """

    if combobox.count():
        for i in xrange(combobox.count()):
            if name == unicode(combobox.itemText(i)):
                combobox.setCurrentIndex(i)
                return True

    return False


class TransitionWidget(QWidget):
    """
    This class implements a transition effect between two pixmaps.

    Starts the transition with the method `start` and emit the signal finished()
    when the transition is done.
    """

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self._timeline = QTimeLine(400, self)
        self._blending_factor = 0.0
        self.connect(self._timeline, SIGNAL("valueChanged(qreal)"),
                     self._triggerRepaint)
        self.connect(self._timeline, SIGNAL("finished()"), SIGNAL("finished()"))

    def start(self, prev_pixmap, next_pixmap):
        self._prev_pixmap = prev_pixmap
        self._next_pixmap = next_pixmap
        self._timeline.start()

    def stop(self):
        self._timeline.stop()

    def _triggerRepaint(self, value):
        self._blending_factor = value
        self.update()

    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        if self._timeline.state() == QTimeLine.NotRunning:  # nothing to do
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.SmoothPixmapTransform, True)
        p.drawPixmap(QPoint(0, 0), self._prev_pixmap)
        p.setOpacity(self._blending_factor)
        p.drawPixmap(QPoint(0, 0), self._next_pixmap)


class FormConnection(object):
    """
    Manage the connection part of gui option.
    """

    def __init__(self, widget):
        self.w = widget
        self.w.port_conn.setValidator(QtGui.QIntValidator(self.w.port_conn))

        self.connections = storage.connections()
        for el in self.connections:
            self.w.list_conn.addItem(el[1], QVariant(el[0]))
        self._setupSignal()
        self._text = self.w._text

    def _setupSignal(self):
        self.w.connect(self.w.save_conn, _CLICKED, self.save)
        self.w.connect(self.w.delete_conn, _CLICKED, self.delete)
        self.w.connect(self.w.list_conn, SIGNAL("currentIndexChanged(QString)"),
                       self.load)

    def load(self, name):
        """
        Load data of one connection.

        :Parameters:
          name : str
            the name of connection to load
        """

        conn = [el for el in self.connections if el[1] == name]

        if conn:
            n, h, p = conn[0][1:]
            connect = True
        else:
            n, h, p = ('', '', '')
            connect = False

        self.w.name_conn.setText(n)
        self.w.host_conn.setText(h)
        self.w.port_conn.setText(unicode(p))

    def _checkFields(self):
        """
        Check validity of fields.
        """

        msg = []

        conn_fields = {self._text['Name']: self.w.name_conn,
                       self._text['Host']: self.w.host_conn,
                       self._text['Port']: self.w.port_conn}

        for text, field in conn_fields.iteritems():
            if not field.text():
                msg.append(unicode(text))

        if msg:
            self.w._displayWarning(self._text['Connection'],
                "%s:\n%s" % (self._text['ReqFields'], '\n'.join(msg)))
            return False

        if not self.w.list_conn.currentIndex():
            id_conn = 0
        else:
            data = self.w.list_conn.itemData(self.w.list_conn.currentIndex())
            id_conn = data.toInt()[0]

        if [el[0] for el in self.connections if
            el[1] == self.w.name_conn.text() and el[0] != id_conn]:
            self.w._displayWarning(self._text['Connection'],
                                   self._text['UniqueName'])
            return False

        return True

    def save(self):
        """
        Save a connection after check the fields validity.
        """

        if not self._checkFields():
            return

        if not self.w.list_conn.currentIndex():
            id_conn = 0
        else:
            data = self.w.list_conn.itemData(self.w.list_conn.currentIndex())
            id_conn = data.toInt()[0]

        conn = [id_conn,
                unicode(self.w.name_conn.text()),
                unicode(self.w.host_conn.text()),
                int(self.w.port_conn.text())]

        if not self.w.list_conn.currentIndex():
            storage.addConnection(conn)
            self.w.list_conn.addItem(self.w.name_conn.text(), QVariant(conn[0]))
            self.connections.append(conn)
        else:
            self.connections[self.w.list_conn.currentIndex() - 1] = conn
            self.w.list_conn.setItemText(self.w.list_conn.currentIndex(),
                                         conn[1])
            storage.updateConnection(conn)

        self.w.list_conn.setCurrentIndex(0)
        self.w.emit(SIGNAL('reloadConnData(QString)'), '')
        self.load('')

    def delete(self):
        """
        Erase a connection.
        """

        if self.w.list_conn.currentIndex() <= 0:
            return

        if storage.connectionHasChild(unicode(self.w.list_conn.currentText())) \
           and not self.w._displayQuestion(self._text['Connection'],
                                           self._text['ConfirmDelete']):
            return

        index = self.w.list_conn.currentIndex() - 1
        storage.deleteConnection(self.connections[index])
        self.w.list_conn.removeItem(self.w.list_conn.currentIndex())
        self.w.emit(SIGNAL('reloadConnData(QString)'), '')
        del self.connections[index]


class FormOption(object):
    def __init__(self, widget):
        self.w = widget
        self._text = self.w._text
        self._conn_combobox = self._getComboboxConnection()
        self.loadForm()
        # To propagate who is the current connection selected
        if self._conn_combobox:
            self.w.connect(self._conn_combobox,
                           SIGNAL("currentIndexChanged(QString)"),
                           self.w, SIGNAL("currentConnChanged(QString)"))

        self._setupSignal()

    def loadForm(self):
        raise NotImplementedError()

    def _getComboboxConnection(self):
        return None

    def disableSignal(self, disable):
        pass

    def _setupSignal(self):
        pass

    def _updateConnection(self):
        """
        Change the connection selected in the combobox argument and return
        the connection name (or None if there aren't connections defined).
        """

        if not self._conn_combobox.count():
            return None

        if _changeItemSelected(self._conn_combobox, self.w._lazy_conn):
            return self.w._lazy_conn

        return unicode(self._conn_combobox.currentText())


class FormMacro(FormOption):
    """
    Manage the macro part of gui option.
    """

    def __init__(self, widget):
        self._key_descr = {}
        for k, v in Qt.__dict__.iteritems():
            if k.startswith('Key_'):
                self._key_descr[v] = k[4:]

        self.start_reg = False
        FormOption.__init__(self, widget)

    def _getComboboxConnection(self):
        return self.w.list_conn_macro

    def loadForm(self):
        connections = storage.connections()
        self.w.list_conn_macro.clear()
        self.w.list_conn_macro.addItems([c[1] for c in connections])

        for o in (self.w.list_macro, self.w.command_macro,
                  self.w.register_macro):
            o.setEnabled(bool(self.w.list_conn_macro.count()))

        conn_name = self._updateConnection()
        self.loadMacros(conn_name, True)

    def disableSignal(self, disable):
        self.w.list_macro.blockSignals(disable)
        self.w.list_conn_macro.blockSignals(disable)

    def _setupSignal(self):
        self.w.connect(self.w.register_macro, _CLICKED, self._register)
        self.w.connect(self.w.save_macro, _CLICKED, self.save)
        self.w.connect(self.w.delete_macro, _CLICKED, self.delete)
        self.w.connect(self.w.list_conn_macro,
                       SIGNAL("currentIndexChanged(QString)"),
                       self.loadMacros)
        self.w.connect(self.w.list_macro,
                       SIGNAL("currentIndexChanged(int)"),
                       self.load)

    def loadMacros(self, conn, signal=False):
        """
        Load all macros for a connection.

        :Parameters:
          conn : str
            the name of connection
          signal : bool
            if False the signal connected with combo must be disconnected
        """

        if not signal:
            self.disableSignal(True)

        self.macros = storage.macros(unicode(conn)) if conn else []
        self.w.list_macro.clear()
        self.w.list_macro.addItem(self._text['NewMacro'])
        self.w.list_macro.addItems([self.getKeyDescr(*m[1:]) for m in
                                    self.macros])
        if not signal:
            self.disableSignal(False)
        self._clear()

    def load(self, idx):
        if not idx:
            k, c = '', ''
            self.key_seq = None
        else:
            m = self.macros[idx - 1]
            c = m[0]
            k = self.getKeyDescr(*m[1:])
            self.key_seq = m[1:]

        self.w.keys_macro.setText(k)
        self.w.command_macro.setText(c)

    def _checkFields(self):
        """
        Check validity of fields.
        """

        msg = []

        conn_fields = {self._text['Keys']: self.w.keys_macro,
                       self._text['Command']: self.w.command_macro}

        for text, field in conn_fields.iteritems():
            if not field.text():
                msg.append(unicode(text))

        if msg:
            self.w._displayWarning(self._text['Macro'],
                "%s:\n%s" % (self._text['ReqFields'], '\n'.join(msg)))
            return False

        cur_idx = self.w.list_macro.currentIndex()
        if [el for idx, el in enumerate(self.macros) if el[1:] == self.key_seq
            and (not cur_idx or idx != cur_idx - 1)]:
            self.w._displayWarning(self._text['Macro'],
                                   self._text['UniqueKeys'])
            return False

        # FIX: the shortcuts should be read (and write) from storage
        # Format: shift, alt, ctrl, keycode
        shortcuts = [(0, 1, 0, Qt.Key_C),
                     (0, 1, 0, Qt.Key_O),
                     (0, 1, 0, Qt.Key_Q),
                     (0, 0, 0, Qt.Key_Enter),
                     (0, 0, 0, Qt.Key_Return),
                     (0, 0, 0, Qt.Key_Up),
                     (0, 0, 0, Qt.Key_Down)]

        if [el for el in shortcuts if el == self.key_seq]:
            self.w._displayWarning(self._text['Macro'],
                                   self._text['ShortcutKeys'])
            return False

        return True

    def save(self):
        if not self._checkFields():
            return

        macro = [unicode(self.w.command_macro.text())]
        macro.extend(self.key_seq)
        macro = tuple(macro)

        list_idx = self.w.list_macro.currentIndex()
        if not list_idx:
            self.macros.append(macro)
            self.w.list_macro.addItem(self.getKeyDescr(*self.key_seq))
        else:
            self.macros[list_idx - 1] = macro
            self.w.list_macro.setItemText(list_idx,
                                          self.getKeyDescr(*macro[1:]))

        conn_name = self.w.list_conn_macro.currentText()
        storage.saveMacros(unicode(conn_name), self.macros)
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)
        self._clear()

    def delete(self):

        list_idx = self.w.list_macro.currentIndex()
        if list_idx <= 0:
            return

        del self.macros[list_idx - 1]
        self.w.list_macro.removeItem(list_idx)
        conn_name = self.w.list_conn_macro.currentText()
        storage.saveMacros(unicode(conn_name), self.macros)
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)

    def _clear(self):
        self.w.list_macro.setCurrentIndex(0)
        self.load(0)
        self.w.keys_macro.setStyleSheet('')
        self.start_reg = False

    def _register(self):
        """
        Start register keyboard's event.
        """

        self.w.grabKeyboard()
        self.w.keys_macro.setText('')
        self.key_seq = None
        color = self.w.keys_macro.property('highlight_color').toString()
        self.w.keys_macro.setStyleSheet('background-color: %s' % color)
        self.start_reg = True

    def _getKeySeq(self, event):
        """
        Given a keyboard event, return a tuple of its components.

        :Parameters:
          event : QKeyEvent
            the keyboard event

        :return: a tuple of the form (shift, alt, ctrl, keycode)
        """

        def _checkModifier(event, mod):
            """
            Check keyboard's modifier.
            """

            return int((event.modifiers() & mod) == mod)

        s = _checkModifier(event, Qt.ShiftModifier)
        a = _checkModifier(event, Qt.AltModifier)
        c = _checkModifier(event, Qt.ControlModifier)
        return (s, a, c, event.key())

    def getKeyDescr(self, shift, alt, ctrl, key):
        """
        Return a readable description for a sequence of keys.

        :Parameters:
          shift : int
            1 if the shift key is pressed, 0 otherwise
          alt : int
            1 if the alt key is pressed, 0 otherwise
          ctrl : int
            1 if the control key is pressed, 0 otherwise
          key : int
            the code of key
        """

        return ('', 'Ctrl ')[ctrl] + ('', 'Alt ')[alt] + \
               ('', 'Shift ')[shift] + self._key_descr[key]

    def keyPressEvent(self, keyEvent):
        """
        Manage the event keyboard's saving the sequence of keys of a macro.
        """

        if self.start_reg and self._key_descr.has_key(keyEvent.key()) and \
           keyEvent.key() not in (Qt.Key_Shift, Qt.Key_Control,
                                  Qt.Key_Meta, Qt.Key_Alt):

            if keyEvent.nativeScanCode() in keypad_codes.values():
                self.w._displayWarning(self._text['Macro'], 
                                       self._text['KeypadKeys'])
            else:
                self.key_seq = self._getKeySeq(keyEvent)
                self.w.keys_macro.setText(self.getKeyDescr(*self.key_seq))
 
            self.w.releaseKeyboard()
            self.w.keys_macro.setStyleSheet('')
            self.start_reg = False


class FakeFormKeypad(FormOption):
    """
    A courtesy page for the platforms that don't support the keypad.
    """

    def __init__(self, widget):
        fake_page = QWidget()
        self._replacePage(widget.page_container, widget.keypad_page, fake_page)
        layout = QVBoxLayout(fake_page)
        layout.addSpacing(10)
        label = QLabel(widget._text['NoKeypad'])
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch(1)

    def _replacePage(self, container, oldpage, newpage):
        index = container.indexOf(oldpage)
        container.removeWidget(oldpage)
        del oldpage
        container.insertWidget(index, newpage)

    def loadForm(self):
        pass


class FormKeypad(FormOption):
    """
    Manage the keypad part of gui option.
    """

    def _setupSignal(self):
        self.w.connect(self.w.save_keypad, _CLICKED, self._saveKeypad)
        self.w.connect(self.w.list_conn_keypad,
                      SIGNAL("currentIndexChanged(QString)"),
                      self._loadKeypad)

    def _getComboboxConnection(self):
        return self.w.list_conn_keypad

    def loadForm(self):
        self.w.list_conn_keypad.clear()
        self.w.list_conn_keypad.addItems([c[1] for c in storage.connections()])
        conn_name = self._updateConnection()
        self.keypad = {}
        self._loadKeypad(conn_name)

    def _loadKeypad(self, conn_name):
        for f in self.w.keypad_fields.itervalues():
            f.setEnabled(bool(conn_name))

        if conn_name:
            self.keypad = storage.keypad(unicode(conn_name))
            for k, v in self.keypad.iteritems():
                self.w.keypad_fields[k].setText(v)

    def _saveKeypad(self):
        conn_name = self.w.list_conn_keypad.currentText()
        if conn_name:
            keypad = {}
            for k, f in self.w.keypad_fields.iteritems():
                keypad[k] = unicode(f.text())

            storage.saveKeypad(unicode(conn_name), keypad)

    def disableSignal(self, disable):
        self.w.list_conn_keypad.blockSignals(disable)


class FormPreferences(FormOption):
    """
    Manage the preferences part of gui option.
    """

    def _setupSignal(self):
        self.w.connect(self.w.echo_color_button, _CLICKED, self._getEchoColor)
        self.w.connect(self.w.save_preferences, _CLICKED, self.save)

    def _getEchoColor(self):
        c = QColorDialog.getColor()
        self._echo_color = unicode(c.name()) if c.isValid() else ''
        _setLabelColor(self.w.echo_color, self._echo_color)

    def loadForm(self):
        preferences = storage.preferences()
        if preferences:
            self._echo_color = preferences[0]
            _setLabelColor(self.w.echo_color, self._echo_color)
            keep_text = (Qt.Unchecked, Qt.Checked)[preferences[1]]
            self.w.keep_text.setCheckState(keep_text)
            save_log = (Qt.Unchecked, Qt.Checked)[preferences[2]]
            self.w.save_log.setCheckState(save_log)
            self.w.cmd_separator.setText(preferences[3])

    def save(self):
        preferences = (self._echo_color,
                       int(self.w.keep_text.checkState() == Qt.Checked),
                       int(self.w.save_log.checkState() == Qt.Checked),
                       unicode(self.w.cmd_separator.text()))

        storage.savePreferences(preferences)
        self.w.emit(SIGNAL('reloadPreferences()'))


class FormAccounts(FormOption):
    """
    Manage the accounts part of gui option.
    """

    def _getComboboxConnection(self):
        return self.w.list_conn_account

    def loadForm(self):
        connections = storage.connections()
        self.w.list_conn_account.clear()

        selected = 0
        for i, el in enumerate(connections):
            self.w.list_conn_account.addItem(el[1], QVariant(el[0]))
            if el[1] == self.w._lazy_conn:
                selected = i

            self.w.list_conn_account.setCurrentIndex(selected)
        if connections:
            self._loadAccounts(selected)
        val = storage.option('save_account')
        self.w.save_account.setCheckState(Qt.Checked if val else Qt.Unchecked)
        self.w.box_prompt.setVisible(False)

    def _setupSignal(self):
        change_idx = SIGNAL("currentIndexChanged(int)")
        self.w.connect(self.w.list_conn_account, change_idx, self._loadAccounts)
        self.w.connect(self.w.delete_account, _CLICKED, self.deleteAccount)
        self.w.connect(self.w.save_account, SIGNAL('stateChanged(int)'),
                       self._saveAccounts)
        self.w.connect(self.w.change_prompt, _CLICKED, self._togglePrompt)
        self.w.connect(self.w.save_prompt, _CLICKED, self._savePrompt)
        self.w.connect(self.w.list_account, change_idx, self._loadAccount)

    def _togglePrompt(self):
        self.w.box_prompt.setVisible(not self.w.box_prompt.isVisible())

    def _loadAccounts(self, idx):
        id_conn = self.w.list_conn_account.itemData(idx).toInt()[0]
        self.w.list_account.blockSignals(True)
        self.w.list_account.clear()
        accounts = storage.accounts(id_conn)
        self.w.list_account.addItems(accounts)
        self.w.list_account.blockSignals(False)
        self.w.delete_account.setEnabled(True if accounts else False)
        self.w.change_prompt.setEnabled(True if accounts else False)
        self.w.box_prompt.setVisible(False)
        self._loadAccount()

    def _loadAccount(self, i=0):
        idx = self.w.list_conn_account.currentIndex()
        id_conn = self.w.list_conn_account.itemData(idx).toInt()[0]
        username = unicode(self.w.list_account.currentText())
        if id_conn and username:
            n_prompt, f_prompt = storage.prompt(id_conn, username)
            self.w.normal_prompt.setText(n_prompt)
            self.w.fight_prompt.setText(f_prompt)

    def disableSignal(self, disable):
        self.w.list_conn_account.blockSignals(disable)
        self.w.list_account.blockSignals(disable)

    def deleteAccount(self):
        idx = self.w.list_conn_account.currentIndex()
        id_conn = self.w.list_conn_account.itemData(idx).toInt()[0]
        username = unicode(self.w.list_account.currentText())
        storage.deleteAccount(id_conn, username)
        self.w.list_account.removeItem(self.w.list_account.currentIndex())
        self.w.emit(SIGNAL('reloadConnData(QString)'), '')
        if not self.w.list_account.count():
            self.w.delete_account.setEnabled(False)
            self.w.change_prompt.setEnabled(False)

    def _saveAccounts(self, val):
        storage.setOption('save_account', int(val == Qt.Checked))

    def _savePrompt(self):
        idx = self.w.list_conn_account.currentIndex()
        id_conn = self.w.list_conn_account.itemData(idx).toInt()[0]
        username = unicode(self.w.list_account.currentText())
        normal = unicode(self.w.normal_prompt.text())
        fight = unicode(self.w.fight_prompt.text())
        d = {normal: self.w.normal_prompt, fight: self.w.fight_prompt}
        for text, field in d.iteritems():
            if text:
                for c in 'hHmMvV':
                    if text.count('%' + c) != 1:
                        self.w._displayWarning(self._text['Accounts'],
                                               self._text['BadPrompt'])
                        field.setFocus()
                        return

        storage.savePrompt(id_conn, username, normal, fight)
        conn_name = self.w.list_conn_account.currentText()
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)
        self.w.box_prompt.setVisible(False)


class FormAliases(FormOption):
    """
    Manage the aliases part of gui option.
    """

    def _getComboboxConnection(self):
        return self.w.list_conn_alias

    def _setupSignal(self):
        self.w.connect(self.w.save_alias, _CLICKED, self._saveAlias)
        self.w.connect(self.w.delete_alias, _CLICKED, self._deleteAlias)
        self.w.connect(self.w.list_conn_alias,
                      SIGNAL("currentIndexChanged(QString)"),
                      self._loadAliases)
        self.w.connect(self.w.list_alias,
                      SIGNAL("currentIndexChanged(int)"),
                      self._loadAlias)

    def disableSignal(self, disable):
        self.w.list_alias.blockSignals(disable)
        self.w.list_conn_alias.blockSignals(disable)

    def loadForm(self):
        self.w.list_conn_alias.clear()
        self.w.list_conn_alias.addItems([c[1] for c in storage.connections()])

        if self.w.list_conn_alias.count():
            conn_name = self._updateConnection()
            self._loadAliases(conn_name)

        for o in (self.w.list_alias, self.w.label_alias, self.w.body_alias):
            o.setEnabled(bool(self.w.list_conn_alias.count()))

    def _loadAliases(self, conn):
        self.disableSignal(True)
        self.w.list_alias.clear()
        self.w.list_alias.addItem(self._text['NewAlias'])
        self.aliases = storage.aliases(unicode(conn))
        self.w.list_alias.addItems([l for l, b in self.aliases])
        self.disableSignal(False)
        self._loadAlias(0)

    def _loadAlias(self, idx):
        if not idx:
            l, b = '', ''
        else:
            l, b = self.aliases[idx - 1]

        self.w.label_alias.setText(l)
        self.w.body_alias.setText(b)

    def _checkAliasFields(self):
        """
        Check validity of alias fields.
        """

        msg = []

        alias_fields = {self._text['Label']: self.w.label_alias,
                        self._text['Body']: self.w.body_alias}

        for text, field in alias_fields.iteritems():
            if not field.text():
                msg.append(unicode(text))

        if msg:
            self.w._displayWarning(self._text['Alias'],
                "%s:\n%s" % (self._text['ReqFields'], '\n'.join(msg)))
            return False


        if [el[0] for el in self.aliases if
            el[0] == self.w.label_alias.text() and
            not self.w.list_alias.currentIndex()]:
            self.w._displayWarning(self._text['Alias'],
                                   self._text['UniqueLabel'])
            return False

        return True

    def _saveAlias(self):
        if not self._checkAliasFields():
            return

        alias = (unicode(self.w.label_alias.text()),
                 unicode(self.w.body_alias.text()))

        list_idx = self.w.list_alias.currentIndex()
        if not list_idx:
            self.aliases.append(alias)
            self.w.list_alias.addItem(alias[0])
        else:
            self.aliases[list_idx - 1] = alias
            self.w.list_alias.setItemText(list_idx, alias[0])

        conn_name = self.w.list_conn_alias.currentText()
        storage.saveAliases(unicode(conn_name), self.aliases)
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)
        self.w.list_alias.setCurrentIndex(0)
        self._loadAlias(0)

    def _deleteAlias(self):

        list_idx = self.w.list_alias.currentIndex()
        if list_idx <= 0:
            return

        del self.aliases[list_idx - 1]
        self.w.list_alias.removeItem(list_idx)
        conn_name = self.w.list_conn_alias.currentText()
        storage.saveAliases(unicode(conn_name), self.aliases)
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)


class FormTriggers(FormOption):
    """
    Manage the triggers part of gui option.
    """

    def _getComboboxConnection(self):
        return self.w.list_conn_trigger

    def _setupSignal(self):
        self.w.connect(self.w.save_trigger, _CLICKED, self._saveTrigger)
        self.w.connect(self.w.delete_trigger, _CLICKED, self._deleteTrigger)
        self.w.connect(self.w.list_conn_trigger,
                      SIGNAL("currentIndexChanged(QString)"), self._loadTriggers)
        self.w.connect(self.w.list_trigger,
                      SIGNAL("currentIndexChanged(int)"), self._loadTrigger)
        self.w.connect(self.w.text_color_trigger_button, _CLICKED,
                       self._getTextColor)
        self.w.connect(self.w.bg_color_trigger_button, _CLICKED,
                       self._getBgColor)

    def _getTextColor(self):
        c = QColorDialog.getColor()
        self._text_color = unicode(c.name()) if c.isValid() else ''
        _setLabelColor(self.w.text_color_trigger, self._text_color)

    def _getBgColor(self):
        c = QColorDialog.getColor()
        self._bg_color = unicode(c.name()) if c.isValid() else ''
        _setLabelColor(self.w.bg_color_trigger, self._bg_color)

    def disableSignal(self, disable):
        self.w.list_trigger.blockSignals(disable)
        self.w.list_conn_trigger.blockSignals(disable)

    def loadForm(self):
        self.w.list_conn_trigger.clear()
        self.w.list_conn_trigger.addItems([c[1] for c in storage.connections()])

        if self.w.list_conn_trigger.count():
            conn_name = self._updateConnection()
            self._loadTriggers(conn_name)

        for o in (self.w.list_trigger, self.w.pattern_trigger,
                  self.w.command_trigger, self.w.case_trigger):
            o.setEnabled(bool(self.w.list_conn_trigger.count()))

        self._text_color, self._bg_color = '', ''

    def _loadTriggers(self, conn):
        self.disableSignal(True)
        self.w.list_trigger.clear()
        self.w.list_trigger.addItem(self._text['NewTrigger'])
        self.triggers = storage.triggers(unicode(conn))
        self.w.list_trigger.addItems([el[0] for el in self.triggers])
        self.disableSignal(False)
        self._loadTrigger(0)

    def _loadTrigger(self, idx):
        if not idx:
            patt, case, comm, bg, fg = '', 0, '', '', ''
        else:
            patt, case, comm, bg, fg = self.triggers[idx - 1]

        self.w.pattern_trigger.setText(patt)
        self.w.command_trigger.setText(comm)
        self.w.case_trigger.setCheckState((Qt.Unchecked, Qt.Checked)[case])

        self._text_color = fg
        self._bg_color = bg
        _setLabelColor(self.w.text_color_trigger, self._text_color)
        _setLabelColor(self.w.bg_color_trigger, self._bg_color)

    def _checkTriggerFields(self):
        """
        Check validity of trigger fields.
        """

        msg = []

        trigger_fields = {self._text['Pattern']: self.w.pattern_trigger}

        if not self.w.pattern_trigger.text():
            self.w._displayWarning(self._text['Trigger'], 
                                   self._text['ReqPattern'])
            return False

        if not self._text_color and not self._bg_color and \
           not self.w.command_trigger.text():
            self.w._displayWarning(self._text['Trigger'],
                                   self._text['ReqFields'])
            return False

        if [el[0] for el in self.triggers if
            el[0].upper() == unicode(self.w.pattern_trigger.text()).upper() and
            not self.w.list_trigger.currentIndex()]:
            self.w._displayWarning(self._text['Trigger'],
                                   self._text['UniquePattern'])
            return False

        return True

    def _saveTrigger(self):
        if not self._checkTriggerFields():
            return

        trigger = (unicode(self.w.pattern_trigger.text()),
                   int(self.w.case_trigger.checkState() == Qt.Checked),
                   unicode(self.w.command_trigger.text()),
                   self._bg_color,
                   self._text_color)

        list_idx = self.w.list_trigger.currentIndex()
        if not list_idx:
            self.triggers.append(trigger)
            self.w.list_trigger.addItem(trigger[0])
        else:
            self.triggers[list_idx - 1] = trigger
            self.w.list_trigger.setItemText(list_idx, trigger[0])

        conn_name = self.w.list_conn_trigger.currentText()
        storage.saveTriggers(unicode(conn_name), self.triggers)
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)
        self.w.list_trigger.setCurrentIndex(0)
        self._loadTrigger(0)

    def _deleteTrigger(self):
        list_idx = self.w.list_trigger.currentIndex()
        if list_idx <= 0:
            return

        del self.triggers[list_idx - 1]
        self.w.list_trigger.removeItem(list_idx)
        conn_name = self.w.list_conn_trigger.currentText()
        storage.saveTriggers(unicode(conn_name), self.triggers)
        self.w.emit(SIGNAL('reloadConnData(QString)'), conn_name)


class GuiOption(QDialog, Ui_option):
    """
    The Gui dialog for setup option.
    """

    def __init__(self, parent, conn_name):
        QDialog.__init__(self, parent)
        self._translateText()
        self.setupUi(self)
        self.setFixedWidth(480)

        # the transition widget is added at the end of the page_container stack
        # to keep the real pages indexes in sync with the correspondent items in
        # the listwidget.
        self._transition_widget = TransitionWidget(self)
        self.page_container.addWidget(self._transition_widget)
        self._setupSignal()

        self._lazy_conn = conn_name
        """the connection to load as the current conn in a Form* instance."""

        self.conn = FormConnection(self)
        """the `FormConnection` instance, used to manage form of connections."""

        self.macro = FormMacro(self)
        """the `FormMacro` instance, used to manage form of macros."""

        self.keypad = FormKeypad(self) if keypad_codes else FakeFormKeypad(self)

        self.preferences = FormPreferences(self)
        """the `FormPreferences` instance, used to manage form of preferences."""

        self.accounts = FormAccounts(self)
        """the FormAccounts instance, used to manage form of accounts."""

        self.alias = FormAliases(self)
        """the FormAliases instance, used to manage form of aliases."""

        self.trigger = FormTriggers(self)
        """the FormTriggers instance, used to manage form of triggers."""

    def _translateText(self):
        self._text = {}
        execfile(join(config['devclient']['path'], 'gui_option.msg'),
                 self._text)

    def _displayWarning(self, title, message):
        QMessageBox.warning(self, title, message)

    def _displayQuestion(self, title, message):
        b = QMessageBox.question(self, title, message,
                                 QMessageBox.Yes, QMessageBox.No)
        return b == QMessageBox.Yes

    def _setupSignal(self):
        self.connect(self.list_option,
                     SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
                     self._changeForm)
        self.connect(self, SIGNAL("currentConnChanged(QString)"),
                     self._lazyLoad)
        self.connect(self._transition_widget, SIGNAL("finished()"),
                     self._endTransition)

    def _lazyLoad(self, conn):
        self._lazy_conn = unicode(conn)

    def keyPressEvent(self, keyEvent):
        curr_page = self.page_container.currentWidget().objectName()
        if curr_page == "macro_page" and self.macro:
            self.macro.keyPressEvent(keyEvent)

    def _changeForm(self, current, previous):
        prev_page = self.page_container.currentWidget()
        next_page = self.page_container.widget(self.list_option.currentRow())

        curr_page = str(next_page.objectName())

        objs = {'alias_page': self.alias,
                'macro_page': self.macro,
                'keypad_page': self.keypad,
                'account_page': self.accounts,
                'trigger_page': self.trigger}

        form = objs.get(curr_page)
        if form:
            form.disableSignal(True)
            form.loadForm()
            form.disableSignal(False)

        # The transition effect works with the image of the previous page and
        # the image of the next page. To do the image of the next_page correct
        # we have to force the application of the layout before taking the image.
        next_page.resize(prev_page.size())
        next_page.layout().activate()

        self._startTransition(QPixmap.grabWidget(prev_page),
                              QPixmap.grabWidget(next_page))

    def _startTransition(self, prev_pixmap, next_pixmap):
        # We have to manage the situation when the user change the current
        # page before the ending of the transition effect.
        if self.page_container.currentWidget() == self._transition_widget:
            self._transition_widget.stop()

        # We set the transition widget as the current page of the stacked widget
        # in order to do the transition effect. At the end of the effect, we
        # set the next page as the current page.
        self.page_container.setCurrentWidget(self._transition_widget)
        self._transition_widget.start(prev_pixmap, next_pixmap)

    def _endTransition(self):
        self.page_container.setCurrentIndex(self.list_option.currentRow())

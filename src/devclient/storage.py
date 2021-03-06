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

import logging
from glob import glob
from os import unlink, chmod
from os.path import join, basename
from base64 import b64decode, b64encode

from validate import Validator
from configobj import ConfigObj

import exception

logger = logging.getLogger('storage')

if not logger.handlers:
    logger.addHandler(logging.StreamHandler())

_STORAGE_EXT = 'save'

connection_spec = {'id': 'integer',
                   'port': 'integer',
                   'macros': { '__many__': {'shift': 'integer(0, 1)',
                                            'alt': 'integer(0, 1)',
                                            'ctrl': 'integer(0, 1)',
                                            'keycode': 'integer'}},
                   'default_account': "string(default='')",
                   'triggers': { '__many__': {'ignore_case': 'integer(0, 1)',
                                              'command': "string(default='')",
                                              'bg_color': "string(default='')",
                                              'fg_color': "string(default='')"}},
                   'keypad': {'7': "string(default='')",
                              '8': "string(default='')",
                              '9': "string(default='')",
                              '4': "string(default='')",
                              '5': "string(default='')",
                              '6': "string(default='')",
                              '1': "string(default='')",
                              '2': "string(default='')",
                              '3': "string(default='')",
                              '0': "string(default='')",
                              '.': "string(default='')"
                              },
                  }

general_spec = {'echo_color': "string(max=7, default='')",
                'keep_text': 'integer(0, 1, default=0)',
                'save_log': 'integer(0, 1, default=0)',
                'save_account': 'integer(0, 1, default=0)',
                'default_connection': 'integer(default=0)',
                'bg_color': 'string(min=7, max=7, default=#000000)',
                'fg_color': 'string(min=7, max=7, default=#AAAAAA)',
                'cmd_separator' : 'string(max=1, default=";")'
               }

shortcuts_spec = {'history_prev': 'string(default="Up")',
                  'history_next': 'string(default="Down")',
                  'quit': 'string(default="ALT+Q")',
                  'connect': 'string(default="ALT+C")',
                  'option': 'string(default="ALT+O")',
                 }

_config = {'connections': {}}
"""The dict that contains the ConfigObj objs for connections and general pref"""

_storage_path = None

def init(storage_path):
    global _storage_path

    def _readStorageFile(f, spec):
        c = ConfigObj(f, configspec=spec)
        d = c.validate(Validator(), preserve_errors=True)
        if d != True:
            logger.warning('format error in storage file: %s' % f)
            for k, v in d.iteritems():
                if v != True:
                    logger.warning("%s: %s" % (k, v))
            return None

        return c

    if _config:
        _config.clear()
        _config['connections'] = {}

    _storage_path = storage_path 
    files = glob(join(_storage_path, '*.' + _STORAGE_EXT))
    for f in files:
        if basename(f) == 'passwords.' + _STORAGE_EXT:
            _config['passwords'] = ConfigObj(f, options={'indent_type': '  '})

        elif basename(f) != 'general.' + _STORAGE_EXT:
            c = _readStorageFile(f, connection_spec)
            if c:
                if 'name' in c:
                    _config['connections'][c['name']] = c
                else:
                    logger.warning(" format error in storage file %s" % f)

    general = join(_storage_path, 'general.' + _STORAGE_EXT)
    c = _readStorageFile(general, general_spec)
    if not c:
        # format error: restore defaults
        c = ConfigObj(options={'indent_type': '  '}, configspec=general_spec)
        c.validate(Validator())
        c.filename = general

    _config['general'] = c

    shortcuts = join(_storage_path, 'shortcuts.' + _STORAGE_EXT)
    c = _readStorageFile(shortcuts, shortcuts_spec)
    if not c:
        # format error: restore defaults
        c = ConfigObj(options={'indent_type': '  '}, configspec=shortcuts_spec)
        c.validate(Validator())
        c.filename = shortcuts

    _config['shortcuts'] = c

def shortcut(action):
    c = _config['shortcuts']
    return c[action] if action in c else ''

def preferences():
    """
    Return the list of preferences.

    :return: a tuple (echo_color, keep_text, save_log, cmd_separator)
    """

    c = _config['general']
    return (c['echo_color'], c['keep_text'], c['save_log'], c['cmd_separator'])

def savePreferences(pref):
    c = _config['general']
    c['echo_color'], c['keep_text'], c['save_log'], c['cmd_separator'] = pref
    c.write()

def _saveMany(conn_name, label, fields_name, fields):
    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    c[label] = {}
    i = 1
    for f in fields:
        d = {}
        for j in xrange(len(fields_name)):
            d[fields_name[j]] = f[j]
        c[label][str(i)] = d
        i += 1

    c.write()

def triggers(conn_name):
    """
    Load the list of trigger for a connection.

    :Parameters:
      conn_name : str
        the name of connection.

    :return: a list of tuples (pattern, ignore_case, command, bg_color, fg_color)
    """

    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    triggers = []
    if 'triggers' in c:
        for t in c['triggers'].itervalues():
            triggers.append((t['pattern'], t['ignore_case'], t['command'],
                             t['bg_color'], t['fg_color']))

    return triggers

def saveTriggers(conn_name, triggers):
    names = ('pattern', 'ignore_case','command', 'bg_color', 'fg_color')
    _saveMany(conn_name, 'triggers', names, triggers)

def aliases(conn_name):
    """
    Load the list of alias for a connection.

    :Parameters:
      conn_name : str
        the name of connection.

    :return: a list of tuples (label, body)
    """

    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    return c['aliases'].items() if 'aliases' in c else []

def saveAliases(conn_name, aliases):
    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    c['aliases'] = {}
    for alias in aliases:
        c['aliases'][alias[0]] = alias[1]
    c.write()

def keypad(conn_name):
    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    return c['keypad']

def saveKeypad(conn_name, keypad):
    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    c['keypad'] = keypad
    c.write()

def macros(conn_name):
    """
    Load the list of macro for a connection.

    :Parameters:
      conn_name : str
        the name of connection.

    :return: a list of tuples (command, shift, alt, ctrl, keycode)
    """

    if conn_name not in _config['connections']:
        raise exception.ConnectionNotFound

    c = _config['connections'][conn_name]
    macros = []
    if 'macros' in c:
        for m in c['macros'].itervalues():
            macros.append((m['command'], m['shift'], m['alt'],
                           m['ctrl'], m['keycode']))

    return macros

def saveMacros(conn_name, macros):
    names = ('command', 'shift', 'alt', 'ctrl', 'keycode')
    _saveMany(conn_name, 'macros', names, macros)

def connections():
    """
    Load the list of connections.

    :return: a list of tuples (id, name, host, port)
    """

    data = []
    for v in _config['connections'].itervalues():
        data.append((v['id'], v['name'], v['host'], v['port']))

    data.sort()
    return data

def addConnection(conn):
    """
    Add a new connection to the list of connections.

    :Parameters:
      conn : list
        the params of connection to add. The id param should be return
        valued.
    """

    m = 0
    for v in _config['connections'].itervalues():
        m = max(v['id'], m)

    c = ConfigObj(options={'indent_type': '  '}, configspec=connection_spec)
    c.validate(Validator())
    c['id'] = conn[0] = m + 1
    c['name'], c['host'], c['port'] = conn[1:]
    c.filename = join(_storage_path, conn[1] + '.' + _STORAGE_EXT)
    _config['connections'][conn[1]] = c
    c.write()

def deleteConnection(conn):
    unlink(_config['connections'][conn[1]].filename)
    del _config['connections'][conn[1]]

def updateConnection(conn):
    m = 0
    for k, c in _config['connections'].iteritems():
        if c['id'] == conn[0]:
            if c['name'] != conn[1] and 'passwords' in _config and \
               c['name'] in _config['passwords']:
                _config['passwords'][conn[1]] = _config['passwords'][c['name']]
                del _config['passwords'][c['name']]
                _config['passwords'].write()
            unlink(c.filename)
            del _config['connections'][k]
            c['name'], c['host'], c['port'] = conn[1:]
            c.filename = join(_storage_path, conn[1] + '.' + _STORAGE_EXT)
            _config['connections'][conn[1]] = c
            c.write()
            return
    else:
        raise exception.ConnectionNotFound

def connectionHasChild(conn_name):
    c = _config['connections'][conn_name]
    return c.get('aliases') or c.get('macros') or c.get('accounts')

def connection(conn_name):
    for k, c in _config['connections'].iteritems():
        if k == conn_name:
            return (c['id'], c['name'], c['host'], c['port'])
    else:
        raise exception.ConnectionNotFound

def option(name, id_conn=0):
    """
    Return the value of an option.

    :Parameters:
      name : str
        the name of the option.

      id_conn : int
        the id of connection.
    """

    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn:
                return c[name]
        else:
            raise exception.ConnectionNotFound
    else:
        return _config['general'][name]

def setOption(name, value, id_conn=0):
    if id_conn:
        for v in _config['connections'].itervalues():
            if v['id'] == id_conn:
                c = v
                break
        else:
            raise exception.ConnectionNotFound
    else:
        c = _config['general']

    c[name] = value
    c.write()

def accounts(id_conn):
    """
    Return the list of (username of) account for a connection.

    :Parameters:
      id_conn : int
        the id of connection.
    """

    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn:
                return c['accounts'].keys() if 'accounts' in c else []

    raise exception.ConnectionNotFound

def accountDetail(id_conn, username):
    """
    Return the list of command defined for an account.

    :Parameters:
      id_conn : int
        the id of connection.

      username : str
        the username of account.
    """

    def _getAccountPwd(conn, user):
        c =  _config
        if 'passwords' in c and conn in c['passwords'] and \
           user in c['passwords'][conn]:
            return b64decode(c['passwords'][conn][user])
        return None

    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn and 'accounts' in c:
                accounts = [(l, cmd) for l, cmd in
                            c['accounts'][username].iteritems()
                            if l.startswith('cmd-')]
                accounts.sort()
                data = [el[1] for el in accounts]
                pwd = _getAccountPwd(c['name'], username)
                if pwd:
                    data.append(pwd)
                return data

    raise exception.ConnectionNotFound

def deleteAccount(id_conn, username):
    """
    Erase an account.

    :Parameters:
      id_conn : int
        the id of connection.

      username : str
        the username of account.
    """

    def _delAccountPwd(conn, user):
        c =  _config
        if 'passwords' in c and conn in c['passwords'] and \
           user in c['passwords'][conn]:
            del c['passwords'][conn][user]
            c['passwords'].write()

    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn and 'accounts' in c:
                _delAccountPwd(c['name'], username)
                del c['accounts'][username]
                if not c['accounts']:
                    del c['accounts']
                c.write()
                return

    raise exception.ConnectionNotFound

def saveAccount(commands, id_conn, username):

    def _saveAccountPwd(conn, user, pwd):
        c =  _config
        if 'passwords' not in c:
            c['passwords'] = ConfigObj(options={'indent_type': '  '})
            c['passwords'].filename = join(_storage_path, 
                                           'passwords.' + _STORAGE_EXT)

        if conn not in c['passwords']:
            c['passwords'][conn] = {}

        c['passwords'][conn][user] = b64encode(pwd)
        c['passwords'].write()
        chmod(c['passwords'].filename, 0600)

    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn:
                if 'accounts' not in c:
                    c['accounts'] = {}
                if username not in c['accounts']:
                    c['accounts'][username] = {}
                else:
                    dead_list = [kk for kk in c['accounts'][username].iterkeys()
                                 if kk.startswith('cmd-')]

                    for d in dead_list:
                        del c['accounts'][username][d]

                _saveAccountPwd(c['name'], username, commands[-1])
                commands = commands[:-1]
                for i, cmd in enumerate(commands):
                    c['accounts'][username]['cmd-%d' % (i + 1)] = cmd
                c.write()
                return

    raise exception.ConnectionNotFound

def prompt(id_conn, username):
    if not username:
        return ('', '')

    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn:
                a = c['accounts'][username]
                n = a['normal_prompt'] if 'normal_prompt' in a else ''
                f = a['fight_prompt'] if 'fight_prompt' in a else ''
                return (n, f)

    raise exception.ConnectionNotFound

def savePrompt(id_conn, username, normal, fight):
    if id_conn:
        for c in _config['connections'].itervalues():
            if c['id'] == id_conn:
                c['accounts'][username]['normal_prompt'] = normal
                c['accounts'][username]['fight_prompt'] = fight
                c.write()
                return

    raise exception.ConnectionNotFound

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

"""
The module to manage auto updating of client.
"""

__version__ = "$Revision$"[11:-2]
__docformat__ = 'restructuredtext'

import sys, time
import tarfile
import subprocess
from filecmp import cmp
from optparse import OptionParser
from socket import setdefaulttimeout
from ConfigParser import SafeConfigParser
from shutil import copyfile, rmtree, copymode
from urllib2 import urlopen, HTTPError, URLError
from os import chdir, walk, getcwd, makedirs, rename, sep, unlink
from os.path import basename, splitext, split, abspath
from os.path import exists, join, normpath, dirname

_SELF_MODULE = basename(sys.argv[0])
"""name of the module itself"""

_SELF_DIR = abspath(dirname(sys.argv[0]))
"""directory of the module itself"""

_LOCAL_VERSION_FILE = abspath(join(_SELF_DIR, 'local.version'))
"""The file where the updater stores the local version"""

_ROOT_DIR = abspath(join(_SELF_DIR, '..'))
"""the root directory of client"""

_TMP_DIR = abspath(join(_SELF_DIR, 'temp'))
"""temp directory where store data for the process of updating"""

_CONFIG_FILE = join(_SELF_DIR, 'updater.cfg')
"""the configuration file"""


class UpdaterError(Exception):
    """
    Base class for the exceptions of updater.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def checkVersion(online_version, local_version):
    """
    Check the existance of a new version to download.

    :Parameters:
      online_version : str
        the online version available
      local_version : str
        the local version
    """

    print 'online version:', online_version, 'local version:', local_version
    online = map(int, online_version.split('.'))
    local = map(int, local_version.split('.'))
    return online > local

def getOnlineVersion(url):
    """
    Return the online version given an url, or the empty string if errors
    occurred.

    :Parameters:
      url : str
        the url of the file that contains the version.
    """

    setdefaulttimeout(2)

    try:
        u = urlopen(url)
    except HTTPError:
        raise UpdaterError('Unable to download file: %s' % url)
    except URLError:
        raise UpdaterError('Url malformed: %s' % url)
    except IOError:
        raise UpdaterError('Timeout on download file: %s' % url)

    return u.read().strip()

def downloadFile(url, timeout=2):
    """
    Download a file from an url and save in the filesystem.

    :Parameters:
      url : str
        the url of file to download
      timeout : int
        timeout to wait before raising error
    """

    setdefaulttimeout(timeout)
    try:
        u = urlopen(url)
    except HTTPError:
        raise UpdaterError('Unable to download file: %s' % url)
    except URLError:
        raise UpdaterError('Url malformed: %s' % url)
    except IOError:
        raise UpdaterError('Timeout on download file: %s' % url)

    length = int(u.info()['content-length'])
    if length > 524288: # 512 KB

        def format_time(seconds):
            return time.strftime('%H:%M:%S', time.gmtime(seconds))

        print 'download updates of:', int(u.info()['content-length']) / 1024, \
            'Kb '

        bar_length = 20
        chunk = length / 50
        data = ''
        start_time = time.time()
        for i in xrange(50):
            completed = int(i / (50.0 / bar_length))
            missing = bar_length - completed
            elapsed = time.time() - start_time
            if completed:
                eta = format_time(elapsed * bar_length / completed - elapsed)
            else:
                eta = '--:--:--'

            sys.stdout.write("\r[%s%s] %2d%% ETA: %s Time: %s" %
                ('#' * completed, '.' * missing, i * 2, eta, format_time(elapsed)))
            sys.stdout.flush()
            data += u.read(chunk)

        data += u.read()
        sys.stdout.write("\r[%s] %2d%% ETA: %s Time: %s\n" %
            ('#' * bar_length, 100, eta, format_time(time.time() - start_time)))
        sys.stdout.flush()
    else:
        data = u.read()

    filename = basename(url)
    fd = open(filename, 'wb+')
    fd.write(data)
    fd.close()

def uncompressFile(filename):
    """
    Extracting the file's data

    :Parameters:
      filename : str
        the name of the file
    """

    try:
        tar = tarfile.open(filename)
        name = normpath(tar.getnames()[0])
        sep_pos = name.find(sep)
        base_dir = name[:sep_pos] if sep_pos != -1 else name
        tar.extractall()
        tar.close()
    except tarfile.ReadError:
        raise UpdaterError('Archive malformed')
    return base_dir

def replaceOldVersion(root_dir, base_dir, ignore_list):
    """
    Replace the old files of installed client with the new files.

    :Parameters:
        root_dir : str
          the root directory of the tree
        base_dir : str
          the base directory of the new version
        ignore_list : list
          the list of files to be skipped
    """

    chdir(base_dir)
    for root, dirs, files in walk('.'):
        for f in files:
            source = normpath(join(root, f))
            if source in ignore_list:
                d, f = split(source)
                name, ext = splitext(f)
                dest = join(root_dir, d, name + '_ignore' + ext)
                if exists(dest) and cmp(source, dest):
                    continue
                print 'skip file: %s, save into %s' % (source, dest)
            else:
                dest = join(root_dir, source)
                if exists(dest) and cmp(source, dest):
                    continue

                # FIX: this check should be done from the root dir of client
                if basename(source) == _SELF_MODULE:
                    d, f = split(dest)
                    name, ext = splitext(f)
                    rename(dest, join(d, name + '_old' + ext))
                    print 'replace file: %s (old version backupped)' % source
                else:
                    print '%s file:' % ('add', 'replace')[exists(dest)], source

            if not exists(dirname(dest)):
                print 'create directory:', dirname(dest)
                makedirs(dirname(dest))
            copyfile(source, dest)
            copymode(source, dest)

        # create all the directories in the archive
        for d in dirs:
            if not exists(join(root_dir, root, d)):
                makedirs(join(root_dir, root, d))

def update(archive_name, root_dir, ignore_list):
    """
    Update a source tree, starting from an archive and the root dir of the
    tree.

    :Parameters:
        archive_name : str
          the new tree archive
        root_dir : str
          the root directory of the tree
        ignore_list : list
          the list of files to be skipped
        timeout : int
          the timeout (in second) of the newtwork operation. None means no
          timeout.
    """

    retvalue = False
    if not exists(_TMP_DIR):
        makedirs(_TMP_DIR)

    try:
        chdir(_TMP_DIR)
        base_dir = uncompressFile(archive_name)
        replaceOldVersion(root_dir, base_dir, ignore_list)
    except UpdaterError, e:
        print 'ERROR:', e
    else:
        retvalue = True
    finally:
        chdir(root_dir)  # change directory is required to remove the temp dir
        rmtree(_TMP_DIR)
    return retvalue

def getLocalVersion():
    """
    Read and return the local version (as a dictionary).
    """

    cp = SafeConfigParser()
    cp.read(_LOCAL_VERSION_FILE)
    # if no local version is found, force the download of the new version
    versions = {'client' : '0.0.00', 'packages' : '0.0.00'}
    if cp.has_section('versions'):
        versions.update(dict(cp.items('versions')))
    return versions

def saveVersion(version):
    """
    Update the file that contains the local version. Return False if errors
    occurred.

    :Parameters:
        version : dict
          the dictionary containing the version to save into the file.
    """

    cp = SafeConfigParser()
    cp.read(_LOCAL_VERSION_FILE)

    if not cp.has_section('versions'):
        cp.add_section('versions')
    for key, value in version.iteritems():
        cp.set('versions', key, value)

    try:
        cp.write(open(_LOCAL_VERSION_FILE, 'w'))
    except IOError:
        return False

    return True

def updateFromNet(config):
    ignore_list = map(normpath, config['files']['ignore'].split(','))
    local_version = getLocalVersion()
    updated = False
    retcode = 0

    client_ver = getOnlineVersion(config['client']['version'])
    if not client_ver:
        print 'Unknown online version of client, download it'

    if not client_ver or checkVersion(client_ver, local_version['client']):
        downloadFile(config['client']['url'])
        client = abspath(basename(config['client']['url']))
        if not update(client, _ROOT_DIR, ignore_list):
            print 'Fatal error while updating', config['client']['url']
            retcode = 1
        else:
            updated = True
        unlink(client)

    if hasattr(sys, 'frozen') and sys.frozen:
        pack_ver = getOnlineVersion(config['packages']['version'])
        if not pack_ver:
            print 'Unknown online version of the packages, download them'

        if not pack_ver or checkVersion(pack_ver, local_version['packages']):
            downloadFile(config['packages']['url'], None)
            packages = abspath(basename(config['packages']['url']))
            if not update(packages, _ROOT_DIR, ignore_list):
                print 'Fatal error while updating', config['packages']['url']
                retcode = 1
            else:
                updated = True
            unlink(packages)

    if updated:
        if client_ver:
            local_version['client'] = client_ver
        if hasattr(sys, 'frozen') and sys.frozen and pack_ver:
            local_version['packages'] = pack_ver
        saveVersion(local_version)

    return (retcode, updated)

def updateFromLocal(config):

    updated = False
    retcode = 0
    ignore_list = map(normpath, config['files']['ignore'].split(','))
    client = abspath(basename(config['client']['url']))
    packages = abspath(basename(config['packages']['url']))

    if exists(client):
        if not update(client, _ROOT_DIR, ignore_list):
            print 'Fatal error while updating', client
            retcode = 1
        else:
            updated = True


    if hasattr(sys, 'frozen') and sys.frozen:
        if exists(packages):
            if not update(packages, _ROOT_DIR, ignore_list):
                print 'Fatal error while updating', packages
                retcode = 1
            else:
                updated = True

    return (retcode, updated)

def main():
    parser = OptionParser()
    parser.add_option('--source', default='net',
                      help='(local|net) the source used for the updates')

    o, args = parser.parse_args()

    cp = SafeConfigParser()
    cp.read(_CONFIG_FILE)
    config = {}
    for s in cp.sections():
        config[s] = dict(cp.items(s))

    if not int(config['main']['update']):
        print 'Update disabled!'
        return 0

    funcUpdate = updateFromLocal if o.source == 'local' else updateFromNet
    retcode, updated = funcUpdate(config)

    if not retcode and updated:
        print 'Update successfully complete!'
    sys.exit(retcode)


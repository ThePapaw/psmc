# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v3 Scrapers
# Addon id: script.module.fuzzybritchesv3scrapers
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import os
import traceback
from datetime import datetime
from kodi_six import xbmc

import six

from io import open

from fuzzybritchesscrapers.modules import control

LOGDEBUG = xbmc.LOGDEBUG
# LOGINFO = xbmc.LOGINFO
# LOGNOTICE = xbmc.LOGNOTICE if control.getKodiVersion() < 19 else xbmc.LOGINFO
# LOGWARNING = xbmc.LOGWARNING
# LOGERROR = xbmc.LOGERROR
# LOGFATAL = xbmc.LOGFATAL
# LOGNONE = xbmc.LOGNONE

name = control.addonInfo('name')
version = control.addonInfo('version')
DEBUGPREFIX = '[ Fuzzybritchesscrapers {0} | DEBUG ]'.format(version)
INFOPREFIX = '[ Fuzzybritchesscrapers | INFO ]'
LOGPATH = control.transPath('special://logpath/')
log_file = os.path.join(LOGPATH, 'fuzzybritches_v3.log')
debug_enabled = control.addon('plugin.video.fuzzybritches_v3').getSetting('addon.debug')


def log(msg, trace=0):

    if not debug_enabled == 'true':
        return

    try:
        if trace == 1:
            head = DEBUGPREFIX
            failure = six.ensure_str(traceback.format_exc(), errors='replace')
            _msg = ' %s:\n  %s' % (six.ensure_text(msg, errors='replace'), failure)
        else:
            head = INFOPREFIX
            _msg = '\n    %s' % six.ensure_text(msg, errors='replace')

        #if not debug_log == '0':
        if not os.path.exists(log_file):
            f = open(log_file, 'w')
            f.close()
        with open(log_file, 'a', encoding='utf-8') as f:
            line = '[%s %s] %s%s' % (datetime.now().date(), str(datetime.now().time())[:8], head, _msg)
            f.write(line.rstrip('\r\n')+'\n\n')
        #else:
            #xbmc.log('%s: %s' % (head, _msg), LOGDEBUG)
    except Exception as e:
        try:
            xbmc.log('FuzzybritchesScrapers Logging Failure: %s' % e, LOGDEBUG)
        except:
            pass


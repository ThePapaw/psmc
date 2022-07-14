# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches
# Addon id: script.module.fuzzybritches
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs,os,sys
import urllib
import re
import time
from resources.lib.modules import control
from datetime import datetime
from resources.lib.modules.backtothefuture import unicode, PY2

dp           = xbmcgui.DialogProgress()
dialog       = xbmcgui.Dialog()
addonInfo    = xbmcaddon.Addon().getAddonInfo

AddonTitle="PSMC Maintenance"
AddonID ='plugin.program.psmcmaintenance'

def open_Settings():
    open_Settings = xbmcaddon.Addon(id=AddonID).openSettings()

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText())
    return default

def logView():
    modes = ['View Log', 'Upload Log to Pastebin']
    logPaths = []
    logNames = []
    select = control.selectDialog(modes)

    # Code to map the old translatePath
    try:
        translatePath = xbmcvfs.translatePath
    except AttributeError:
        translatePath = xbmc.translatePath

    try:
        if select == -1: raise Exception()
        logfile_path = translatePath('special://logpath')
        logfile_names = ('kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'freetelly.log', 'ftmc.log', 'firemc.log', 'nodi.log')
        for logfile_name in logfile_names:
            log_file_path = os.path.join(logfile_path, logfile_name)
            if os.path.isfile(log_file_path):
                logNames.append(logfile_name)
                logPaths.append(log_file_path)

        selectLog = control.selectDialog(logNames)
        selectedLog = logPaths[selectLog]
        if selectLog == -1: raise Exception()
        if select == 0:
            from resources.lib.modules import TextViewer
            TextViewer.text_view(selectedLog)
        elif select == 1:
            xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
            f = open(selectedLog, 'rb')
            text = f.read()
            text = text.decode('UTF-8')
            f.close()
            from resources.lib.modules import pastebin
            upload_Link = pastebin.api().paste(unicode(text))
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
            print ("LOGVIEW UPLOADED LINK", upload_Link)
            if upload_Link != None:
                if not "Error" in upload_Link:
                    label = "Log Link: [COLOR skyblue][B]" + upload_Link + "[/B][/COLOR]"
                    dialog.ok(AddonTitle, "Log Uploaded to Pastebin" + '\n' + label)
                else: dialog.ok(AddonTitle, "Cannot Upload Log to Pastebin" + '\n' + "Reason " + upload_Link)
            else:dialog.ok(AddonTitle, "Cannot Upload Log to Pastebin")

    except:pass


##############################    END    #########################################
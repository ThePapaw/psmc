# -*- coding: UTF-8 -*-
### Saved
# CustomColor = control.setting('my_ColorChoice')
# if CustomColor == '': CustomColor = 'none'

import os,sys,urlparse
from datetime import date, datetime, timedelta
import xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs


integer = 1000
addon = xbmcaddon.Addon
Addon = xbmcaddon.Addon()
addonInfo = addon().getAddonInfo
transPath = xbmc.translatePath
execute = xbmc.executebuiltin

lang = addon().getLocalizedString
lang2 = xbmc.getLocalizedString

setting = addon().getSetting
setSetting = addon().setSetting

addItem = xbmcplugin.addDirectoryItem
directory = xbmcplugin.endOfDirectory

dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

item = xbmcgui.ListItem
content = xbmcplugin.setContent
property = xbmcplugin.setProperty
infoLabel = xbmc.getInfoLabel
condVisibility = xbmc.getCondVisibility
jsonrpc = xbmc.executeJSONRPC

sleep = xbmc.sleep

skin = xbmc.getSkinDir()
skinPath = transPath('special://skin/')
dataPath = transPath(addonInfo('profile')).decode('utf-8')
viewsFile = os.path.join(dataPath, 'views.db')

AddonID = addonInfo('id')
AddonTitle = addonInfo('name')
AddonVersion = addonInfo('version') # old label  VERSION
AddonIcon = addonInfo('icon')
AddonFanart = addonInfo('fanart')
AddonPath = addonInfo('path')
AddonProfile = transPath(addonInfo('profile'))

artPath = transPath(os.path.join(AddonPath, 'art')) # used here for theme defs
HOMEPATH = transPath('special://home/') # used in cogs (Favs stuff)
USERDATAPATH = os.path.join(HOMEPATH, 'userdata') # used in cogs (Favs stuff)
DATABASE = os.path.join(USERDATAPATH, 'Database') # in clean.py
THUMBSPATH = os.path.join(USERDATAPATH, 'Thumbnails') # in clean.py
ADDONDATA = os.path.join(USERDATAPATH, 'addon_data', AddonID) # used in cogs (Favs stuff)
USERDATA = transPath(os.path.join('special://home/userdata','')) # used in wiz.py (backup)
THUMBS = transPath(os.path.join('special://home/userdata/Thumbnails','')) # used in maintenance.py
WIZLOG = os.path.join(ADDONDATA, 'psmcmaintenance.log') # Used here only for loga


def getKodiVersion():
    return infoLabel("System.BuildVersion").split(".")[0]


def get_Kodi_Version():
    try: KODIV = float(infoLabel("System.BuildVersion")[:4])
    except: KODIV = 0
    return KODIV


def getCurrentViewId():
    win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    return str(win.getFocusId())


def getSettingEnabled(item):
    is_enabled = setting(item).strip()
    if (is_enabled == '' or is_enabled == 'false'): return False
    return True


def getSetting(id):
        return Addon.getSetting(id)


def setSetting(id, value):
        return Addon.setSetting(id, value)


def get_keyboard(default="", heading="", hidden=False):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return unicode(keyboard.getText(), "utf-8")
    return default


def version():
    num = ''
    try: version = addon('xbmc.addon').getAddonInfo('version')
    except: version = '999'
    for i in version:
        if i.isdigit(): num += i
        else: break
    return int(num)


def Notify(title, message, duration=3000, icon=AddonIcon):
    execute('XBMC.Notification(%s, %s, %s, %s)' % (title , message , duration, icon))


def log(log):
    xbmc.log("[%s]: %s" % (AddonTitle, log))
    if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)


def loga(msg, level=xbmc.LOGDEBUG):
    if setting('addon_debug') == 'true' and level == xbmc.LOGDEBUG:
        level = xbmc.LOGNOTICE
    try:
        if isinstance(msg, unicode):
            msg = '%s' % (msg.encode('utf-8'))
        xbmc.log('%s: %s' % (AddonTitle, msg), level)
    except Exception as e:
        try: xbmc.log('Logging Failure: %s' % (e), level)
        except: pass
    if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
    if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
    with open(WIZLOG, 'a') as f:
        line = "[%s %s] %s" % (datetime.now().date(), str(datetime.now().time())[:8], msg)
        f.write(line.rstrip('\r\n')+'\n')    


def infoDialog(message, heading=addonInfo('name'), icon='', time=None, sound=False):
    if time == None: time = 3000
    else: time = int(time)
    if icon == '': icon = AddonIcon
    elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
    elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
    elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
    dialog.notification(heading, message, icon, time, sound=sound)


def TextBox(header, message):
    execute("ActivateWindow(10147)")
    controller = xbmcgui.Window(10147)
    sleep(500)
    controller.getControl(1).setLabel(header)
    controller.getControl(5).setText(message)


def OkDialog(title, message):
    dialog.ok(title,message)


def YesNoDialog(title, message, yes=None, no=None):
    choice = dialog.yesno(title,message,yeslabel=yes,nolabel=no)
    return choice


def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def SelectDialog(title, options, key=True):
    mychoice = dialog.select(title,options)
    if key:
        return mychoice
    else:
        return options[mychoice]


def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)


def openSettings(query=None, id=addonInfo('id')):
    try:
        idle()
        execute('Addon.OpenSettings(%s)' % id)
        if query == None: raise Exception()
        c, f = query.split('.')
        if int(getKodiVersion()) >= 18:
            execute('SetFocus(%i)' % (int(c) - 100))
            execute('SetFocus(%i)' % (int(f) - 80))
        else:
            execute('SetFocus(%i)' % (int(c) + 100))
            execute('SetFocus(%i)' % (int(f) + 200))
    except:
        return


def refresh():
    return execute('Container.Refresh')


def closeOkDialog():
    return execute('Dialog.Close(okdialog, true)')


def busy():
    if int(getKodiVersion()) >= 18:
        return execute('ActivateWindow(busydialognocancel)')
    else:
        return execute('ActivateWindow(busydialog)')


def idle():
    if int(getKodiVersion()) >= 18:
        return execute('Dialog.Close(busydialognocancel)')
    else:
        return execute('Dialog.Close(busydialog)')


def getChangeLog():
    changelogfile = transPath(os.path.join(AddonPath, 'changelog.txt'))
    r = open(changelogfile)
    text = r.read()
    id = 10147
    execute('ActivateWindow(%d)' % id)
    sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            sleep(10)
            retry -= 1
            win.getControl(1).setLabel('--[ v%s ChangeLog ]--' %(AddonVersion))
            win.getControl(5).setText(text)
            return
        except:
            pass


def platform(): # used in ForceClose()
    if condVisibility('system.platform.android'): return 'android'
    elif condVisibility('system.platform.linux'): return 'linux'
    elif condVisibility('system.platform.windows'): return 'windows'
    elif condVisibility('system.platform.osx'): return 'osx'
    elif condVisibility('system.platform.atv2'): return 'atv2'
    elif condVisibility('system.platform.ios'): return 'ios'



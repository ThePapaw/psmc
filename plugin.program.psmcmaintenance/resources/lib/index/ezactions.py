# -*- coding: UTF-8 -*-

import os
from resources.lib.modules import control
from resources.lib.api import colorChoice


AddonID = control.AddonID
AddonTitle = control.AddonTitle
SelectDialog = control.SelectDialog
Execute = control.execute
Notify = control.Notify

CustomColor = control.setting('my_ColorChoice')
if CustomColor == '': CustomColor = 'none'


def actChangeLog():
    from resources.lib.api import TextViewer
    changelogfile = control.transPath(os.path.join('special://home/addons/' + AddonID, 'changelog.txt'))
    my_options = ['DialogWindow', 'TextViewer', '[ [B] Close [/B] ]']
    selectList = []
    for Item in my_options:
        selectList.append(colorChoice.colorString(Item, CustomColor))
    mychoice = SelectDialog(AddonTitle, selectList, key=False)
    mychoice = mychoice.replace('[COLOR %s]' % (CustomColor),'').replace('[/COLOR]','')
    if mychoice == 'DialogWindow': control.getChangeLog()
    elif mychoice == 'TextViewer': TextViewer.text_view(changelogfile)
    elif mychoice == '[ [B] Close [/B] ]': return


def actLogMenu():
    from resources.lib.modules import utilz
    my_options = ['[B]Log Viewer/Uploader[/B]', '[B]Clear CrashLogs[/B]', '[B]Clear DebugLogs[/B]', '[ [B]Close[/B] ]']
    selectList = []
    for Item in my_options:
        selectList.append(colorChoice.colorString(Item, CustomColor))
    mychoice = SelectDialog(AddonTitle, selectList, key=False)
    mychoice = mychoice.replace('[COLOR %s]' % (CustomColor),'').replace('[/COLOR]','')
    if mychoice == '[B]Log Viewer/Uploader[/B]': utilz.logView()
    elif mychoice == '[B]Clear CrashLogs[/B]': utilz.Delete_Crash_Logs()
    elif mychoice == '[B]Clear DebugLogs[/B]': utilz.Delete_DebugLogs()
    elif mychoice == '[ [B]Close[/B] ]' : return


def advancedSettingsMenu():
    from resources.lib.modules import advsetz
    my_options = ['Create AdvancedSettings', 'View AdvancedSettings', 'Clear AdvancedSettings', '[ [B] Close [/B] ]']
    selectList = []
    for Item in my_options:
        selectList.append(colorChoice.colorString(Item, CustomColor))
    mychoice = SelectDialog(AddonTitle, selectList, key=False)
    mychoice = mychoice.replace('[COLOR %s]' % (CustomColor),'').replace('[/COLOR]','')
    if mychoice == 'Create AdvancedSettings': advsetz.advancedSettings()
    elif mychoice == 'View AdvancedSettings': advsetz.viewAdvancedSettings()
    elif mychoice == 'Clear AdvancedSettings': advsetz.clearAdvancedSettings()
    elif mychoice == '[ [B] Close [/B] ]': return


def kodiMenu():
    my_options = ['FileManager', 'AddonBrowser', 'InterfaceSettings', 'SystemSettings', 'ShowSettings', 'SkinSettings', 'ShowSystemInfo', '[ [B]Close[/B] ]']
    selectList = []
    for Item in my_options:
        selectList.append(colorChoice.colorString(Item, CustomColor))
    mychoice = SelectDialog(AddonTitle, selectList, key=False)
    mychoice = mychoice.replace('[COLOR %s]' % (CustomColor),'').replace('[/COLOR]','')
    if mychoice == 'FileManager': Execute("ActivateWindow(10003)")
    elif mychoice == 'AddonBrowser': Execute("ActivateWindow(10040)")
    elif mychoice == 'InterfaceSettings': Execute("ActivateWindow(10032)")
    elif mychoice == 'SystemSettings': Execute("ActivateWindow(10016)")
    elif mychoice == 'ShowSettings': Execute("ActivateWindow(10004)")
    elif mychoice == 'SkinSettings': Execute("ActivateWindow(10035)")
    elif mychoice == 'ShowSystemInfo': Execute("ActivateWindow(10007)")
    elif mychoice == '[ [B]Close[/B] ]': return


def kodiDbMenu():
    my_options = ['CleanPlaylist', 'UpdateVideoDB', 'CleanVideoDB', 'UpdateMusicDB', 'CleanMusicDB', '[ [B]Close[/B] ]']
    selectList = []
    for Item in my_options:
        selectList.append(colorChoice.colorString(Item, CustomColor))
    mychoice = SelectDialog(AddonTitle, selectList, key=False)
    mychoice = mychoice.replace('[COLOR %s]' % (CustomColor),'').replace('[/COLOR]','')
    if mychoice == 'CleanPlaylist': Execute("Playlist.Clear")
    elif mychoice == 'UpdateVideoDB': Execute("UpdateLibrary(video)")
    elif mychoice == 'CleanVideoDB': Execute("CleanLibrary(video)")
    elif mychoice == 'UpdateMusicDB': Execute("UpdateLibrary(music)")
    elif mychoice == 'CleanMusicDB': Execute("CleanLibrary(music)")
    elif mychoice == '[ [B]Close[/B] ]' : return



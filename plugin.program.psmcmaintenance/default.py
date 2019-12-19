# -*- coding: UTF-8 -*-

import os,sys,urllib
from resources.lib.modules import control


AddonID = control.AddonID
AddonTitle = control.AddonTitle
MENU_FANART = control.AddonFanart
MENU_ICON = "DefaultAddonProgram.png"
getSetEnabled = control.getSettingEnabled
Notify = control.Notify
log = control.log


def setView(content, viewType):
    if content:
        control.content(int(sys.argv[1]), content)
    if control.getSetting('auto-view')=='true':
        views = control.getSetting('viewType2')
        if views == '50' and control.getKodiVersion >= 17 and control.skin == 'skin.estuary': views = '55'
        if views == '500' and control.getKodiVersion >= 17 and control.skin == 'skin.estuary': views = '50'
        return control.execute("Container.SetViewMode(%s)" % views)
    else:
        views = control.getCurrentViewId()
        return control.execute("Container.SetViewMode(%s)" % views)


def CreateDir(name, url, action, icon, fanart, description, isFolder=False):
    CustomColor = control.setting('my_ColorChoice')
    if CustomColor == '': CustomColor = 'none'
    if icon == None or icon == '': icon = MENU_ICON
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&action="+str(action)+"&name="+urllib.quote_plus(name)+"&icon="+urllib.quote_plus(icon)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
    ok=True
    name = '[COLOR %s][B]%s[/B][/COLOR]' % (CustomColor, name)
    liz=control.item(name, iconImage="DefaultAddonProgram.png", thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    ok=control.addItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
    return ok


def MAIN_MENU():
    setView('addons', 'views')
    if getSetEnabled('navi.maintenance') == True:
        CreateDir('Maintenance', 'url', 'maintenance', control.AddonIcon, MENU_FANART, 'Maintenance Menu.', isFolder=True )
    if getSetEnabled('navi.tools') == True:
        CreateDir('Tools', 'url', 'tools', control.AddonIcon, MENU_FANART, 'Tools Menu.', isFolder=True )
    if getSetEnabled('navi.utils') == True:
        CreateDir('Utilities', 'url', 'utilities', control.AddonIcon, MENU_FANART, 'Utilities Menu.', isFolder=True )
    if getSetEnabled('navi.logs') == True:
        CreateDir('Logs', 'url', 'log_tools', control.AddonIcon, MENU_FANART, 'Debug Logs Menu.')
    if getSetEnabled('navi.settings') == True:
        CreateDir('Settings', 'url', 'settings', control.AddonIcon, MENU_FANART, '%s Settings.' %AddonTitle)
    if getSetEnabled('navi.changelog') == True:
        CreateDir('Change Log', 'url', 'changeLog', control.AddonIcon, MENU_FANART, '%s Change Log.' %AddonTitle)


def MAINTENANCE():
    #setView('addons', 'views') # descriptions left as template while i think i about adding stats to these options.
    CreateDir('Clear All (Cache, Packages, Thumbnails)', 'url', 'clear_ALL', control.AddonIcon, MENU_FANART, 'description' )
    CreateDir('Clear Cache', 'url', 'deleteCache', control.AddonIcon, MENU_FANART, 'description' )
    CreateDir('Clear Packages', 'url', 'deletePackages', control.AddonIcon, MENU_FANART, 'description' )
    CreateDir('Clear Thumbnails', 'url', 'clearThumb', control.AddonIcon, MENU_FANART, 'description' )
    CreateDir('[I]Clear Resolvers Cache[/I]', 'url', 'reset_ResolversCache', control.AddonIcon, MENU_FANART, 'description' )
    CreateDir('[I]Clear Empty Folders[/I]', 'url', 'clearEmptyFolders', control.AddonIcon, MENU_FANART, 'description' )


def TOOLS():
    setView('addons', 'views')
    CreateDir('Backup/Restore', 'url', 'backup_restore', control.AddonIcon, MENU_FANART, 'Backup and Restore Menu.' )
    CreateDir('Builds/Wizards', 'url', 'builds', control.AddonIcon, MENU_FANART, 'Builds and Wizards Menu.', isFolder=True )
    CreateDir('AdvancedSettings.xml Tool', 'url', 'advancedSettings', control.AddonIcon, MENU_FANART, 'Advanced Settings Menu.')
    CreateDir('Kodi Shortcuts', 'url', 'kodishortz', control.AddonIcon, MENU_FANART, 'Useful Kodi Shortcuts to speed up Setup.' )
    CreateDir('Kodi Database ShortCuts', 'url', 'kodiDBshortz', control.AddonIcon, MENU_FANART, 'Kodi Shortcuts for DB Stuff.' )
    CreateDir('Network Info', 'url', 'netINFO', control.AddonIcon, MENU_FANART, 'View Device Net Info.', isFolder=True )



def UTILITIES():
    #setView('addons', 'views')
    CreateDir('Run Quick Speed Test', 'url', 'speedTest', control.AddonIcon, MENU_FANART, 'Run a quick Speed Test.' )
    CreateDir('Check Sources', 'url', 'checkSources', control.AddonIcon, MENU_FANART, 'Check for any Broken Sources.' )
    CreateDir('Check for Non-working Repos', 'url', 'checkRepos', control.AddonIcon, MENU_FANART, 'Check for any Broken Repos.' )
    CreateDir('Check for Add-on Updates', 'url', 'forceUpdate', control.AddonIcon, MENU_FANART, 'Check for any new Updates.' )
    CreateDir('Disable Auto Updates (Sets to Notify)', 'url', 'disableAutoUpdates', control.AddonIcon, MENU_FANART, 'Set AutoUpdates To Notify but not Auto Intsall.' )
    CreateDir('Enable Unknown Sources', 'url', 'enableUnknownSources', control.AddonIcon, MENU_FANART, 'Enable Unknown Sources.' )
    CreateDir('Enable ALL Addons', 'url', 'enableAddons', control.AddonIcon, MENU_FANART, 'Enable All Addons.' )


def NETINFO():
    setView('addons', 'views')
    from resources.lib.modules import toolz
    mac, inter_ip, ip, city, state, country, isp = toolz.net_info()
    CreateDir('Mac: [ %s ]' % (mac), '', '', control.AddonIcon, MENU_FANART, '' )
    CreateDir('Internal IP: [ %s ]' % (inter_ip), '', '', control.AddonIcon, MENU_FANART, '' )
    CreateDir('External IP: [ %s ]' % (ip), '', '', control.AddonIcon, MENU_FANART, '' )
    CreateDir('City: [ %s ]' % (city), '', '', control.AddonIcon, MENU_FANART, '' )
    CreateDir('State: [ %s ]' % (state), '', '', control.AddonIcon, MENU_FANART, '' )
    CreateDir('Country: [ %s ]' % (country), '', '', control.AddonIcon, MENU_FANART, '' )
    CreateDir('ISP: [ %s ]' % (isp), '', '', control.AddonIcon, MENU_FANART, '' )


def BUILDS():
    setView('addons', 'views')
    CreateDir('Kodi Version Check', 'url', 'getKodiVersion', control.AddonIcon, MENU_FANART, 'Check My Kodi Version.' )
    CreateDir('Current Profile Check', 'url', 'checkCurrentProfile', control.AddonIcon, MENU_FANART, 'Check My Current Profile.' )
    wizard1 = control.setting('enable_wiz1')
    if wizard1!= 'false':
        try:
            name = unicode(control.getSetting('name1'))
            url = unicode(control.getSetting('url1'))
            img = unicode(control.getSetting('img1'))
            fanart = unicode(control.getSetting('img1'))
            CreateDir('[Wizard] ' + name, url, 'install_build', img, fanart, 'My Custom Build.', isFolder=False )
        except: pass
    wizard2 = control.setting('enable_wiz2')
    if wizard2!= 'false':
        try:
            name = unicode(control.getSetting('name2'))
            url = unicode(control.getSetting('url2'))
            img = unicode(control.getSetting('img2'))
            fanart = unicode(control.getSetting('img2'))
            CreateDir('[Wizard] ' + name, url, 'install_build', img, fanart, 'My Custom Build.', isFolder=False )
        except: pass
    wizard3 = control.setting('enable_wiz3')
    if wizard3!= 'false':
        try:
            name = unicode(control.getSetting('name3'))
            url = unicode(control.getSetting('url3'))
            img = unicode(control.getSetting('img3'))
            fanart = unicode(control.getSetting('img3'))
            CreateDir('[Wizard] ' + name, url, 'install_build', img, fanart, 'My Custom Build.', isFolder=False )
        except: pass
    CreateDir('[I]Swap Skin[/I]', 'url', 'skinSWAP', control.AddonIcon, MENU_FANART, 'Swap to Default Skin.')
    CreateDir('[I]Force Close Kodi[/I]', 'url', 'Force_Close', control.AddonIcon, MENU_FANART, 'Force Close Kodi.' )
    CreateDir('[I]Reload Skin[/I]', 'url', 'reloadMySkin', control.AddonIcon, MENU_FANART, 'Reload Current Skin.' )
    CreateDir('[I]Reload Profile[/I]', 'url', 'reloadProfile', control.AddonIcon, MENU_FANART, 'Reload My User Profile.' )
    CreateDir('[I]Fresh Start[/I]', 'url', 'fresh_start', control.AddonIcon, MENU_FANART, 'Wipe Kodi like a Factory Reset.' )
    CreateDir('Wizard Settings', 'url', 'wizSettings', control.AddonIcon, MENU_FANART, 'Open up Wizard Settings.' )


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
        return param


params = get_params()
url = None
try: url = urllib.unquote_plus(params["url"])
except: pass
action = None
try: action = urllib.unquote_plus(params["action"])
except: pass
name = None
try: name = urllib.unquote_plus(params["name"])
except: pass
icon = None
try: icon = urllib.unquote_plus(params["icon"])
except: pass
fanart = None
try: fanart = urllib.unquote_plus(params["fanart"])
except: pass
description = None
try: description = urllib.unquote_plus(params["description"])
except: pass
mode = None
try: mode = urllib.unquote_plus(params["mode"])
except: pass


if action == None: MAIN_MENU()
elif action == 'maintenance': MAINTENANCE()
elif action == 'tools': TOOLS()
elif action == 'utilities': UTILITIES()
elif action == "netINFO": NETINFO()
elif action == 'builds': BUILDS()
elif action == 'wizSettings': control.openSettings(query='3.1')
elif action == 'settings': control.openSettings()


elif action == 'colorChoice':
    from resources.lib.api import colorChoice
    colorChoice.colorChoice()


elif action == 'viewTypes':
    from resources.lib.api import viewTypes
    viewTypes.getViewType()


elif action == 'changeLog':
    from resources.lib.index import ezactions
    ezactions.actChangeLog()


elif action == 'log_tools':
    from resources.lib.index import ezactions
    ezactions.actLogMenu()


elif action == 'clear_ALL':
    from resources.lib.modules import maintenance
    maintenance.clearCache()
    maintenance.purgePackages()
    maintenance.deleteThumbnails()


elif action == 'deleteCache':
    from resources.lib.modules import clean
    clean.Delete_Cache(url)


elif action == 'deletePackages':
    from resources.lib.modules import clean
    clean.Delete_Packages(url)


elif action == 'clearThumb':
    from resources.lib.modules import clean
    clean.Clear_Thumb()


elif action == 'reset_ResolversCache':
    from resources.lib.modules import toolz
    Notify(AddonTitle, 'Clearing Resolver Cache...')
    toolz.resetResolversCache()


elif action == 'clearEmptyFolders':
    from resources.lib.modules import wiz
    Notify(AddonTitle, 'Clearing Empty Folders...')
    wiz.REMOVE_EMPTY_FOLDERS()
    Notify(AddonTitle, 'Done Clearing Empty Folders.')


elif action == 'advancedSettings':
    from resources.lib.index import ezactions
    ezactions.advancedSettingsMenu()


elif action == 'checkSources':
    from resources.lib.modules import utilz
    utilz.Broken_Sources()


elif action == 'checkRepos':
    from resources.lib.modules import utilz
    utilz.Broken_Repos()


elif action == 'forceUpdate':
    from resources.lib.modules import toolz
    toolz.ForceUpdateCheck()


elif action == 'enableAddons':
    from resources.lib.modules import toolz
    toolz.ENABLE_ADDONS()


elif action == 'enableUnknownSources':
    from resources.lib.modules import toolz
    toolz.swapUS()


elif action == 'Force_Close':
    from resources.lib.modules import forceClose
    forceClose.ForceClose()


elif action == 'skinSWAP':
    from resources.lib.modules import wiz
    wiz.skinswap()


elif action == 'disableAutoUpdates':
    from resources.lib.modules import toolz
    toolz.AutoUpdateToggle_System()


elif action == 'kodishortz':
    from resources.lib.index import ezactions
    ezactions.kodiMenu()


elif action == 'kodiDBshortz':
    from resources.lib.index import ezactions
    ezactions.kodiDbMenu()


elif action == 'speedTest':
    from resources.lib.index import speedTest
    result = speedTest.fast_com()
    ok = control.OkDialog("FAST.com", "Result: %s Mbps" % result)


elif action == 'getKodiVersion':
    ummmm = control.get_Kodi_Version()
    Notify(AddonTitle, 'Kodi Version:[B] %s [/B]' % (ummmm))


elif action == 'checkCurrentProfile':
    from resources.lib.modules import toolz
    userName = toolz.Current_Profile()
    TestItem = 'Current Profile: %s' % userName
    control.Notify(AddonTitle, TestItem)


elif action == 'backup_restore':
    from resources.lib.modules import wiz
    typeOfBackup = ['BACKUP', 'RESTORE']
    s_type = control.selectDialog(typeOfBackup)
    if s_type == 0:
        modes = ['Full Backup', 'UserData Backup']
        select = control.selectDialog(modes)
        if select == 0: wiz.backup(mode='full')
        elif select == 1: wiz.backup(mode='userdata')
    elif s_type == 1: wiz.restoreFolder()


elif action == 'reloadMySkin':
    from resources.lib.modules import toolz
    yesDialog = control.yesnoDialog(AddonTitle, 'Are you sure you want to Reload Skin?', yeslabel='Yes', nolabel='No')
    if yesDialog:
        toolz.ReloadMySkin()


elif action == 'reloadProfile':
    from resources.lib.modules import toolz
    yesDialog = control.yesnoDialog(AddonTitle, 'Are you sure you want to Reload Profile?', yeslabel='Yes', nolabel='No')
    if yesDialog:
        toolz.reloadProfile(tools.getInfo('System.ProfileName'))


elif action == 'fresh_start':
    yesDialog = control.yesnoDialog(AddonTitle, 'Are you sure you want to perform a Fresh Start?', yeslabel='Yes', nolabel='No')
    if yesDialog:
        control.OkDialog(AddonTitle, 'First gotta switch the skin to the default... Confluence or Estuary...', '', '')
        from resources.lib.modules import wiz
        wiz.skinswap()
        wiz.FRESHSTART()


elif action == 'install_build':
    yesDialog = control.yesnoDialog(AddonTitle, 'Are you sure you want to Install this Build?', yeslabel='Yes', nolabel='No')
    if yesDialog:
        from resources.lib.modules import wiz
        wiz.skinswap()
        yesDialog = control.yesnoDialog(AddonTitle, 'Do you want to perform a Fresh Start before Installing your Build?', yeslabel='Yes', nolabel='No')
        if yesDialog:
            wiz.FRESHSTART(mode='silent')
        wiz.buildInstaller(url)


control.directory(int(sys.argv[1]))


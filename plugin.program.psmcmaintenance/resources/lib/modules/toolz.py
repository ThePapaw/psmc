# -*- coding: UTF-8 -*-

import re,os,sys,urllib,urllib2,time,json,zipfile
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from datetime import datetime
from resources.lib.modules import control

HOME = xbmc.translatePath('special://home/')


def Folder_Size(dirname = HOME, filesize = 'b'):
    finalsize = 0
    for dirpath, dirnames, filenames in os.walk(dirname):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            finalsize += os.path.getsize(fp)
    if filesize == 'b': # 'b'  = bytes (integer)
        return finalsize
    elif filesize == 'kb': # 'kb' = kilobytes (float to 1 decimal place)
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb': # 'mb' = kilobytes (float to 2 decimal places)
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb': # 'gb' = kilobytes (float to 3 decimal places)
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb': # 'tb' = terabytes (float to 4 decimal places)
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)


def dialogWatch():
    x = 0
    while not control.condVisibility("Window.isVisible(yesnodialog)") and x < 100:
        x += 1
        xbmc.sleep(100)
    if control.condVisibility("Window.isVisible(yesnodialog)"):
        control.execute('SendClick(11)')


def swapUS():
    new = '"addons.unknownsources"'
    value = 'true'
    query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (new)
    response = control.jsonrpc(query)
    if 'true' in response:
        xbmcgui.Dialog().notification(control.AddonTitle, "Unknown Sources: Already Enabled.")
    if 'false' in response:
        #thread.start_new_thread(dialogWatch, ())
        xbmc.sleep(200)
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
        response = control.jsonrpc(query)
        xbmcgui.Dialog().notification(control.AddonTitle, "Unknown Sources: Enabled.")


def AutoUpdateToggle_System():
    #Sets system-wide auto-update.  Change the "value" number for desired action
    # 0-auto-update, 1 -notify of updates, 2-disable auto updates. 
    control.jsonrpc('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"general.addonupdates","value":1}}')
    #control.execute('xbmc.ActivateWindow(systemsettings)')
    control.execute('xbmc.ActivateWindow(AddonBrowser)')
    control.execute('SendClick(10125, 5)')


def AutoUpdateToggle_Addon():
    #The Addons27.db has a table called blacklist.  These are the addonIDs that you won't get auto-updated.
    #Couldn't figure out how to automatically set a unique ID for the table, so I just set I set the first value(ID) to 100
    #import os,xbmc
    dataPath = xbmc.translatePath('special://userdata/Database/')
    addonsFile = os.path.join(dataPath, 'Addons27.db')
    sourceFile = addonsFile
    try:
        from sqlite3 import dbapi2 as database
    except Exception:
        from pysqlite2 import dbapi2 as database
    dbcon = database.connect(sourceFile)
    dbcur = dbcon.cursor()
    ##Enable disable toggle could go below instead of (un)commenting below code.
    ##To Add to do not auto update list
    dbcur.execute("INSERT INTO blacklist Values (?,?)", ('100','plugin.video.exodusredux'))
    dbcon.commit()
    ##To Remove from do not auto update list
    # dbcur.execute("DELETE FROM blacklist WHERE addonID = 'plugin.video.exodusredux'")
    #dbcon.commit()


def ForceUpdateCheck():
    from resources.lib.modules import control
    control.busy()
    control.execute("UpdateAddonRepos")
    control.execute("UpdateLocalAddons")
    control.idle()
    control.Notify(control.AddonTitle, 'Checking for Updates...')


def ENABLE_ADDONS():
    EXCLUDES_ADDONS = ['notification', 'packages']
    HOME_ADDONS = xbmc.translatePath('special://home/addons')
    for root, dirs, files in os.walk(HOME_ADDONS,topdown=True):
        dirs[:] = [d for d in dirs]
        for addon_name in dirs:
                if not any(value in addon_name for value in EXCLUDES_ADDONS):
                    # addLink(addon_name,'url',100,ART+'tool.png',control.AddonFanart,'')
                    try:
                        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (addon_name)
                        xbmc.executeJSONRPC(query)
                    except:
                        pass


def resetResolversCache():
    if control.condVisibility('System.HasAddon(script.module.resolveurl)'): control.execute('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')
    if control.condVisibility('System.HasAddon(script.module.urlresolver)'): control.execute('RunPlugin(plugin://script.module.urlresolver/?mode=reset_cache)')


def ReloadMySkin():
	control.execute("ReloadSkin()")


def Current_Profile(): #use
    return control.infoLabel('System.ProfileName')


def reloadProfile(profile=None):
    if profile == None:
        control.execute('LoadProfile(Master user)')
    else: control.execute('LoadProfile(%s)' % profile)


def getInfo(label):
    try: return control.infoLabel(label)
    except: return False


def net_info():
    import json
    infoLabel = ['Network.IPAddress', 'Network.MacAddress',]
    data = []; x = 0
    for info in infoLabel:
        temp = getInfo(info)
        y = 0
        while temp == "Busy" and y < 10:
            temp = getInfo(info); y += 1; xbmc.log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
        data.append(temp)
        x += 1
    try:
        url = 'http://extreme-ip-lookup.com/json/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        geo = json.load(response)
    except:
        url = 'http://ip-api.com/json'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        geo = json.load(response)
    mac = data[1]
    inter_ip = data[0]
    ip=geo['query']
    isp=geo['org']
    city = geo['city']
    country=geo['country']
    state=geo['region']
    return mac,inter_ip,ip,city,state,country,isp





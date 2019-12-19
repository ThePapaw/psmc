# -*- coding: UTF-8 -*-

import os, re, shutil, time, xbmc
from resources.lib.modules import control
try: import json as simplejson 
except: import simplejson


ADDONS = os.path.join(control.HOMEPATH, 'addons')


def currSkin():
    return control.skin


def getOld(old):
    try:
        old = '"%s"' % old
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (old)
        response = control.jsonrpc(query)
        response = simplejson.loads(response)
        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response ['result']['value']
    except:
        pass
    return None


def setNew(new, value):
    try:
        new = '"%s"' % new
        value = '"%s"' % value
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
        response = control.jsonrpc(query)
    except:
        pass
    return None


def swapSkins(skin):
    old = 'lookandfeel.skin'
    value = skin
    current = getOld(old)
    new = old
    setNew(new, value)


def lookandFeelData(do='save'):
    scan = ['lookandfeel.enablerssfeeds', 'lookandfeel.font', 'lookandfeel.rssedit', 'lookandfeel.skincolors', 'lookandfeel.skintheme', 'lookandfeel.skinzoom', 'lookandfeel.soundskin', 'lookandfeel.startupwindow', 'lookandfeel.stereostrength']
    if do == 'save':
        for item in scan:
            query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"%s"}, "id":1}' % (item)
            response = control.jsonrpc(query)
            if not 'error' in response:
                match = re.compile('{"value":(.+?)}').findall(str(response))
                control.setSetting(item.replace('lookandfeel', 'default'), match[0])
                control.log("%s saved to %s" % (item, match[0]))
    else:
        for item in scan:
            value = setting(item.replace('lookandfeel', 'default'))
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}, "id":1}' % (item, value)
            response = control.jsonrpc(query)
            control.log("%s restored to %s" % (item, value))


def defaultSkin():
    control.log("[Default Skin Check]")
    tempgui = os.path.join(USERDATAPATH, 'guitemp.xml')
    gui = tempgui if os.path.exists(tempgui) else GUISETTINGS
    if not os.path.exists(gui): return False
    control.log("Reading gui file: %s" % gui)
    guif = open(gui, 'r+')
    msg = guif.read().replace('\n','').replace('\r','').replace('\t','').replace('    ',''); guif.close()
    control.log("Opening gui settings")
    match = re.compile('<lookandfeel>.+?<ski.+?>(.+?)</skin>.+?</lookandfeel>').findall(msg)
    control.log("Matches: %s" % str(match))
    if len(match) > 0:
        skinid = match[0]
        addonxml = os.path.join(ADDONS, match[0], 'addon.xml')
        if os.path.exists(addonxml):
            addf = open(addonxml, 'r+')
            msg2 = addf.read().replace('\n','').replace('\r','').replace('\t',''); addf.close()
            match2 = re.compile('<addon.+?ame="(.+?)".+?>').findall(msg2)
            if len(match2) > 0: skinname = match2[0]
            else: skinname = 'no match'
        else: skinname = 'no file'
        control.log("[Default Skin Check] Skin name: %s" % skinname)
        control.log("[Default Skin Check] Skin id: %s" % skinid)
        control.setSetting('defaultskin', skinid)
        control.setSetting('defaultskinname', skinname)
        control.setSetting('defaultskinignore', 'false')
    if os.path.exists(tempgui):
        control.log("Deleting Temp Gui File.")
        os.remove(tempgui)
    control.log("[Default Skin Check] End")


def checkSkin():
    control.loga("Invalid Skin Check Start")
    DEFAULTSKIN = setting('defaultskin')
    DEFAULTNAME = setting('defaultskinname')
    DEFAULTIGNORE = setting('defaultskinignore')
    gotoskin = False
    if not DEFAULTSKIN == '':
        if os.path.exists(os.path.join(ADDONS, DEFAULTSKIN)):
            if DIALOG.yesno(AddonTitle, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, SKIN[5:].title()), "Would you like to set the skin back to:[/COLOR]", '[COLOR %s]%s[/COLOR]' % (COLOR1, DEFAULTNAME)):
                gotoskin = DEFAULTSKIN
                gotoname = DEFAULTNAME
            else: control.loga("Skin was not reset"); control.setSetting('defaultskinignore', 'true'); gotoskin = False
        else: control.setSetting('defaultskin', ''); control.setSetting('defaultskinname', ''); DEFAULTSKIN = ''; DEFAULTNAME = ''
    if DEFAULTSKIN == '':
        skinname = []
        skinlist = []
        for folder in glob.glob(os.path.join(ADDONS, 'skin.*/')):
            xml = "%s/addon.xml" % folder
            if os.path.exists(xml):
                f  = open(xml,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
                match = re.compile('<addon.+?id="(.+?)".+?>').findall(g)
                match2 = re.compile('<addon.+?name="(.+?)".+?>').findall(g)
                control.loga("%s: %s" % (folder, str(match[0])))
                if len(match) > 0: skinlist.append(str(match[0])); skinname.append(str(match2[0]))
                else: control.loga("ID not found for %s" % folder)
            else: control.loga("ID not found for %s" % folder)
        if len(skinlist) > 0:
            if len(skinlist) > 1:
                if DIALOG.yesno(control.AddonTitle, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, SKIN[5:].title()), "Would you like to view a list of avaliable skins?[/COLOR]"):
                    choice = DIALOG.select("Select skin to switch to!", skinname)
                    if choice == -1: control.loga("Skin was not reset"); control.setSetting('defaultskinignore', 'true')
                    else: 
                        gotoskin = skinlist[choice]
                        gotoname = skinname[choice]
                else: control.loga("Skin was not reset"); control.setSetting('defaultskinignore', 'true')
            else:
                if DIALOG.yesno(control.AddonTitle, "It seems that the skin has been set back to [B]%s[/B]" % (SKIN[5:].title()), "Would you like to set the skin back to: ", '[B] %s [/B]' % (skinname[0])):
                    gotoskin = skinlist[0]
                    gotoname = skinname[0]
                else: control.loga("Skin was not reset"); control.setSetting('defaultskinignore', 'true')
        else: control.loga("No skins found in addons folder."); control.setSetting('defaultskinignore', 'true'); gotoskin = False
    if gotoskin:
        swapSkins(gotoskin)
        x = 0
        control.sleep(1000)
        while not control.condVisibility("Window.isVisible(yesnodialog)") and x < 150:
            x += 1
            control.sleep(200)
        if control.condVisibility("Window.isVisible(yesnodialog)"):
            control.execute('SendClick(11)')
            lookandFeelData('restore')
        else: control.Notify(control.AddonTitle,'Skin Swap Timed Out!')
    control.loga("Invalid Skin Check End")



# -*- coding: UTF-8 -*-

import os
from resources.lib.modules import control

OkDialog = control.OkDialog
log = control.log

def ForceClose(): # def killxbmc():
    choice = control.yesnoDialog('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel', yeslabel='Yes, Close')
    if choice == 0: return
    elif choice == 1: pass
    myplatform = control.platform()
    log("Platform: " + str(myplatform))
    os._exit(1)
    log("Force close failed!  Trying alternate methods.")
    if myplatform == 'osx': # OSX
        log("############ try osx force close #################")
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        OkDialog("[B]WARNING !!![/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi DO NOT exit cleanly via the menu.", '')
    elif myplatform == 'linux': # Linux
        log("############ try linux force close #################")
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        OkDialog("[B]WARNING !!![/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi DO NOT exit cleanly via the menu.", '')
    elif myplatform == 'android': # Android 
        log("############ try android force close #################")
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass		
        try: os.system('adb shell kill org.xbmc.kodi')
        except: pass
        try: os.system('adb shell kill org.kodi')
        except: pass
        try: os.system('adb shell kill org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell kill org.xbmc')
        except: pass
        try: os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
        except: pass
        try: os.system('Process.killProcess(android.os.Process.org.kodi());')
        except: pass
        try: os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
        except: pass
        try: os.system('Process.killProcess(android.os.Process.org.xbmc());')
        except: pass
        OkDialog(AddonTitle, "Press the HOME button on your remote and [B]FORCE STOP[/B] KODI via the Manage Installed Applications menu in settings on your Amazon home page then re-launch KODI")
    elif myplatform == 'windows': # Windows
        log("############ try windows force close #################")
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        OkDialog("[B]WARNING !!![/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi DO NOT exit cleanly via the menu.", "Use task manager and NOT ALT F4")
    else: #ATV
        log("############ try atv force close #################")
        try: os.system('killall AppleTV')
        except: pass
        log("############ try raspbmc force close #################") # OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        OkDialog("[B]WARNING !!![/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi DO NOT exit via the menu.", "iOS detected. Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")



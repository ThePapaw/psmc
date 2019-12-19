# -*- coding: UTF-8 -*-

import os,shutil,xbmc,xbmcaddon
from resources.lib.modules import control

AddonTitle = control.AddonTitle
THUMBS = control.transPath(os.path.join('special://home/userdata/Thumbnails',''))
tempPath = control.transPath('special://temp')
databasePath = control.transPath('special://database')
thumbnailPath = control.transPath('special://thumbnails');
cachePath = os.path.join(control.transPath('special://home'), 'cache')
Notify = control.Notify

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi

    def setupCacheEntries():
        entries = 5 #make sure this refelcts the amount of entries you have
        dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
        pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                        "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                        "special://profile/addon_data/plugin.video.itv/Images"]
        cacheEntries = []
        for x in range(entries):
            cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
        return cacheEntries


def clearCache(mode='verbose'):
    if os.path.exists(cachePath)==True:
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if control.getSettingEnabled('tune.cachePath') == True:
                #if control.yesnoDialog("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log" or f == "xbmc.log" or f == "xbmc.old.log" or f == "spmc.log" or f == "spmc.old.log" or f == "psmcmaintenance.log" or f == "fuzzybritches_v2.log"): continue
                            os.unlink(os.path.join(root, f))
                        except: pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except: pass
            else:
                pass
    if os.path.exists(tempPath)==True:
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if control.getSettingEnabled('tune.tempPath') == True:
                #if control.yesnoDialog("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log" or f == "xbmc.log" or f == "xbmc.old.log" or f == "spmc.log" or f == "spmc.old.log" or f == "psmcmaintenance.log" or f == "fuzzybritches_v2.log"): continue
                            os.unlink(os.path.join(root, f))
                        except: pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except: pass
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if control.getSettingEnabled('tune.atv2_cache_a') == True:
                #if control.yesnoDialog("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if control.getSettingEnabled('tune.atv2_cache_b') == True:
                #if control.yesnoDialog("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
    cacheEntries = []
    #cacheEntries = setupCacheEntries()
    for entry in cacheEntries:
        clear_cache_path = control.transPath(entry.path)
        if os.path.exists(clear_cache_path)==True:
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    if control.getSettingEnabled('tune.cacheEntries') == True:
                    #if control.yesnoDialog("Manager",str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                else:
                    pass
    if mode == 'verbose': control.Notify(AddonTitle, 'Clean Cache Completed.', '3000')


def deleteThumbnails(mode='verbose'):
    if os.path.exists(thumbnailPath)==True:
        if control.getSettingEnabled('tune.thumbs1') == True:
        #if control.yesnoDialog("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
            for root, dirs, files in os.walk(thumbnailPath):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
    if os.path.exists(THUMBS):
        try:
            if control.getSettingEnabled('tune.thumbs2') == True:
                for root, dirs, files in os.walk(THUMBS):
                    file_count = 0
                    file_count += len(files)
                    #Count files and give option to delete
                    if file_count > 0:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
        except:
            pass
    try:
        if control.getSettingEnabled('tune.thumbs3') == True:
            text13 = os.path.join(databasePath,"Textures13.db")
            os.unlink(text13)
    except:
        pass
    if mode == 'verbose': control.Notify(AddonTitle, 'Clean Thumbs Completed.', '3000')


def purgePackages(mode='verbose'):
    purgePath = control.transPath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    if mode == 'verbose': control.Notify(AddonTitle, 'Clean Packages Completed.', '3000')


# -*- coding: UTF-8 -*-

import os,re,glob,shutil
from resources.lib.modules import control


AddonTitle = control.AddonTitle
OkDialog = control.OkDialog
yesnoDialog = control.yesnoDialog
log = control.log


def removeFile(path):
    log("Deleting File: %s" % path)
    try: os.remove(path)
    except: return False


def removeFolder(path):
    log("Deleting Folder: %s" % path)
    try: shutil.rmtree(path, ignore_errors=True, onerror=None)
    except: return False


def latestDB(DB):
    if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
        match = glob.glob(os.path.join(control.DATABASE, '%s*.db' % DB))
        comp = '%s(.+?).db' % DB[1:]
        highest = 0
        for file in match :
            try: check = int(re.compile(comp).findall(file)[0])
            except: check = 0
            if highest < check :
                highest = check
        return '%s%s.db' % (DB, highest)
    else:
        return False


def purgeDb(name):
    log('Purging DB %s.' % name)
    if os.path.exists(name):
        try:
            textdb = database.connect(name)
            textexe = textdb.cursor()
        except Exception, e: log(str(e)); return False
    else: log('%s not found.' % name); return False
    textexe.execute("""SELECT name FROM sqlite_master WHERE type = 'table';""")
    for table in textexe.fetchall():
        if table[0] == 'version': 
            log('Data from table `%s` skipped.' % table[0])
        else:
            try:
                textexe.execute("""DELETE FROM %s""" % table[0])
                textdb.commit()
                log('Data from table `%s` cleared.' % table[0])
            except e: log(str(e))
    log('%s DB Purging Complete.' % name)
    show = name.replace('\\', '/').split('/')
    control.Notify("Purge Database", "%s Complete" % show[len(show)-1])


def Clear_Thumb():
    latest = latestDB('Textures')
    if yesnoDialog(AddonTitle, "Would you like to delete the %s and Thumbnails folder?" % latest, "They will repopulate on startup", nolabel='No, Cancel', yeslabel='Yes, Remove'):
        try: removeFile(os.join(control.DATABASE, latest))
        except: log('Failed to delete, Purging DB.'); purgeDb(latest)
        removeFolder(control.THUMBSPATH)
        if yesnoDialog(AddonTitle, "Would you like to restart Kodi now?", "", nolabel='No', yeslabel='Yes'):
            from resources.lib.modules import forceClose
            forceClose.ForceClose()
        else: log('Clear Thumbnails Cancelled')
    else: log('Clear Thumbnails Cancelled')


def Delete_Packages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = control.transPath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):                      
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    OkDialog(AddonTitle, "Complete")  
    except: 
        OkDialog(AddonTitle, "Sorry we were not able to remove Package Files")


def Delete_Cache(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(control.transPath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        try:
                            if (f == "kodi.log" or f == "kodi.old.log" or f == "xbmc.log" or f == "xbmc.old.log" or f == "spmc.log" or f == "spmc.old.log" or f == "psmcmaintenance.log" or f == "fuzzybritches_v2.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
            else:
                pass
    if control.condVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found in 'Other'", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
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
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found in 'LocalAndRental'", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
    wtf_cache_path = os.path.join(control.transPath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))    
            else:
                pass
    channel4_cache_path= os.path.join(control.transPath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))    
            else:
                pass
    iplayer_cache_path= os.path.join(control.transPath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))   
            else:
                pass
    downloader_cache_path = os.path.join(control.transPath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
    itv_cache_path = os.path.join(control.transPath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + "Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))    
            else:
                pass
    temp_cache_path = os.path.join(control.transPath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                if yesnoDialog(AddonTitle, str(file_count) + " Cache files found", "Do you want to delete them?", yeslabel='YES', nolabel='NO'):
                    for f in files:
                        if (f == "kodi.log" or f == "kodi.old.log" or f == "xbmc.log" or f == "xbmc.old.log" or f == "spmc.log" or f == "spmc.old.log" or f == "psmcmaintenance.log" or f == "fuzzybritches_v2.log"): continue
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))                      
            else:
                pass
    OkDialog(AddonTitle, "Complete")  


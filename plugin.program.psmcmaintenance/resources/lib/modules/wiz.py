# -*- coding: UTF-8 -*-

import re,os,sys,urllib,time,zipfile
import xbmc,xbmcaddon,xbmcgui
from resources.lib.modules import control
from resources.lib.modules import maintenance
from datetime import datetime

AddonID = control.AddonID
AddonTitle = control.AddonTitle
Notify = control.Notify
HOME = control.transPath('special://home/') # REMOVE_EMPTY_FOLDERS, FRESHSTART,
HOMEPATH = control.transPath('special://home/') # (Favs stuff)
USERDATA = control.transPath(os.path.join('special://home/userdata','')) # (backup)
USERDATAPATH = os.path.join(HOMEPATH, 'userdata') # (Favs stuff)
ADDONDATA = os.path.join(USERDATAPATH, 'addon_data', AddonID) # (Favs stuff)
FAVOURITES = os.path.join(USERDATAPATH, 'favourites.xml') # (Favs stuff)
FAVdest = os.path.join(ADDONDATA, 'favs') # (Favs stuff)
FAVfile = os.path.join(FAVdest, 'favourites.xml') # (Favs stuff)
dialog = control.dialog # (buildInstaller)(Favs stuff)
dp = control.dp # (Favs stuff)(downloaders)

backupdir = xbmc.translatePath(os.path.join('special://home/backupdir',''))
backup_zip = xbmc.translatePath(os.path.join(backupdir,'backup_addon_data.zip'))
wizard1 = control.setting('enable_wiz1')
wizard2 = control.setting('enable_wiz2')
wizard3 = control.setting('enable_wiz3')


def ENABLE_WIZARD():
    try:
        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' %(AddonID)
        control.jsonrpc(query)
    except:
        pass


def REMOVE_EMPTY_FOLDERS():
    print"########### Start Removing Empty Folders #########"
    empty_count = 0 #initialize the counters
    used_count = 0
    try:
        for curdir, subdirs, files in os.walk(HOME):
            if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
                empty_count += 1 #increment empty_count
                os.rmdir(curdir) #delete the directory
                print "successfully removed: "+curdir
            elif len(subdirs) > 0 and len(files) > 0: #check for used directories
                used_count += 1 #increment used_count
    except: pass


def FIX_SPECIAL():
    HOME = control.transPath('special://home')
    dp.create(AddonTitle, "Renaming paths...", '', '')
    url = control.transPath('special://userdata')
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0, "Fixing", file, "Please wait.....")
                 a = open((os.path.join(root, file))).read()
                 b = a.replace(HOME, 'special://home/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()


def RESTOREFAV():
    if os.path.exists(FAVfile):
        choice = control.yesnoDialog(AddonTitle, 'Do you want to Restore your favorites?', '', '', yeslabel='[B]Yes[/B]', nolabel='[B]No[/B]')
        if choice == 0:
            return
        elif choice == 1:
            dp.create(AddonTitle, "Restoring", '', 'Please Wait')
            shutil.copy(FAVfile, USERDATAPATH)
            control.sleep(5)
            dp.close()
            dialog.ok(AddonTitle, '[B]COMPLETE[/B]', 'Your favorites are Restored.', '')
    else: Notify("[B]%s[/B]" %(AddonTitle), '[B]No Backup found![/B]')


def BACKUPFAV():
    if not os.path.exists(FAVdest): os.makedirs(FAVdest)
    if os.path.exists(FAVOURITES):
        choice = control.yesnoDialog(AddonTitle, 'Do you want to Back-up your favorites?', '', '', yeslabel='[B]Yes[/B]', nolabel='[B]No[/B]')
        if choice == 0:
            return
        elif choice == 1:
            dp.create(AddonTitle, "Backing Up Favourites", '', 'Please Wait')
            shutil.copy(FAVOURITES, FAVdest)
            control.sleep(10)
            dp.close()
            dialog.ok(AddonTitle, '[B]COMPLETE[/B]', 'Your favorites are Backed up.', '')
    else: Notify("[B]%s[/B]" %(AddonTitle), '[B]You have no Favourites![/B]')


def DELFAV():
    if os.path.exists(FAVfile):
        choice = control.yesnoDialog(AddonTitle, 'Are you sure you want to PERMANENTLY delete your backup?!?!', '', '', yeslabel='[B]Yes[/B]', nolabel='[B]No[/B]')
        if choice == 0:
            return
        elif choice == 1:
            shutil.rmtree(os.path.join(FAVdest))#(FAVdest)
            dialog.ok(AddonTitle, '[B]COMPLETE[/B]', 'Backed up deleted.', '')
    else: Notify("[B]%s[/B]" %(AddonTitle), '[B]No Backups to remove![/B]')


def FRESHSTART(mode='verbose'):
    EXCLUDES = [AddonID, 'backupdir', 'backup.zip', 'script.module.requests', 'script.module.urllib3', 'script.module.chardet', 'script.module.idna', 'script.module.certifi', 'repository.jewrepo']
    if mode!= 'silent': select = control.yesnoDialog(AddonTitle, 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='Yes',nolabel='No')
    else: select = 1
    if select == 0: return
    elif select == 1:
        dp.create(AddonTitle, 'Wiping Install', '', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    # RESTOREFAV()
    ENABLE_WIZARD()
    if mode!= 'silent': dialog.ok(AddonTitle, 'Wipe Successful, The interface will now be reset...', '', '')
    # control.execute('Mastermode')
    if mode!= 'silent': control.execute('LoadProfile(Master user)')
    # control.execute('Mastermode')


def skinswap():
    from resources.lib.modules import skinz
    skin = control.skin
    KODIV = control.get_Kodi_Version()
    skinswapped = 0
    #SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
    if skin not in ['skin.confluence', 'skin.estuary']:
        choice = dialog.yesno(AddonTitle, 'Swap to the default Kodi Skin...', 'Do you want to Proceed?', '', yeslabel='Yes', nolabel='No')
        if choice == 1:
            skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
            skinz.swapSkins(skin)
            skinswapped = 1
            time.sleep(1)
    #IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
    if skinswapped == 1:
        if not control.condVisibility("Window.isVisible(yesnodialog)"):
            control.execute( "Action(Select)" )
    #IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
    if skinswapped == 1:
        while not control.condVisibility("Window.isVisible(yesnodialog)"):
            time.sleep(1)
    #WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
    if skinswapped == 1:
        while control.condVisibility("Window.isVisible(yesnodialog)"):
            control.execute( "Action(Left)" )
            control.execute( "Action(Select)" )
            time.sleep(1)
    if skinswapped == 1:
        skin = control.skin
        #CHECK IF THE SKIN IS NOT CONFLUENCE
        if skin not in ['skin.confluence', 'skin.estuary']:
            choice = dialog.yesno(AddonTitle, '[B]ERROR: MAYBE AUTOSWITCH WAS NOT SUCCESFUL[/B]', 'CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW.', 'OR YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH.', yeslabel='YES', nolabel='NO')
            if choice == 1:
                control.execute("ActivateWindow(appearancesettings)")
                return
            else:
                sys.exit(1)


def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
            kbps_speed = numblocks * blocksize / (time.time() - start_time)
            if kbps_speed > 0:
                eta = (filesize - numblocks * blocksize) / kbps_speed
            else:
                eta = 0
            kbps_speed = kbps_speed / 1024
            total = float(filesize) / (1024 * 1024)
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total)
            e = 'Speed: %.02f Kb/s ' % kbps_speed
            e += 'ETA: %02d:%02d' % divmod(eta, 60)
            string = 'Downloading... Please Wait...'
            dp.update(percent, mbs, e, string)
        except:
            percent = 100
            dp.update(percent)
            dp.close()
            return
        if dp.iscanceled():
            raise Exception("Canceled")
            dp.close()


class customdownload(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'


def downloader(url, dest, dp = None):
    if not dp:
        dp.create(AddonTitle, "",' ', ' ')
    dp.update(0)
    start_time = time.time()
    customdownload().retrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, dp, start_time))


def ExtractNOProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
    return True


def ExtractWithProgress(_in, _out, dp):
    zin = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0
    errors = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            try: name = os.path.basename(item.filename)
            except: name = item.filename
            label = '[B]%s[/B]' % str(name)
            dp.update(int(update), 'Extracting... Errors:  ' + str(errors), label, '')
            try: zin.extract(item, _out)
            except Exception, e:
                print ("EXTRACTING ERRORS", e)
                pass
    except Exception, e:
        print str(e)
    return True


def ExtractZip(_in, _out, dp=None):
    if dp: return ExtractWithProgress(_in, _out, dp)
    return ExtractNOProgress(_in, _out)


def CreateZip(folder, zip_filename, message_header, message1, exclude_dirs, exclude_files):
    abs_src = os.path.abspath(folder)
    for_progress = []
    ITEM = []
    dp.create(message_header, message1)
    try: os.remove(zip_filename)
    except: pass
    for base, dirs, files in os.walk(folder):
        for file in files: ITEM.append(file)
    N_ITEM = len(ITEM)
    count = 0
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    for dirpath, dirnames, filenames in os.walk(folder):
        try:
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
            filenames[:] = [f for f in filenames if f not in exclude_files]
            for file in filenames:
                if file.endswith('.pyo'): continue
                elif file.endswith('.pyc'): continue
                elif file.endswith('.csv'): continue
                elif file.endswith('.log'): continue
                elif 'kodi_backup' in zip_filename:
                    if file.endswith('.db') and 'addon_data' in dirpath:
                        continue
                count += 1
                for_progress.append(file)
                progress = len(for_progress) / float(N_ITEM) * 100
                dp.update(int(progress), "Backing Up", 'FILES: ' + str(count) + '/' + str(N_ITEM)  + '  [B]' + str(file) + '[/B]', 'Please Wait')
                file = os.path.join(dirpath, file)
                file = os.path.normpath(file)
                arcname = file[len(abs_src) + 1:]
                zip_file.write(file, arcname)
        except: pass
    zip_file.close()


def restoreFolder():
    names = []
    links = []
    zipFolder = control.setting('restore.path')
    if zipFolder == '' or zipFolder == None:
        control.infoDialog('Please Setup a Zip Files Location first')
        control.openSettings(query='2.0')
        return
    for zipFile in os.listdir(zipFolder):
            if zipFile.endswith(".zip"):
                url = control.transPath(os.path.join(zipFolder, zipFile))
                names.append(zipFile)
                links.append(url)
    select = control.selectDialog(names)
    if select!= -1: restore(links[select])


def restore(zipFile):
    yesDialog = dialog.yesno(AddonTitle, 'This will overwrite all your current settings ... Are you sure?', yeslabel='Yes', nolabel='No')
    if yesDialog:
        try:
            dp.create("Restoring File", "In Progress...", '', 'Please Wait')
            dp.update(0, "", "Extracting Zip Please Wait")
            ExtractZip(zipFile, HOME, dp)
            dialog.ok(AddonTitle, 'Restore Complete', '', '')
            ForceClose()
            #control.execute('ShutDown') #Testing with ForceClose()
        except: pass


def buildInstaller(url):
    destination = dialog.browse(type=0, heading='Select Download Directory', shares='files', useThumbs=True, treatAsFolder=True, enableMultiple=False)
    if destination:
        dest = control.transPath(os.path.join(destination, 'custom_build.zip'))
        downloader(url, dest)
        time.sleep(2)
        dp.create("Installing Build", "In Progress...", '', 'Please Wait')
        dp.update(0, "", "Extracting Zip Please Wait")
        ExtractZip(dest, HOME, dp)
        time.sleep(2)
        dp.close()
        dialog.ok(AddonTitle, 'Installation Complete...', 'Your interface will now be reset', 'Click ok to Start...')
        control.execute('LoadProfile(Master user)')


def backup(mode='full'):
    KODIV = control.get_Kodi_Version()
    backupdir = control.setting('download.path')
    if backupdir == '' or backupdir == None:
        control.infoDialog('Please Setup a Path for Downlads first')
        control.openSettings(query='1.3')
        return
    if mode == 'full':
        defaultName = "kodi_backup"
        BACKUPDATA = HOME
        FIX_SPECIAL()
    elif mode == 'userdata':
        defaultName = "kodi_userdata"
        BACKUPDATA = USERDATA
    else: return
    if os.path.exists(BACKUPDATA):
        if not backupdir == '':
            name = control.get_keyboard(default=defaultName, heading='Name your Backup')
            today = datetime.now().strftime('%Y%m%d%H%M')
            today = re.sub('[^0-9]', '', str(today))
            zipDATE = "_%s.zip" % today
            name = re.sub(' ', '_', name) + zipDATE
            backup_zip = control.transPath(os.path.join(backupdir, name))
            exclude_database = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
            try:
                maintenance.clearCache(mode='silent')
                maintenance.deleteThumbnails(mode='silent')
                maintenance.purgePackages(mode='silent')
            except: pass
            exclude_dirs = ['cache', 'system', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'keymaps', 'cdm']
            CreateZip(BACKUPDATA, backup_zip, 'Creating Backup', 'Backing up files', exclude_dirs, exclude_database)
            dialog.ok(AddonTitle, 'Backup complete', '', '')
        else:
            dialog.ok(AddonTitle, 'No backup location found. Please setup your Backup location', '', '')



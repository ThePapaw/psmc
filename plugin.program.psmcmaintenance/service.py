# -*- coding: UTF-8 -*-

import os
from resources.lib.modules import control,maintenance

AddonTitle = control.AddonTitle
packagesdir = control.transPath('special://home/addons/packages')
thumbnails = control.transPath('special://home/userdata/Thumbnails')

notify_mode = control.getSetting('notify_mode')
auto_checkup = control.getSetting('auto_check4updates')
auto_clean = control.getSetting('startup.cache')
service_package = control.getSetting('service_package')
filesize = int(control.getSetting('filesize_alert'))
maxpackage_zips = int(control.getSetting('packagenumbers_alert'))
service_thumbnails = control.getSetting('service_thumbnails')
filesize_thumb = int(control.getSetting('filesizethumb_alert'))

#control.loga("[ Addon Startup ] [ v.%s ]" % control.AddonVersion) # Removed for now, causes a error on windows10. gotta look into it lol.
total_size = 0
total_size2 = 0
count = 0
count2 = 0

for dirpath, dirnames, filenames in os.walk(packagesdir):
    count = 0
    for f in filenames:
        count += 1
        fp = os.path.join(dirpath, f)
        total_size += os.path.getsize(fp)
    total_sizetext = "%.0f" % (total_size/1024000.0)
    if service_package == 'true':
        if count > maxpackage_zips or int(total_sizetext) > filesize:
            choice2 = control.yesnoDialog(AddonTitle, 'The Packages folder is [B]' + str(total_sizetext) +' MB[/B] \n\n with [B]' + str(count) + '[/B] zips.', 'The folder can be cleaned up without issues to save space...', 'Do you want to clean it now?', yeslabel='Yes', nolabel='No')
            if choice2 == 1:
                maintenance.purgePackages()
                #control.loga("[ Packages Cleared. ]")

for dirpath2, dirnames2, filenames2 in os.walk(thumbnails):
    count2 = 0
    for f2 in filenames2:
        count2 += 1
        fp2 = os.path.join(dirpath2, f2)
        total_size2 += os.path.getsize(fp2)
    total_sizetext2 = "%.0f" % (total_size2/1024000.0)
    if service_thumbnails == 'true':
        if int(total_sizetext2) > filesize_thumb:
            choice2 = control.yesnoDialog(AddonTitle, 'The Thumbnails folder is [B]' + str(total_sizetext2) + ' MB[/B] \n\n with [B]' + str(count2) + '[/B] files.', 'The folder can be cleaned up without issues to save space...', 'Do you want to clean it now?', yeslabel='Yes', nolabel='No')
            if choice2 == 1:
                maintenance.deleteThumbnails()
                #control.loga("[ Thumbnails Cleared. ]")

if auto_clean  == 'true':
    maintenance.clearCache()
    #control.loga("[ Cache Cleared. ]")

if notify_mode == 'true':
    total_sizetext = "%.0f" % (total_size/1024000.0)
    total_sizetext2 = "%.0f" % (total_size2/1024000.0)
    control.execute('XBMC.Notification(%s, %s, %s, %s)' % (AddonTitle, 'Packages: [B]' + str(count) + '[/B] @ [B]' + str(total_sizetext) + '[/B] MB                                                                                                       Thumbnails: [B]' + str(total_sizetext2) + '[/B] MB', '6000', control.AddonIcon))
    #control.loga('Packages: ' + str(count) + ' @ ' + str(total_sizetext) + ' MB | Thumbnails: ' + str(total_sizetext2) + ' MB')

if auto_checkup  == 'true':
    from resources.lib.modules import toolz
    toolz.ForceUpdateCheck()
    #control.loga("[ Auto Check for Updates. ]")


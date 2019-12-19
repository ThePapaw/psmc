# -*- coding: UTF-8 -*-

import re,os,sys,urllib,urllib2,glob,requests,time,shutil
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from datetime import date, datetime, timedelta
from urllib2 import urlopen
from resources.lib.modules import control

AddonID = control.AddonID
AddonTitle = control.AddonTitle
Notify = control.Notify
getSetEnabled = control.getSettingEnabled
log = control.log
logfile_path = xbmc.translatePath('special://logpath/')
dialog = control.dialog
dp = control.dp


def OPEN_URL_NORMAL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'python-requests/2.9.1')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link  


def Delete_Crash_Logs(over=None):
    crashfiles = []
    tracefiles = []
    for file in glob.glob(os.path.join(logfile_path, '*crashlog*.*')):
        crashfiles.append(file)
    for file in glob.glob(os.path.join(logfile_path, '*stacktrace*.*')):
        tracefiles.append(file)
    totalfiles = len(crashfiles) + len(tracefiles)
    if totalfiles > 0:
        if over:
            yes=1
        else:
            yes=dialog.yesno(AddonTitle, 'Would you like to delete the Crash logs?', '%s Files Found' % (totalfiles), nolabel="No, Cancel", yeslabel="Yes, Remove")
        if yes:
            if len(crashfiles) > 0:
                for f in crashfiles:
                    os.remove(f)
            if len(tracefiles) > 0:
                for f in tracefiles:
                    os.remove(f)
            Notify(AddonTitle, 'Clear Crash Logs: %s Crash Logs Removed' % (totalfiles))
        else:
            Notify(AddonTitle, 'Clear Crash Logs: Clear Crash Logs Cancelled')
    else:
        Notify(AddonTitle, 'Clear Crash Logs: No Crash Logs Found')


def Delete_DebugLogs():
    debuglogfiles = []
    for file in glob.glob(os.path.join(logfile_path, '*.*log*')):
        debuglogfiles.append(file)
    totalfiles = len(debuglogfiles)
    if totalfiles > 0:
        yes = dialog.yesno(AddonTitle, 'Would you like to delete the Debug Logs?', '%s Files Found' % (totalfiles), nolabel="No, Cancel", yeslabel="Yes, Remove")
        if yes:
            if len(debuglogfiles) > 0:
                for f in debuglogfiles:
                    os.remove(f)
            Notify(AddonTitle, 'Clear Debug Logs: %s Removed.' % (totalfiles))
            log('Clear Debug Logs: %s Removed.' % (totalfiles))
        else:
            Notify(AddonTitle, 'Clear Debug Logs: Cancelled.')
            log('Clear Debug Logs: Cancelled.')
    else:
        Notify(AddonTitle, 'Clear Debug Logs: No Debug Logs Found.')
        log('Clear Debug Logs: No Debug Logs Found.')


def logView():
    modes = ['View Log', 'Upload Log (Pastebin)']
    logPaths = []
    logNames = []
    select = control.selectDialog(modes)
    try:
        if select == -1: raise Exception()
        logfile_names = ('kodi.log', 'kodi.old.log', 'xbmc.log', 'xbmc.old.log', 'spmc.log', 'spmc.old.log', 'psmcmaintenance.log', 'fuzzybritches_v2.log')
        for logfile_name in logfile_names:
            log_file_path = os.path.join(logfile_path, logfile_name)
            if os.path.isfile(log_file_path):
                logNames.append(logfile_name)
                logPaths.append(log_file_path)
        selectLog = control.selectDialog(logNames)
        selectedLog = logPaths[selectLog]
        if selectLog == -1: raise Exception()
        if select == 0:
            from resources.lib.api import TextViewer
            TextViewer.text_view(selectedLog)
        elif select == 1:
            f = open(selectedLog, 'r')
            text = f.read()
            f.close()
            from resources.lib.api import PasteBin
            upload_Link = PasteBin.api().paste(text)
            print ("LOGVIEW UPLOADED LINK", upload_Link)
            if upload_Link != None:
                if not "Error" in upload_Link:
                    Color1 = 'purple'
                    label = "Log Link: [COLOR %s][B] %s [/B][/COLOR]" % (Color1, upload_Link)
                    dialog.ok(AddonTitle, "Log Uploaded to Pastebin", label)
                else: dialog.ok(AddonTitle, "Cannot Upload Log to Pastebin", "Reason " + upload_Link)
            else: dialog.ok(AddonTitle, "Cannot Upload Log to Pastebin", "")
    except:
        pass


def Broken_Sources():
    SOURCES_FILE =  xbmc.translatePath('special://home/userdata/sources.xml')
    if not os.path.isfile(SOURCES_FILE):
        dialog.ok(AddonTitle,'Error: It appears you do not currently have a sources.xml file on your system. We are unable to perform this test.')
        sys.exit(0)
    dp.create(AddonTitle,"Testing Internet Connection...", '', 'Please Wait...') 
    try: OPEN_URL_NORMAL("http://www.google.com")
    except:
        dialog.ok(AddonTitle, 'Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.')
        sys.exit(0)
    found = 0
    passed = 0
    dp.update(0, "Checking Sources...", '', 'Please Wait...') 
    a=open(SOURCES_FILE).read() 
    b=a.replace('\n','U').replace('\r','F')
    match=re.compile('<source>(.+?)</source>').findall(str(b))
    counter = 0
    for item in match:
        name=re.compile('<name>(.+?)</name>').findall(item)[0]
        checker=re.compile('<path pathversion="1">(.+?)</path>').findall(item)[0]
        if "http" in str(checker):
            dp.update(0, "", "Checking: " + name, "")
            try:
                checkme = requests.get(checker, timeout=30)
            except:
                checkme = "null"
                pass
            try:
                error_out = 0
                if not "this does not matter its just a test" in ("%s" % checkme.text):
                    error_out = 0
            except:
                error_out = 1
            if error_out == 0:
                if not ".zip" in ("%s" % checkme.text):     
                    if not "repo" in ("%s" % checkme.text):                 
                        choice = xbmcgui.Dialog().yesno("Error conencting to the following: ", "Source Name: " + name, "Source URL: " + checker, "Would you like to remove this source now?", yeslabel='YES', nolabel='NO')
                        counter = counter + 1
                        if choice == 1:
                            found = 1
                            h=open(SOURCES_FILE).read()
                            i=h.replace('\n','U').replace('\r','F')
                            j=i.replace(str(item), '')
                            k=j.replace('U','\n').replace('F','\r')
                            l=k.replace('<source></source>','').replace('        \n','')
                            f= open(SOURCES_FILE, mode='w')
                            f.write(l)
                            f.close()
                    else:
                        passed = passed + 1
                else:
                    passed = passed + 1
            else:
                choice = xbmcgui.Dialog().yesno("Error conencting to the following: ", "Source Name: " + name, "Source URL: " + checker, "Would you like to remove this source now?", yeslabel='YES', nolabel='NO')
                counter = counter + 1
                if choice == 1:
                    found = 1
                    h=open(SOURCES_FILE).read()
                    i=h.replace('\n','U').replace('\r','F')
                    j=i.replace(str(item), '')
                    k=j.replace('U','\n').replace('F','\r')
                    l=k.replace('<source></source>','').replace('        \n','')
                    f= open(SOURCES_FILE, mode='w')
                    f.write(l)
                    f.close()
                else:
                    passed = passed + 1
            if dp.iscanceled():
                dialog.ok(AddonTitle, 'The source check was cancelled')
                dp.close()
                sys.exit()
            dp.update(0, "", "", "Alive: " + str(passed) + "        Dead: " + str(counter))
    dialog.ok(AddonTitle, 'We have checked your sources and found:', 'WORKING SOURCES: ' + str(passed), 'DEAD SOURCES: ' + str(counter))


def Broken_Repos():
    dp.create(AddonTitle, "Testing Internet Connection...", '', 'Please Wait...') 
    try:
        OPEN_URL_NORMAL("http://www.google.com")
    except:
        dialog.ok(AddonTitle, 'Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.')
        sys.exit(0)
    passed = 0
    failed = 0
    HOMEPATH =  xbmc.translatePath('special://home/addons/')
    dp.update(0, "We are currently checking:", '', "Alive: " + "0" + "       Dead: " + "0")
    url = HOMEPATH
    for root, dirs, files in os.walk(url):
        for file in files:
            if file == "addon.xml":
                a=open((os.path.join(root, file))).read()   
                if "info compressed=" in str(a):
                    match = re.compile('<info compressed="false">(.+?)</info>').findall(a)
                    for checker in match:
                        dp.update(0, "", checker, "")
                        try:
                            Common.OPEN_URL_NORMAL(checker, timeout=30)
                            passed = passed + 1
                        except:
                            try:
                                checkme = requests.get(checker, timeout=30)
                            except:
                                pass
                            try:
                                error_out = 0
                                if not "this does not matter its just a test" in ("%s" % checkme.text):
                                    error_out = 0
                            except:
                                error_out = 1
                            if error_out == 0:
                                if not "addon id=" in ("%s" % checkme.text):    
                                    failed = failed + 1
                                    match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                    for repo_id,repo_name in match:
                                        default_path = xbmc.translatePath("special://home/addons/")
                                        file_path = xbmc.translatePath(file)
                                        full_path = default_path + repo_id
                                        choice = xbmcgui.Dialog().yesno(AddonTitle, "The " + repo_name + " appears to be broken. We attempted to connect to the repo but it was unsuccessful.", 'To remove this repository please click YES', yeslabel='YES', nolabel='NO')
                                        if choice == 1:
                                            try:
                                                shutil.rmtree(full_path)
                                            except:
                                                dialog.ok(AddonTitle, "Sorry we were unable to remove " + repo_name)
                                else:
                                    passed = passed + 1
                            else:
                                failed = failed + 1
                                match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                for repo_id,repo_name in match:
                                    default_path = control.transPath("special://home/addons/")
                                    file_path = control.transPath(file)
                                    full_path = default_path + repo_id
                                    choice = dialog.yesno(AddonTitle, "The " + repo_name + " appears to be broken. We attempted to connect to the repo but it was unsuccessful.", 'To remove this repository please click YES', yeslabel='YES', nolabel='NO')
                                    if choice == 1:
                                        try:
                                            shutil.rmtree(full_path)
                                        except:
                                            dialog.ok(AddonTitle, "Sorry we were unable to remove " + repo_name)
                        if dp.iscanceled():
                            dialog.ok(AddonTitle, 'The repository check was cancelled')
                            dp.close()
                            sys.exit()
                        dp.update(0, "", "", "Alive: " + str(passed) + "       Dead: " + str(failed))
    dialog.ok(AddonTitle, 'We have checked your repositories and found:', 'Working Repositories: ' + str(passed), 'Dead Repositories: ' + str(failed))



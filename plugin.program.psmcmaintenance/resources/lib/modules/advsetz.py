# -*- coding: UTF-8 -*-

import re,os,sys
from resources.lib.modules import control


AddonTitle = control.AddonTitle
AdvancedSettingsFile = control.transPath(os.path.join('special://profile/', 'advancedsettings.xml'))
dialog = control.dialog


def xml_data_advSettings_old(size):
    xml_data = """<advancedsettings>
      <network>
        <curlclienttimeout>10</curlclienttimeout>
        <curllowspeedtime>20</curllowspeedtime>
        <curlretries>2</curlretries>
        <cachemembuffersize>%s</cachemembuffersize>
        <buffermode>2</buffermode>
        <readbufferfactor>20</readbufferfactor>
      </network>
</advancedsettings>""" % size
    return xml_data


def xml_data_advSettings_New(size):
    xml_data = """<advancedsettings>
      <network>
        <curlclienttimeout>10</curlclienttimeout>
        <curllowspeedtime>20</curllowspeedtime>
        <curlretries>2</curlretries>
      </network>
      <cache>
        <memorysize>%s</memorysize>
        <buffermode>2</buffermode>
        <readfactor>20</readfactor>
      </cache>
</advancedsettings>""" % size
    return xml_data


def advancedSettings():
    MEM = control.infoLabel("System.Memory(total)")
    FREEMEM = control.infoLabel("System.FreeMemory")
    BUFFER_F = re.sub('[^0-9]', '', FREEMEM)
    BUFFER_F = int(BUFFER_F) / 3
    BUFFERSIZE = BUFFER_F * 1024 * 1024
    try: KODIV = control.get_Kodi_Version()
    except: KODIV = 16
    choice = dialog.yesno(AddonTitle, 'Free Memory: [B]' + str(FREEMEM) + '[/B]', 'Optimal BufferSize is: [B]' + str(BUFFER_F) + ' MB[/B]', 'Choose an Option below...', yeslabel='[COLOR lime][B]Use Optimal[/B][/COLOR]', nolabel='[COLOR red]Input a Value[/COLOR]')
    if choice == 1:
        with open(AdvancedSettingsFile, "w") as f:
            if KODIV >= 17: xml_data = xml_data_advSettings_New(str(BUFFERSIZE))
            else: xml_data = xml_data_advSettings_old(str(BUFFERSIZE))
            f.write(xml_data)
            dialog.ok(AddonTitle, 'Buffer Size Set to: [B]' + str(BUFFERSIZE) + '[/B]  aka  [B]' + str(BUFFER_F) + ' MB[/B]', 'Please restart Kodi for the settings to apply.', '')
    elif choice == 0:
        BUFFERSIZE = control.get_keyboard( default=str(BUFFERSIZE), heading="INPUT BUFFER SIZE")
        with open(AdvancedSettingsFile, "w") as f:
            if KODIV >= 17: xml_data = xml_data_advSettings_New(str(BUFFERSIZE))
            else: xml_data = xml_data_advSettings_old(str(BUFFERSIZE))
            f.write(xml_data)
            dialog.ok(AddonTitle, 'Buffer Size Set to: [B]' + str(BUFFERSIZE) + '[/B]', 'Please restart Kodi for the settings to apply.', '')


def viewAdvancedSettings():
    try:
        from resources.lib.api import TextViewer
        TextViewer.text_view(AdvancedSettingsFile)
    except:
        dialog.ok(AddonTitle, "Error", 'Unable to view the advancedsettings.xml file.', 'Might not have one yet.')
        sys.exit(0)


def clearAdvancedSettings():
    try:
        os.remove(AdvancedSettingsFile)
        dialog.ok(AddonTitle, "Success", 'The advancedsettings.xml has been removed.')
    except:
        dialog.ok(AddonTitle, "Error", 'Unable to remove the advancedsettings.xml file.', 'Might not have one yet.')
        sys.exit(0)



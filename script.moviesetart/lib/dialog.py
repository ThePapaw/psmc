# -*- coding: utf-8 -*-

import xbmcaddon, xbmc, xbmcgui

__addon__              = xbmcaddon.Addon( "script.moviesetart" )
__language__           = __addon__.getLocalizedString
__scriptname__         = __addon__.getAddonInfo('name')

dialog = xbmcgui.DialogProgress()

def dialog_msg(action,
               percent = 0,
               heading = '',
               line1 = '',
               line2 = '',
               line3 = '',
               nolabel = __language__(32005),
               yeslabel = __language__(32004)):
    # Fix possible unicode errors 
    heading = heading.encode( 'utf-8', 'ignore' )
    line1 = line1.encode( 'utf-8', 'ignore' )
    line2 = line2.encode( 'utf-8', 'ignore' )
    line3 = line3.encode( 'utf-8', 'ignore' )
    # Dialog logic
    if not heading == '':
        heading = heading
    else:
        heading = __scriptname__
    if not line1:
        line1 = ""
    if not line2:
        line2 = ""
    if not line3:
        line3 = ""
    if action == 'create':
        dialog.create( heading, line1, line2, line3 )
    if action == 'update':
        dialog.update( percent, line1, line2, line3 )
    if action == 'close':
        dialog.close()
    if action == 'iscanceled':
        if dialog.iscanceled():
            return True
        else:
            return False
    if action == 'okdialog':
        xbmcgui.Dialog().ok(heading, line1, line2, line3)
    if action == 'yesno':
        return xbmcgui.Dialog().yesno(heading, line1, line2, line3, nolabel, yeslabel)

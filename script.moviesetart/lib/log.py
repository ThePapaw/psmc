# -*- coding: utf-8 -*-

import xbmc, xbmcaddon

__addon__              = xbmcaddon.Addon( "script.moviesetart" )
__scriptname__         = __addon__.getAddonInfo('name')

# Method to log a message with the script name as prefix
def log( text, severity=xbmc.LOGDEBUG ):
    try:
        message = ('[%s] - %s' % ( __scriptname__ ,text) )
        xbmc.log( msg=message, level=severity)
    except:
        message = repr('[%s] - %s' % ( __scriptname__ ,text) )
        xbmc.log( msg=message, level=severity )
        

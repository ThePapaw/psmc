import sys, urllib, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

sysarg=str(sys.argv[1])
ADDON_ID='script.realdebrid.mod'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

# the main menu structure
mainMenu=[
    {
        "title":"Unrestrict Link", 
        "url":"", 
        "mode":5, 
        "poster":"none",
        "icon":os.path.join(home, '', 'icon.png'),
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
        "isPlayable":True
    },
    {
        "title":"Add Torrent File", 
        "url":"", 
        "mode":3, 
        "poster":"none",
        "icon":os.path.join(home, '', 'icon.png'),
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
    },
    {
        "title":"Add Magnet Link", 
        "url":"", 
        "mode":4, 
        "poster":"none",
        "icon":os.path.join(home, '', 'icon.png'),
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":False,
    },
    {
        "title":"View Torrents", 
        "url":"", 
        "mode":1, 
        "poster":"none",
        "icon":os.path.join(home, '', 'icon.png'),
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
        "extras":{"offset":"0", "limit":"100"}
    },
    {
        "title":"View Unrestricted Links", 
        "url":"", 
        "mode":2, 
        "poster":"none",
        "icon":os.path.join(home, '', 'icon.png'),
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
        "extras":{"offset":"0", "limit":"100"}
    }
    ,
    {
        "title":"View Host Statuses", 
        "url":"", 
        "mode":7, 
        "poster":"none",
        "icon":os.path.join(home, '', 'icon.png'),
        "fanart":os.path.join(home, '', 'fanart.jpg'),
        "type":"", 
        "plot":"",
        "isFolder":True,
        "extras":{"offset":"0", "limit":"100"}
    }
]
# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches
# Addon id: script.module.fuzzybritches
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import os, re, shutil, time, xbmc
try:
    import json as simplejson
except:
    import simplejson

def getOld(old):
    try:
        old = '"%s"' % old
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (old)
        response = xbmc.executeJSONRPC(query)
        response = simplejson.loads(response)
        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response ['result']['value']
    except:
        pass
    return None

def setNew(new, value):
    try:
        new = '"%s"' % new
        value = '"%s"' % value
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
        response = xbmc.executeJSONRPC(query)
    except:
        pass
    return None

def swapSkins(skin):
    old = 'lookandfeel.skin'
    value = skin
    current = getOld(old)
    new = old
    setNew(new, value)
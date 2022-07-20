#!/usr/bin/python
# coding: utf8

import xbmc
import xbmcaddon
import xbmcgui              
import simplejson

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

INFO = xbmc.LOGINFO
WARNING = xbmc.LOGWARNING
DEBUG = xbmc.LOGDEBUG
LOG_ENABLED = True if ADDON.getSetting('log') == 'true' else False
DEBUGLOG_ENABLED = True if ADDON.getSetting('debuglog') == 'true' else False


def get_kodiversion():
    build = xbmc.getInfoLabel('System.BuildVersion')
    return int(build[:2])

def log(txt,loglevel=INFO,force=False):
    if ((loglevel == INFO or loglevel == WARNING) and LOG_ENABLED) or (loglevel == DEBUG and DEBUGLOG_ENABLED) or force:

        # Python 2 requires to decode stuff at first
        try:
            if isinstance(txt, str):
                txt = txt
        except AttributeError:
            pass

        message = '[ %s ] %s' % (ADDON_ID,txt)

        try:
            xbmc.log(msg=message.encode('utf-8'), level=loglevel) # Python 2
        except TypeError:
            xbmc.log(msg=message, level=loglevel)

def visible(condition):
    return xbmc.getCondVisibility(condition)

def get_first_youtube_video(query):
    for media in get_youtube_listing('%s' % query, limit=5):
        if media["filetype"] != "directory":
            return media["file"]
    return ""

def get_youtube_listing(searchquery, limit=None):
    """get items from youtube plugin by query"""
    lib_path = u"plugin://plugin.video.youtube/kodion/search/query/?q=%s&search_type=videos" % searchquery
    files_query = json_call('Files.GetDirectory',
                              params={'directory': lib_path},
                              limit=limit)
    result = []
    if 'result' in files_query:
        for key, value in files_query['result'].items():
            if not key == "limits" and (isinstance(value, list) or isinstance(value, dict)):
                result = value
    return result

def json_call(method,properties=None,sort=None,query_filter=None,limit=None,params=None,item=None):

    json_string = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}

    if properties is not None:
        json_string['params']['properties'] = properties

    if limit is not None:
        json_string['params']['limits'] = {'start': 0, 'end': limit}

    if sort is not None:
        json_string['params']['sort'] = sort

    if query_filter is not None:
        json_string['params']['filter'] = query_filter

    if item is not None:
        json_string['params']['item'] = item

    if params is not None:
        json_string['params'].update(params)

    json_string = simplejson.dumps(json_string)

    result = xbmc.executeJSONRPC(json_string)

    # Python 2 compatibility
    try:
        result = unicode(result, 'utf-8', errors='ignore')
    except NameError:
        pass

    result = simplejson.loads(result)

    log('json-string: %s' % json_string, DEBUG)
    log('json-result: %s' % result, DEBUG)

    return result


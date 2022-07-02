# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v3
# Addon id: plugin.video.fuzzybritches_v3
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import simplejson as json
from resources.lib.modules import client

URL_PATTERN = 'http://thexem.de/map/single?id=%s&origin=tvdb&season=%s&episode=%s&destination=scene'

def get_scene_episode_number(tvdbid, season, episode):

    try:
        url = URL_PATTERN % (tvdbid, season, episode)
        r = client.request(url)
        r = json.loads(r)
        if r['result'] == 'success':
            data = r['data']['scene']
            return data['season'], data['episode']
    except:
        pass

    return season, episode

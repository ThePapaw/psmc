# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v3 Scrapers
# Addon id: script.module.fuzzybritchesv3scrapers
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

#import urlparse, urllib
from six.moves import urllib_parse

from fuzzybritchesscrapers.modules import cache
from fuzzybritchesscrapers.modules import client
from fuzzybritchesscrapers.modules import cleantitle
from fuzzybritchesscrapers.modules import utils


def _getAniList(url):
    try:
        url = urllib_parse.urljoin('https://anilist.co', '/api%s' % url)
        return client.request(url, headers={'Authorization': '%s %s' % cache.get(_getToken, 1), 'Content-Type': 'application/x-www-form-urlencoded'})
    except:
        pass


def _getToken():
    result = urllib_parse.urlencode({'grant_type': 'client_credentials', 'client_id': 'kodiexodus-7erse', 'client_secret': 'XelwkDEccpHX2uO8NpqIjVf6zeg'})
    result = client.request('https://anilist.co/api/auth/access_token', post=result, headers={'Content-Type': 'application/x-www-form-urlencoded'}, error=True)
    result = utils.json_loads_as_str(result)
    return result['token_type'], result['access_token']


def getAlternativTitle(title):
    try:
        t = cleantitle.get(title)

        r = _getAniList('/anime/search/%s' % title)
        r = [(i.get('title_romaji'), i.get('synonyms', [])) for i in utils.json_loads_as_str(r) if cleantitle.get(i.get('title_english', '')) == t]
        r = [i[1][0] if i[0] == title and len(i[1]) > 0 else i[0] for i in r]
        r = [i for i in r if i if i != title][0]
        return r
    except:
        pass

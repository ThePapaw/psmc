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

import re
import urllib
import urlparse
import json
from promisescrapers.modules import cleantitle
from promisescrapers.modules import dom_parser
from promisescrapers.modules import source_utils
from promisescrapers import cfScraper


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123123movies.net']
        self.base_link = 'https://www1.123moviesto.to'
        self.search_link = '/search/%s %s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (clean_title, year)))
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            clean_title = cleantitle.geturl(url['tvshowtitle']) + '-s%02d' % int(season)
            url = urlparse.urljoin(self.base_link, (self.search_link % (clean_title, url['year'])))
            r = cfScraper.get(url).content
            r = dom_parser.parse_dom(r, 'div', {'id': 'ip_episode'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            for i in r[0]:
                if i.content == 'Episode %s' % episode:
                    url = i.attrs['href']
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict

            if url == None: return sources

            r = cfScraper.get(url).content
            quality = re.findall(">(\w+)<\/p", r)
            if quality[0] == "HD":
                quality = "720p"
            else:
                quality = "SD"
            r = dom_parser.parse_dom(r, 'div', {'id': 'servers-list'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]

            for i in r[0]:
                url = {'url': i.attrs['href'], 'data-film': i.attrs['data-film'], 'data-server': i.attrs['data-server'],
                       'data-name': i.attrs['data-name']}
                url = urllib.urlencode(url)
                valid, host = source_utils.is_host_valid(i.content, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return

    def resolve(self, url):
        try:
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            post = {'ipplugins': 1, 'ip_film': urldata['data-film'], 'ip_server': urldata['data-server'], 'ip_name': urldata['data-name'], 'fix': "0"}
            cfScraper.headers.update({'Referer': urldata['url'], 'X-Requested-With': 'XMLHttpRequest'})
            p1 = cfScraper.post('http://123123movies.net/ip.file/swf/plugins/ipplugins.php', data=post).content
            p1 = json.loads(p1)
            p2 = cfScraper.get('http://123123movies.net/ip.file/swf/ipplayer/ipplayer.php?u=%s&s=%s&n=0' % (
            p1['s'], urldata['data-server'])).content
            p2 = json.loads(p2)
            p3 = cfScraper.get('http://123123movies.net/ip.file/swf/ipplayer/api.php?hash=%s' % (p2['hash'])).content
            p3 = json.loads(p3)
            n = p3['status']
            if n == False:
                p2 = cfScraper.get('http://123123movies.net/ip.file/swf/ipplayer/ipplayer.php?u=%s&s=%s&n=1' % (
                p1['s'], urldata['data-server'])).content
                p2 = json.loads(p2)
            url = "https:%s" % p2["data"].replace("\/", "/")
            return url
        except:
            return

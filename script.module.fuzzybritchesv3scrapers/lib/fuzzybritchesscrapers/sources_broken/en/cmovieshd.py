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
from promisescrapers.modules import cleantitle
from promisescrapers.modules import source_utils
from promisescrapers import cfScraper


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cmovieshd.bz']
        self.base_link = 'https://www2.cmovies.ac/'
        self.search_link = '/film/%s/watching.html?ep=0'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.search_link % title
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            r = cfScraper.get(url).content
            qual = re.compile('class="quality">(.+?)</span>').findall(r)
            for i in qual:
                info = i
                if '1080' in i:
                    quality = '1080p'
                elif '720' in i:
                    quality = '720p'
                else:
                    quality = 'SD'
            u = re.compile('data-video="(.+?)"').findall(r)
            for url in u:
                if not url.startswith('http'):
                    url =  "https:" + url
                if 'vidcloud' in url:
                    r = cfScraper.get(url).content
                    t = re.compile('data-video="(.+?)"').findall(r)
                    for url in t:
                        if not url.startswith('http'):
                            url =  "https:" + url
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid and 'vidcloud' not in url:
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url



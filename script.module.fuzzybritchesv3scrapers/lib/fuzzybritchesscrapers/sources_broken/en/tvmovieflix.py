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

import re,requests
from promisescrapers.modules import cleantitle
from promisescrapers.modules import source_utils
from promisescrapers import cfScraper


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['tvmovieflix.com']
        self.base_link = 'http://tvmovieflix.com'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + '/movies/%s' % (mtitle)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            tvshowtitle = url
            url = self.base_link + '/show/%s/season/%s/episode/%s' % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            r = cfScraper.get(url).content
            match = re.compile('<a href="http://www.tvmovieflix.com/report-.+?/(.+?)" target="_blank"><span class="a">Report Broken</span></a></li>', re.DOTALL | re.M).findall(r)
            for link in match:
                if "/show/" in url:
                    surl = "http://www.tvmovieflix.com/e/" + link
                else:
                    surl = "http://www.tvmovieflix.com/m/" + link
                i = cfScraper.get(surl).content
                match = re.compile('<IFRAME.+?SRC="(.+?)"', re.DOTALL | re.IGNORECASE).findall(i)
                for link in match:
                    if "realtalksociety.com" in link:
                        r = requests.get(link).content
                        match = re.compile('<source src="(.+?)" type="video/mp4">', re.DOTALL | re.IGNORECASE).findall(r)
                        for url in match:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            quality, info = source_utils.get_release_quality(url, url)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': True, 'debridonly': False})
                    else:
                        valid, host = source_utils.is_host_valid(link, hostDict)
                        quality, info = source_utils.get_release_quality(link, link)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url



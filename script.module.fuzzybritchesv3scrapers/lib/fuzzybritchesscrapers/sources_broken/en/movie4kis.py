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
import traceback
import urlparse

from promisescrapers.modules import cleantitle, log_utils, source_utils
from promisescrapers import cfScraper


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movie4k.is', 'movie4k.ws']
        self.base_link = 'https://www5.movie4k.to'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))

            r = cfScraper.get(url).content
            info = re.findall('<div class="boxinfo".+?href="(.+?)".+?<h2>(.+?)</h2>.+?class="year">(.+?)</span>', r, re.DOTALL)
            for link, name, r_year in info:
                if cleantitle.get(title) in cleantitle.get(name):
                    if year in str(r_year):
                        return link
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Movie4kis - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            r = cfScraper.get(url).content
            qual = re.compile('<span class="calidad2">(.+?)</span>').findall(r)
            for qcheck in qual:
                quality, info = source_utils.get_release_quality(qcheck, qcheck)

            links = re.compile('<iframe src="(.+?)"', re.DOTALL).findall(r)

            for link in links:

                valid, host = source_utils.is_host_valid(link, hostDict)
                if not valid:
                    continue
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Movie4kis - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url

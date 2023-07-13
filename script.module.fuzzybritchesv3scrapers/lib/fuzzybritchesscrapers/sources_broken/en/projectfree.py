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

from six import ensure_text

from fuzzybritchesscrapers import cfScraper
from fuzzybritchesscrapers import parse_qs, urljoin, urlencode, quote_plus
from fuzzybritchesscrapers.modules import cleantitle, client, source_utils, log_utils

from fuzzybritchesscrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['project-free-tv.ag', 'my-project-free.tv']
        self.base_link = custom_base or 'https://projecfreetv.co'
        self.search_link = '/episode/%s/'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s-s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('+', '-')

            r = cfScraper.get(url, timeout=10).content
            r = ensure_text(r, errors='ignore')
            #log_utils.log('projectfree - r: ' + r)
            try:
                data = re.compile('<a href="(.+?)" target="_blank" rel="nofollow" title=').findall(r)
                #log_utils.log('projectfree - data: ' + repr(data))
                for url in data:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except:
                log_utils.log('projectfree2 - Exception', 1)
                pass
            return sources
        except:
            log_utils.log('projectfree3 - Exception', 1)
            return sources


    def resolve(self, url):
        return url


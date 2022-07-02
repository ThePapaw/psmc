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

from fuzzybritchesscrapers import parse_qs, urljoin, urlencode
from fuzzybritchesscrapers.modules import cleantitle
from fuzzybritchesscrapers.modules import client
from fuzzybritchesscrapers.modules import source_utils, log_utils

from fuzzybritchesscrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['filmxy.me', 'filmxy.one', 'filmxy.tv']
        self.base_link = custom_base or 'https://www.filmxy.pw'
        self.search_link = '/search/%s/feed/rss2/'
        self.post = 'https://cdn.filmxy.one/asset/json/posts.json'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('filmxy', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None: return

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            title = data['title']
            year = data['year']

            tit = cleantitle.geturl(title + ' ' + year)
            query = urljoin(self.base_link, tit)

            r = client.request(query, referer=self.base_link)
            if not data['imdb'] in r:
                return sources

            links = []

            try:
                down = client.parseDOM(r, 'div', attrs={'id': 'tab-download'})[0]
                down = client.parseDOM(down, 'a', ret='href')[0]
                data = client.request(down, headers={'User-Agent': client.agent(), 'Referer': query})
                frames = client.parseDOM(data, 'li', attrs={'class': 'signle-link'})
                frames = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'span')[0]) for i in frames if i]
                for i in frames:
                    links.append(i)
            except:
                pass

            try:
                streams = client.parseDOM(r, 'div', attrs={'id': 'tab-stream'})[0]
                streams = re.findall(r'''iframe src=(.+?) frameborder''', streams.replace('&quot;', ''), re.I | re.DOTALL)
                streams = [(i, '720p') for i in streams]
                for i in streams:
                    links.append(i)
            except:
                pass

            for url, qual in links:
                try:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality = source_utils.check_sd_url(qual)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                        'direct': False, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            log_utils.log('filmxy exc', 1)
            return sources

    def resolve(self, url):
        return url
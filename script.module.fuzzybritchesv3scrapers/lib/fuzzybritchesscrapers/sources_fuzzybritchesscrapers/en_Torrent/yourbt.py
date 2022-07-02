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

from fuzzybritchesscrapers import parse_qs, urljoin, urlencode, quote_plus, unquote_plus
from fuzzybritchesscrapers.modules import cleantitle
from fuzzybritchesscrapers.modules import client
from fuzzybritchesscrapers.modules import debrid
from fuzzybritchesscrapers.modules import source_utils
from fuzzybritchesscrapers.modules import workers
from fuzzybritchesscrapers.modules import log_utils

from fuzzybritchesscrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yourbittorrent.com', 'yourbittorrent2.com']
        self.base_link = custom_base or 'https://yourbittorrent.com'
        self.search_link = '?q=%s'#&page=1&sort=seeders&o=desc'
        self.aliases = []


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('YourBT0 - Exception', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('YourBT1 - Exception', 1)
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
            log_utils.log('YourBT2 - Exception', 1)
            return


    def sources(self, url, hostDict, hostprDict):
        self.sources = []
        try:
            if url is None:
                return self.sources

            if debrid.status() is False:
                return self.sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.title = cleantitle.get_query(self.title)
            self.year = data['year']
            self.hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else self.year

            query = ' '.join((self.title, self.hdlr))
            query = re.sub('[^A-Za-z0-9\s\.-]+', '', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('+', '-')

            try:
                r = client.request(url)
                links = re.findall('<a href="(/torrent/.+?)"', r, re.DOTALL)[:20]

                threads = []
                for link in links:
                    threads.append(workers.Thread(self.get_sources, link))
                [i.start() for i in threads]
                [i.join() for i in threads]
                return self.sources
            except:
                log_utils.log('YourBT3 - Exception', 1)
                return self.sources

        except:
            log_utils.log('YourBT3 - Exception', 1)
            return self.sources


    def get_sources(self, link):
        try:
            url = urljoin(self.base_link, link)
            result = client.request(url)

            info_hash = re.findall('<kbd>(.+?)<', result, re.DOTALL)[0]
            url = 'magnet:?xt=urn:btih:' + info_hash

            name = re.findall('<h3 class="card-title">(.+?)<', result, re.DOTALL)[0]
            name = client.replaceHTMLCodes(name).replace('Original Name: ', '')
            name = cleantitle.get_title(name)
            if not source_utils.is_match(name, self.title, self.hdlr, self.aliases):
                return

            quality, info = source_utils.get_release_quality(name, url)

            try:
                size = re.findall('<div class="col-3">File size:</div><div class="col">(.+?)<', result, re.DOTALL)[0]
                size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', size)[0]
                dsize, isize = source_utils._size(size)
            except:
                dsize, isize = 0.0, ''
            info.insert(0, isize)
            info = ' | '.join(info)

            self.sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})

        except:
            log_utils.log('YourBT4 - Exception', 1)
            pass

    def resolve(self, url):
        return url

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

from fuzzybritchesscrapers import cfScraper
from fuzzybritchesscrapers import parse_qs, urlencode, quote_plus
from fuzzybritchesscrapers.modules import cleantitle, client, debrid, source_utils, log_utils, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.tvsearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Promise&token={0}&mode=search&search_string={1}&format=json_extended'
        self.msearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Promise&token={0}&mode=search&search_imdb={1}&format=json_extended'
        self.token = 'https://torrentapi.org/pubapi_v2.php?app_id=Promise&get_token=get_token'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except BaseException:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None: return sources
            if debrid.status() is False: return sources
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)
            imdb = data['imdb']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = ' '.join((title, hdlr))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            token = cfScraper.get(self.token, timeout=10).json()
            token = token['token']
            if 'tvshowtitle' in data:
                search_link = self.tvsearch.format(token, quote_plus(query))
            else:
                search_link = self.msearch.format(token, imdb)
            #log_utils.log('torapi url: ' + search_link)
            control.sleep(250)
            rjson = cfScraper.get(search_link, timeout=10).json()
            files = rjson['torrent_results']
            for file in files:
                try:
                    if not file['episode_info']['imdb'] == imdb:
                        continue

                    name = cleantitle.get_title(file['title'])

                    url = file['download']
                    url = url.split('&tr')[0]
                    quality, info = source_utils.get_release_quality(name, url)
                    try:
                        dsize = float(file['size']) / 1073741824
                        isize = '%.2f GB' % round(dsize, 2)
                    except:
                        dsize, isize = 0.0, ''
                    info.insert(0, isize)
                    info = ' | '.join(info)
                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                except:
                    pass
            return sources
        except:
            log_utils.log('torapi - Exception', 1)
            return sources

    def resolve(self, url):
        return url

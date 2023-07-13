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

import requests
import simplejson as json

from fuzzybritchesscrapers import parse_qs, urljoin, urlencode, quote_plus
from fuzzybritchesscrapers.modules import cleantitle
from fuzzybritchesscrapers.modules import client
from fuzzybritchesscrapers.modules import source_utils, log_utils
#from fuzzybritchesscrapers import cfScraper

from fuzzybritchesscrapers import custom_base_link
custom_base = custom_base_link(__name__)

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gowatchseries.io','gowatchseries.co']
        self.base_link = 'https://www5.gowatchseries.bz'
        self.search_link = '/ajax-search.html?keyword=%s&id=-1'
        self.search_link2 = '/search.html?keyword=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {
                'imdb': imdb,
                'tvdb': tvdb,
                'tvshowtitle': tvshowtitle,
                'year': year}
            url = urlencode(url)
            return url
        except BaseException:
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
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            if 'season' in data:
                season = data['season']
            if 'episode' in data:
                episode = data['episode']
            year = data['year']

            r = client.request(self.base_link, output='extended', timeout='10')
            try:
                cookie = r[4]
                headers = r[3]
            except:
                cookie = r[3]
                headers = r[2]
            result = r[0]
            headers['Cookie'] = cookie

            query = urljoin(self.base_link, self.search_link %quote_plus(cleantitle.getsearch(title)))
            query2 = urljoin(self.base_link, self.search_link % quote_plus(title).lower())
            r = client.request(query, headers=headers, XHR=True)
            if len(r) < 20:
                r = client.request(query2, headers=headers, XHR=True)
            r = json.loads(r)['content']
            r = zip( client.parseDOM( r, 'a', ret='href'), client.parseDOM(r, 'a'))

            if 'tvshowtitle' in data:
                cltitle = cleantitle.get(title + 'season' + season)
                cltitle2 = cleantitle.get(title + 'season%02d' % int(season))
                r = [ i for i in r if cltitle == cleantitle.get(i[1]) or cltitle2 == cleantitle.get(i[1])]
                vurl = '%s%s-episode-%s' % (self.base_link, str(r[0][0]).replace('/info', ''), episode)
                vurl2 = None

            else:
                cltitle = cleantitle.getsearch(title)
                cltitle2 = cleantitle.getsearch('%s (%s)' % (title, year))
                r = [i for i in r if cltitle2 == cleantitle.getsearch(i[1]) or cltitle == cleantitle.getsearch(i[1])]
                vurl = '%s%s-episode-0' % (self.base_link, str(r[0][0]).replace('/info', ''))
                vurl2 = '%s%s-episode-1' % (self.base_link, str(r[0][0]).replace('/info', ''))

            r = client.request(vurl, headers=headers)
            headers['Referer'] = vurl

            slinks = client.parseDOM(r, 'div', attrs={'class': 'anime_muti_link'})
            slinks = client.parseDOM(slinks, 'li', ret='data-video')
            if len(slinks) == 0 and vurl2 is not None:
                r = client.request(vurl2, headers=headers)
                headers['Referer'] = vurl2
                slinks = client.parseDOM(r, 'div', attrs={'class': 'anime_muti_link'})
                slinks = client.parseDOM(slinks, 'li', ret='data-video')
            slinks = [slink if slink.startswith('http') else 'https:{0}'.format(slink) for slink in slinks]

            _slinks = []
            for url in slinks:
                try:
                    # if 'vidcloud.icu' in url:
                        # urls = []
                        # urls = source_utils.getVidcloudLink(url)
                        # if urls:
                            # for uri in urls:
                                # _slinks.append((uri[0], uri[1]))
                    # elif 'xstreamcdn.com' in url:
                        # url, quality = source_utils.getXstreamcdnLink(url)
                        # if url:
                            # _slinks.append((url, quality))
                    # else:
                    _slinks.append((url, 'HD'))
                except BaseException:
                    pass

            for url in _slinks:
                quality = url[1]
                url = url[0]
                url = client.replaceHTMLCodes(url)
                #url = url.encode('utf-8')
                valid, host = source_utils.is_host_valid(url, hostDict)
                direct = False if valid else True
                host = client.replaceHTMLCodes(host)
                #host = host.encode('utf-8')
                sources.append({'source': host,
                                'quality': quality,
                                'language': 'en',
                                'url': url,
                                'direct': direct,
                                'debridonly': False})
            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url

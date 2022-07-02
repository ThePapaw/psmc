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

import re, base64

import simplejson as json

from six import ensure_text, ensure_binary

from fuzzybritchesscrapers import urljoin
from fuzzybritchesscrapers.modules import cache
from fuzzybritchesscrapers.modules import control
from fuzzybritchesscrapers.modules import client
from fuzzybritchesscrapers.modules import source_utils
from fuzzybritchesscrapers.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ororo.tv']
        self.base_link = 'https://ororo.tv'
        self.moviesearch_link = '/api/v2/movies'
        self.tvsearch_link = '/api/v2/shows'
        self.movie_link = '/api/v2/movies/%s'
        self.show_link = '/api/v2/shows/%s'
        self.episode_link = '/api/v2/episodes/%s'

        self.user = control.setting('ororo.user')
        self.password = control.setting('ororo.pass')
        self.headers = {
            'Authorization': 'Basic %s' % ensure_text(base64.b64encode(ensure_binary('%s:%s' % (self.user, self.password)))),
            'User-Agent': 'Covenant for Kodi'
        }


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = cache.get(self.ororo_moviecache, 60, self.user)
            url = [i[0] for i in url if imdb == i[1]][0]
            url = self.movie_link % url

            return url
        except:
            log_utils.log('Ororo', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            url = cache.get(self.ororo_tvcache, 120, self.user)
            url = [i[0] for i in url if imdb == i[1]][0]
            url = self.show_link % url

            return url
        except:
            log_utils.log('Ororo', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if (self.user == '' or self.password == ''): raise Exception()

            if url == None: return

            url = urljoin(self.base_link, url)

            r = client.request(url, headers=self.headers)
            r = ensure_text(r, errors='replace')
            r = json.loads(r)['episodes']
            r = [(str(i['id']), str(i['season']), str(i['number']), str(i['airdate'])) for i in r]

            url = [i for i in r if season == '%01d' % int(i[1]) and episode == '%01d' % int(i[2])]
            url += [i for i in r if premiered == i[3]]

            url = self.episode_link % url[0][0]

            return url
        except:
            log_utils.log('Ororo', 1)
            return


    def ororo_moviecache(self, user):
        try:
            url = urljoin(self.base_link, self.moviesearch_link)

            r = client.request(url, headers=self.headers)
            r = ensure_text(r, errors='replace')
            r = json.loads(r)['movies']
            r = [(str(i['id']), str(i['imdb_id'])) for i in r]
            r = [(i[0], 'tt' + re.sub('[^0-9]', '', i[1])) for i in r]
            return r
        except:
            log_utils.log('Ororo', 1)
            return


    def ororo_tvcache(self, user):
        try:
            url = urljoin(self.base_link, self.tvsearch_link)

            r = client.request(url, headers=self.headers)
            r = ensure_text(r, errors='replace')
            r = json.loads(r)['shows']
            r = [(str(i['id']), str(i['imdb_id'])) for i in r]
            r = [(i[0], 'tt' + re.sub('[^0-9]', '', i[1])) for i in r]
            return r
        except:
            log_utils.log('Ororo', 1)
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return sources

            if (self.user == '' or self.password == ''): raise Exception()

            url = urljoin(self.base_link, url)
            url = client.request(url, headers=self.headers)
            #log_utils.log('Ororo resp: ' + repr(url))
            url = ensure_text(url, errors='replace')
            url = json.loads(url)['url']
            quality, _ = source_utils.get_release_quality(url)

            sources.append({'source': 'direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

            return sources
        except:
            log_utils.log('Ororo', 1)
            return sources


    def resolve(self, url):
        return url



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

from promisescrapers import parse_qs, urljoin, urlencode
from promisescrapers.modules import cleantitle, client, source_utils, log_utils

from promisescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwaatch.com']
        self.base_link = custom_base or 'https://iwaatch.com'
        self.search_link = '/?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('iWAATCH - Exception', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:

            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']
            year = data['year']

            search_id = title.lower()
            url = urljoin(self.base_link, self.search_link % (search_id.replace(' ', '+')))
            headers = {
                'User-Agent': client.agent(),
                'Accept': '*/*',
                'Accept-Encoding': 'identity;q=1, *;q=0',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'DNT': '1'
            }

            response = requests.Session()
            r = response.get(url, headers=headers, timeout=5).text
            r = client.parseDOM(r, 'div', attrs={'class': 'container'})[1]
            items = client.parseDOM(r, 'div', attrs={'class': r'col-xs-12 col-sm-6 col-md-3 '})
            for item in items:
                movie_url = client.parseDOM(item, 'a', ret='href')[0]
                movie_title = re.compile('div class="post-title">(.+?)<', re.DOTALL).findall(item)[0]
                if cleantitle.get(title).lower() == cleantitle.get(movie_title).lower():

                    r = response.get(movie_url, headers=headers, timeout=5).text
                    year_data = re.findall('<h2 style="margin-bottom: 0">(.+?)</h2>', r, re.IGNORECASE)[0]
                    if year == year_data:
                        links = re.findall(r"<a href='(.+?)'>(\d+)p<\/a>", r)

                        for link, quality in links:

                            if not link.startswith('https:'):
                                link = 'https:' + link.replace('http:', '')
                            link = link + '|Referer=https://iwaatch.com/movie/' + title

                            quality, info = source_utils.get_release_quality(quality, link)

                            sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': link, 'direct': True, 'debridonly': False})
            return sources
        except:
            log_utils.log('iWAATCH - Exception', 1)
            return sources

    def resolve(self, url):
        #log_utils.log('iWAATCH - url: ' + url)
        return url

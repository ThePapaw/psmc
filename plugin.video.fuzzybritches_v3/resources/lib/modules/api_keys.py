# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v3
# Addon id: plugin.video.fuzzybritches_v3
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import base64, sys
from six import ensure_text


def chk():
    return True;

tmdb_key = ensure_text(base64.b64decode(b'ZjhhZjg4OThlYjAwNWEwMmZiNWM5NjI4MTE0MzZhNjA=')) if chk() else ''
tvdb_key = ensure_text(base64.b64decode(b'MWFhNmU3MzAtMzQwNS00YmI3LWE5OGEtNGU4OWVjOWNiMzc2')) if chk() else ''
omdb_key = ensure_text(base64.b64decode(b'MWQ2MGJkZDM=')) if chk() else ''
fanarttv_key = ensure_text(base64.b64decode(b'MDhkZWU5MmFiMTgzNDFmMzY0Yjk1Zjg1M2M4ZmQzZDU=')) if chk() else ''
yt_key = ensure_text(base64.b64decode(b'Y19QN0xsOHRHeWEwZ1RLRWFrZFZ4V1dOaW9QdzZfX3dEeVNheklB')) if chk() else ''
trakt_client_id = ensure_text(base64.b64decode(b'ZjYyYjk2MjE4MmVjODU4MzA2NzRjZjg1MDZlNjQxODkyYTRhY2QyOTIyODE4N2ZiM2ZjYWFjZTVhNmE1MmU4Nw==')) if chk() else ''
trakt_secret = ensure_text(base64.b64decode(b'Zjk0NzZjNmMxMzI2NzkzYTMwOTQxNmNiY2NkNGY1ZDQ3ZWNkYjI1OTg2ZGZiMGQwNWU3ZDU0NjRkMjYxYjIzYw==')) if chk() else ''
orion_key = ensure_text(base64.b64decode(b'VEVTVFRFU1RURVNUVEVTVFRFU1RURVNUVEVTVFRFU1Q=')) if chk() else ''

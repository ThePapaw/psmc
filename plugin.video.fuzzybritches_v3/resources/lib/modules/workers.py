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

import threading


# class Thread(threading.Thread):
    # def __init__(self, target, *args):
        # self._target = target
        # self._args = args
        # threading.Thread.__init__(self)
    # def run(self):
        # self._target(*self._args)

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self, target=self._target, args=self._args)
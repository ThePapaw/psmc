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

import pkgutil
import os

__all__ = [x[1] for x in os.walk(os.path.dirname(__file__))][0]

def sources():
    try:
        sourceDict = []
        for i in __all__:
            for loader, module_name, is_pkg in pkgutil.walk_packages([os.path.join(os.path.dirname(__file__), i)]):
                if is_pkg:
                    continue

                try:
                    module = loader.find_module(module_name).load_module(module_name)
                    sourceDict.append((module_name, module.source()))
                except:
                    # from resources.lib.modules import log_utils
                    # log_utils.log('Could not load "%s"' % module_name, 1)
                    pass
        return sourceDict
    except:
        return []



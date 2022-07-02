# -*- coding: UTF-8 -*-

import os
from resources.lib.modules import control, log_utils

def get():
    try:
        changelogfile = os.path.join(control.addonPath, 'changelog.txt')
        head = '[COLOR crimson]•• [/COLOR]Fuzzy Britches v3 Changelog[COLOR crimson] ••[/COLOR]'
        control.textViewer(file=changelogfile, heading=head)
    except:
        control.infoDialog('Error opening changelog', sound=True)
        log_utils.log('changeloglog_view_fail', 1)


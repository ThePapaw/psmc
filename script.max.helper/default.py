#!/usr/bin/python

import xbmcgui
from resources.lib.utils import *
from resources.lib.helper import *

class Main:

    def __init__(self):
        self._parse_argv()
        if self.action:
            self.getactions()
        else:
            xbmcgui.Dialog().ok('Error', 'This is a tool to provide features to a skin and requires skin integration.')

    def _parse_argv(self):
        args = sys.argv
        self.action = []
        for arg in args:
            if arg == 'script.max.helper':
                continue
            if arg.startswith('action='):
                self.action.append(arg[7:])
            else:
                try:
                    self.params[arg.split("=")[0].lower()] = "=".join(arg.split("=")[1:]).strip()
                except:
                    self.params = {}
                    pass

    def getactions(self):
        action_inventory = {'ismylist': ismylist,
                            'togglemylist': togglemylist,
                            'ratetitle': ratetitle,
                            'gettvshowid': gettvshowid,
                            'playtrailer': playtrailer}
        for action in self.action:
            action_inventory[action](self.params)

if __name__ == "__main__":
    Main()

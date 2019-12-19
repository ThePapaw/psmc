# -*- coding: UTF-8 -*-
# Names and Digits from Aeon Nox Silvo, Alt names commented behind.

from resources.lib.modules import control


def getViewType():
    my_options = ['Default', 'Info Wall', 'Landscape', 'ShowCase', 'ShowCase2',
                    'Wide List', 'Shift', 'Icons', 'Banner', 'Fanart',  'Wall', '[ [B] Close [/B] ]']
    mychoice = control.SelectDialog(control.AddonTitle, my_options, key=False)
    if mychoice == 'Default': viewType2 = '50'
    elif mychoice == 'Info Wall': viewType2 = '51' # Poster
    elif mychoice == 'Landscape': viewType2 = '52' # Icon Wall
    elif mychoice == 'ShowCase': viewType2 = '53' # Shift
    elif mychoice == 'ShowCase2': viewType2 = '54' # Info Wall
    elif mychoice == 'Wide List': viewType2 = '55'
    elif mychoice == 'Shift': viewType2 = '57'
    elif mychoice == 'Icons': viewType2 = '500' # Wall
    elif mychoice == 'Banner': viewType2 = '501'
    elif mychoice == 'Fanart': viewType2 = '502'
    elif mychoice == 'Wall': viewType2 = '503'
    elif mychoice == '[ [B] Close [/B] ]': return
    control.setSetting('viewType', mychoice)
    control.setSetting('viewType2', str (viewType2))
    control.execute("Container.SetViewMode(%s)" % ( int(viewType2) ) )
    return



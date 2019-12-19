# -*- coding: UTF-8 -*-

from resources.lib.modules import control
from resources.lib.api import colorChoice


AddonID = control.AddonID
AddonTitle = control.AddonTitle
SelectDialog = control.SelectDialog
Execute = control.execute
Notify = control.Notify

CustomColor = control.setting('my_ColorChoice')
if CustomColor == '': CustomColor = 'none'


def mySpareMenu():
    my_options = ['[B]Option1[/B]', '[B]Option2[/B]', '[B]Option3[/B]', '[B]Option4[/B]', '[B]Option5[/B]', '[ [B]Close[/B] ]']
    selectList = []
    for Item in my_options:
        selectList.append(colorChoice.colorString(Item, CustomColor))
    mychoice = SelectDialog(AddonTitle, selectList, key=False)
    mychoice = mychoice.replace('[COLOR %s]' % (CustomColor),'').replace('[/COLOR]','')
    if mychoice == '[B]Option1[/B]': Notify(AddonTitle, 'Testing Option1...')
    elif mychoice == '[B]Option2[/B]': Notify(AddonTitle, 'Testing Option2...')
    elif mychoice == '[B]Option3[/B]': Notify(AddonTitle, 'Testing Option3...')
    elif mychoice == '[B]Option4[/B]': Notify(AddonTitle, 'Testing Option4...')
    elif mychoice == '[B]Option5[/B]':
        Notify(AddonTitle, 'Testing Option5...')
    elif mychoice == '[ [B]Close[/B] ]' :
        return



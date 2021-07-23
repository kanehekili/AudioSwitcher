# -*- coding: utf-8 -*-
'''
Created on Dec 21, 2019

@author: matze
'''
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from PulseTools import PulseAudioControl
import locale

VERSION="@xxxx@"

lang = locale.getdefaultlocale()
TEXT_MAP = {}
if "de" in lang[0]:
    TEXT_MAP["SWITCH_REMOTE"]="Soll der Ton auf dem externen Gerät spielen?"
    TEXT_MAP["SWITCH_LOCAL"]="Soll der Ton auf dem eigenen Rechner spielen?"
    TEXT_MAP["SWITCH_NONE"]="Kein externes Audiogerät gefunden"      
else:
    TEXT_MAP["SWITCH_REMOTE"]="Play audio on external device?"
    TEXT_MAP["SWITCH_LOCAL"]="Play audio on this device?"
    TEXT_MAP["SWITCH_NONE"]="No external device found"      

def _t(s):
    if not s in TEXT_MAP:
        print('TEXT_MAP["%s"]="missing"'%(s))
        return s
    return TEXT_MAP[s]
          
def run():
    title = "Audio Switcher"
    app = QApplication(sys.argv)
    tools = PulseAudioControl()
    isLocal= tools.isLocalProfile()
    external = tools.getPrimaryExternalProfile()
    if external:
        if isLocal:
            question=_t("SWITCH_REMOTE")
            target=external
        else:
            question=_t("SWITCH_LOCAL")
            target=tools.getPrimaryLocalProfile()
        buttonReply = QMessageBox.question(None,title,question,);
        if buttonReply == QMessageBox.Yes:
            tools.switchProfile(target)
    else:
        QMessageBox.information(None,title,_t("SWITCH_NONE"))
                                

if __name__ == '__main__':
    run()
    sys.exit(1)
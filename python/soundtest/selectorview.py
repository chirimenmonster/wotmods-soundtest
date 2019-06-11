# -*- coding: utf-8 -*-

import logging
from functools import partial

import BigWorld
import ResMgr
import GUI
import WWISE
import nations
import SoundGroups
from gui.Scaleform.framework import ViewSettings, ViewTypes, ScopeTemplates
from gui.Scaleform.framework.entities.View import View

from gui.IngameSoundNotifications import IngameSoundNotifications
from gui.game_control.epic_meta_game_ctrl import _FrontLineSounds

from modsettings import MOD_NAME

#for name in [ 'gui.Scalform.framework.entities.View', 'gui.Scaleform.Flash' ]:
#    logging.getLogger(name).setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class SelectorView(View):
    __CFG_SECTION_PATH = 'gui/sound_notifications.xml'

    def __init__(self):
        super(SelectorView, self).__init__()
        self.__soundModes = sorted(SoundGroups.g_instance.soundModes.modes.keys())
        self.__genderSwicth = [
            { 'label': 'male', 'data': SoundGroups.CREW_GENDER_SWITCHES.MALE },
            { 'label': 'female', 'data': SoundGroups.CREW_GENDER_SWITCHES.FEMALE }
        ]
        self.__nations = list(nations.NAMES)
        self.__readConfig()

    def __onLogGui(self, logType, msg, *kargs):
        _logger.debug('%s.GUI: %r, %r', str(logType), msg, kargs)

    def __onLogGuiFormat(self, logType, msg, *kargs):
        _logger.debug('%s.GUI: %s', str(logType), msg % kargs)
        print '%s.GUI2: %s', str(logType), msg % kargs

    def afterCreate(self):
        print 'afterCreate'
        self.addExternalCallback('debug.LOG_GUI', self.__onLogGui)
        self.addExternalCallback('debug.LOG_GUI_FORMAT', self.__onLogGuiFormat)

    def _populate(self):
        BigWorld.logInfo(MOD_NAME, '_populate', None)
        super(SelectorView, self)._populate()

    def __readConfig(self):
        sec = ResMgr.openSection(self.__CFG_SECTION_PATH)
        events = []
        #print sec.keys()
        for eventSec in sec.values():
            #print eventSec.keys()
            for category in ('voice', ):
                soundSec = eventSec[category]
                if soundSec is not None:
                    #print soundSec.readString('wwsound')
                    events.append(soundSec.readString('wwsound'))
        self.__events = events
        #print events
        return

    def getDropdownMenuData(self):
        settings = {
            'soundModes':       self.__soundModes,
            'genderSwitch':     self.__genderSwicth,
            'nations':          self.__nations,
            'events':           self.__events
        }
        self.flashObject.as_setConfig(settings)
    
    def playSoundEvent(self, data):
        soundMode = data.soundMode
        genderSwitch = data.genderSwitch.data
        nation  = data.nation
        soundEvent = data.soundEvent
        print 'playSoundEvent: [genderSwitch={}, nation={}, soundMode={}, soundEvent={}]'.format(genderSwitch, nation, soundMode, soundEvent)
        isFrontline = soundEvent.startswith('vo_eb_')
        _FrontLineSounds.onChange(isFrontline)
        g_instance = SoundGroups.g_instance
        savedCurrentMode = g_instance.soundModes.currentMode
        savedCurrentNationalPreset = g_instance.soundModes.currentNationalPreset
        print 'playSoundEvent: [currentMode={}, currentNationalPreset={}]'.format(savedCurrentMode, savedCurrentNationalPreset)
        g_instance.soundModes.setCurrentNation(nation, genderSwitch)
        g_instance.soundModes.setMode(soundMode)
        g_instance.playSound2D(soundEvent)
        #g_instance.soundModes.setNationalMappingByPreset(savedCurrentNationalPreset)
        #g_instance.soundModes.setMode(savedCurrentMode)
        #_FrontLineSounds.onChange(False)

    def onTryClosing(self):
        print 'onTryClosing'
        return True

    def onWindowClose(self):
        print 'onWindowClose'
        self.destroy()

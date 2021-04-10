# -*- coding: utf-8 -*-

import logging

import ResMgr
import nations
import SoundGroups
from gui.Scaleform.framework.entities.View import View

from gui.game_control.epic_meta_game_ctrl import _FrontLineSounds

from modsettings import MOD_NAME

_logger = logging.getLogger(MOD_NAME)
_logger.setLevel(logging.DEBUG)


class SelectorView(View):
    __CFG_SECTION_PATH = 'gui/sound_notifications.xml'

    def __init__(self):
        super(SelectorView, self).__init__()
        self.__soundModes = sorted(SoundGroups.g_instance.soundModes.modes.keys())
        self.__genderSwitch = [
            { 'label': 'male', 'data': SoundGroups.CREW_GENDER_SWITCHES.MALE },
            { 'label': 'female', 'data': SoundGroups.CREW_GENDER_SWITCHES.FEMALE }
        ]
        self.__nations = list(nations.NAMES)
        self.__readConfig()
        self.onCreate += self.beforeCreate

    def __readConfig(self):
        sec = ResMgr.openSection(self.__CFG_SECTION_PATH)
        events = []
        for eventSec in sec.values():
            for category in ('voice', ):
                soundSec = eventSec[category]
                if soundSec is not None:
                    events.append(soundSec.readString('wwsound'))
        self.__events = events
        return

    def beforeCreate(self, pyEntity):
        settings = {
            'soundModes':       self.__soundModes,
            'genderSwitch':     self.__genderSwitch,
            'nations':          self.__nations,
            'events':           self.__events
        }
        self.flashObject.as_setConfig(settings)
    
    def playSoundEvent(self, data):
        soundMode = data.soundMode
        genderSwitch = data.genderSwitch.data
        nation  = data.nation
        soundEvent = data.soundEvent
        _logger.info('playSoundEvent: soundMode=%s, genderSwitch=%s, nation=%s, soundEvent=%s',
                soundMode, genderSwitch, nation, soundEvent)
        isFrontline = soundEvent.startswith('vo_eb_')
        _FrontLineSounds.onChange(isFrontline)
        g_instance = SoundGroups.g_instance
        savedCurrentMode = g_instance.soundModes.currentMode
        savedCurrentNationalPreset = g_instance.soundModes.currentNationalPreset
        _logger.info('playSoundEvent: currentMode=%s, currentNationalPreset=%s',
                savedCurrentMode, savedCurrentNationalPreset)
        g_instance.soundModes.setCurrentNation(nation, genderSwitch)
        g_instance.soundModes.setMode(soundMode)
        g_instance.playSound2D(soundEvent)
        #g_instance.soundModes.setNationalMappingByPreset(savedCurrentNationalPreset)
        #g_instance.soundModes.setMode(savedCurrentMode)
        #_FrontLineSounds.onChange(False)

    def onTryClosing(self):
        _logger.debug('onTryClosing')
        return True

    def onWindowClose(self):
        _logger.debug('onWindowClose')
        self.destroy()

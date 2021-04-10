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

    def __onLogGui(self, logType, msg, *kargs):
        _logger.debug('%s.GUI: %r, %r', str(logType), msg, kargs)

    def __onLogGuiFormat(self, logType, msg, *kargs):
        _logger.debug('%s.GUI: %s', str(logType), msg % kargs)

    def afterCreate(self):
        self.addExternalCallback('debug.LOG_GUI', self.__onLogGui)
        self.addExternalCallback('debug.LOG_GUI_FORMAT', self.__onLogGuiFormat)

    def _populate(self):
        _logger.debug('SelectorView._populate')
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
        _logger.info('playSoundEvent: genderSwitch=%s, nation=%s, soundMode=%s, soundEvent=%s',
                genderSwitch, nation, soundMode, soundEvent)
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

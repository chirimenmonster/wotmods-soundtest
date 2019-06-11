
import json
import re
import struct
import weakref

import BigWorld
import GUI
import ResMgr
import game
import Keys
from debug_utils import LOG_CURRENT_EXCEPTION
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from gui.shared import g_eventBus, events
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.framework import g_entitiesFactories
from gui.Scaleform.framework.entities.View import View, ViewKey
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.IngameSoundNotifications import IngameSoundNotifications

from soundtest.modsettings import MOD_NAME, SELECTOR_VIEW_ALIAS
from soundtest.viewsettings import SELECTOR_VIEW_SETTINGS


g_soundInfo = None

def overrideMethod(cls, method):
    def decorator(handler):
        orig = getattr(cls, method)
        newm = lambda *args, **kwargs: handler(orig, *args, **kwargs)
        if type(orig) is not property:
            setattr(cls, method, newm)
        else:
            setattr(cls, method, property(newm))
    return decorator


@overrideMethod(game, 'handleKeyEvent')
def _handleKeyEvent(orig, event):
    ret = orig(event)
    try:
        if event.isKeyDown() and not event.isRepeatedEvent():
            if event.key == Keys.KEY_F12:
                print '### press F12'
                g_selector.start()
    except:
        LOG_CURRENT_EXCEPTION()
    return ret


def _getSoundText(eventName):
    sec = g_soundInfo.get(eventName, None)
    soundPath = text = None
    if sec:
        soundPath = sec['soundPath']
        description = sec['description']
        if sec['text'] and sec['text'] is not None:
            text = sec['text'][0]
    return soundPath, text

def cvt(d):
    return struct.pack('B', d) if d < 256 else unichr(d)


def init():
    g_entitiesFactories.addSettings(SELECTOR_VIEW_SETTINGS)
    g_eventBus.addListener(events.AppLifeCycleEvent.INITIALIZED, g_control.onAppInitialized)

class Control(object):
    def onAppInitialized(self, event):
        if event.ns != APP_NAME_SPACE.SF_BATTLE:
            return
        BigWorld.logInfo(MOD_NAME, 'AppLifeCycleEvent.INITIALIZED', None)
        battleEntry = g_appLoader.getDefBattleApp()
        if not battleEntry:
            return
        battleEntry.loadView(SFViewLoadParams(VIEW_ALIAS))
        pyEntity = battleEntry.containerManager.getViewByKey(ViewKey(VIEW_ALIAS))
        self.__pyEntity = weakref.proxy(pyEntity)
        BigWorld.logInfo(MOD_NAME, 'pyEntity: {}'.format(pyEntity), None)

    def sendMessage(self, message):
        if self.__pyEntity:
            self.__pyEntity.as_setMessageS(message)


class Selector(object):
    def start(self):
        appLoader = dependency.instance(IAppLoader)
        app = appLoader.getDefLobbyApp()
        if not app:
            return
        app.loadView(SFViewLoadParams(SELECTOR_VIEW_ALIAS))
        pyEntity = app.containerManager.getViewByKey(ViewKey(SELECTOR_VIEW_ALIAS))
        self.__pyEntity = weakref.proxy(pyEntity)
        BigWorld.logInfo(MOD_NAME, 'pyEntity: {}'.format(pyEntity), None)


g_control = Control()
g_selector = Selector()

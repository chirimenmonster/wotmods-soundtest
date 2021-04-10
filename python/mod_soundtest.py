
import weakref
import logging

import game
import Keys
from debug_utils import LOG_CURRENT_EXCEPTION
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from gui.Scaleform.framework import g_entitiesFactories
from gui.Scaleform.framework.entities.View import ViewKey
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams

from soundtest.modsettings import MOD_NAME, SELECTOR_VIEW_ALIAS
from soundtest.viewsettings import SELECTOR_VIEW_SETTINGS

_logger = logging.getLogger(MOD_NAME)
_logger.setLevel(logging.DEBUG)


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
                _logger.debug('press F12')
                g_selector.start()
    except:
        LOG_CURRENT_EXCEPTION()
    return ret


def init():
    g_entitiesFactories.addSettings(SELECTOR_VIEW_SETTINGS)


class Selector(object):
    def start(self):
        appLoader = dependency.instance(IAppLoader)
        app = appLoader.getDefLobbyApp()
        if not app:
            return
        app.loadView(SFViewLoadParams(SELECTOR_VIEW_ALIAS))
        pyEntity = app.containerManager.getViewByKey(ViewKey(SELECTOR_VIEW_ALIAS))
        self.__pyEntity = weakref.proxy(pyEntity)
        _logger.debug('Selector.start: pyEntity: %s', pyEntity)


g_selector = Selector()

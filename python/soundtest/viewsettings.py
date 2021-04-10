# -*- coding: utf-8 -*-

from frameworks.wulf import WindowLayer
from gui.Scaleform.framework import ViewSettings, ScopeTemplates

from selectorview import SelectorView
from modsettings import SELECTOR_VIEW_ALIAS, SELECTOR_SWF_FILE_PATH

SELECTOR_VIEW_SETTINGS = ViewSettings(
    SELECTOR_VIEW_ALIAS,
    SelectorView,
    SELECTOR_SWF_FILE_PATH,
    WindowLayer.WINDOW,
    None,
    ScopeTemplates.DEFAULT_SCOPE
)

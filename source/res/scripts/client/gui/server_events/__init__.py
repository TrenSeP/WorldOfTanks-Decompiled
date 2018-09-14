# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/server_events/__init__.py
from gui.server_events.EventsCache import EventsCache
from skeletons.gui.server_events import IEventsCache
__all__ = ('getServerEventsConfig',)

def getServerEventsConfig(manager):
    """ Configures services for package server_events.
    :param manager: helpers.dependency.DependencyManager
    """
    cache = EventsCache()
    cache.init()
    manager.bindInstance(IEventsCache, cache, finalizer='fini')
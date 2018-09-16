# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/marathon/marathon_constants.py
from shared_utils import CONST_CONTAINER
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
MARATHON_VEHICLE_PREFIX = 'It13_Progetto_M35_mod_46'
MARATHON_VEHICLE_ID = 51361
MARATHON_PREFIX = 'event_marathon:'
MARATHON_SUSPEND = ':suspend'
MARATHON_COMPLETED_TOKEN_POSTFIX = '_PASS'
MARATHON_AWARD_TOKENS = ('event_marathon:IM18_COMPLETE', 'event_marathon:IM18_S10_PASS')
MARATHON_QUESTS_IN_CHAIN = 10
ZERO_TIME = 0.0
MIN_VEHICLE_LVL = 8

class MARATHON_STATE(CONST_CONTAINER):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    FINISHED = 3
    SUSPENDED = 4
    DISABLED = 5
    UNKNOWN = 6
    ENABLED_STATE = (NOT_STARTED, IN_PROGRESS, FINISHED)
    DISABLED_STATE = (SUSPENDED, DISABLED, UNKNOWN)


class MARATHON_WARNING(CONST_CONTAINER):
    WRONG_VEH_TYPE = 'veh_type'
    WRONG_BATTLE_TYPE = 'battle_type'
    NONE = ''


MAP_FLAG_HEADER_ICON = {MARATHON_STATE.ENABLED_STATE: RES_ICONS.MAPS_ICONS_LIBRARY_MARATHON_CUP_ICON,
 MARATHON_STATE.DISABLED_STATE: RES_ICONS.MAPS_ICONS_LIBRARY_MARATHON_CUP_DISABLE_ICON}

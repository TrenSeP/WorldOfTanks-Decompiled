# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/dialogs/rent_confirm_dialog.py
import logging
from constants import RentType
from gui.Scaleform.daapi.view.dialogs import I18nConfirmDialogMeta, DIALOG_BUTTON_ID
from gui.Scaleform.framework import ScopeTemplates
from gui.Scaleform.locale.ARENAS import ARENAS
from gui.Scaleform.locale.VEHICLE_PREVIEW import VEHICLE_PREVIEW
from gui.shared.formatters import formatPrice, text_styles
from gui.shared.money import MONEY_UNDEFINED
from helpers import dependency
from helpers.i18n import makeString as _ms
from helpers.time_utils import getTimeStructInLocal
from skeletons.gui.game_control import IEpicBattleMetaGameController
from skeletons.gui.shared import IItemsCache
_logger = logging.getLogger(__name__)

class RentConfirmDialogMeta(I18nConfirmDialogMeta):
    epicController = dependency.descriptor(IEpicBattleMetaGameController)
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self, intCD, rentType, nums=(0,), price=MONEY_UNDEFINED, seasonType=0, renew=False):
        key = 'rentConfirmationRenew' if renew else 'rentConfirmation'
        super(RentConfirmDialogMeta, self).__init__(key, scope=ScopeTemplates.LOBBY_SUB_SCOPE, focusedID=DIALOG_BUTTON_ID.SUBMIT)
        vehicle = self.itemsCache.items.getItemByCD(intCD)
        if rentType == RentType.SEASON_CYCLE_RENT:
            if len(nums) > 1:
                key = 'cycles'
                indexes = [ self.epicController.getCycleOrdinalNumber(n) for n in nums ]
                indexes = '{}-{}'.format(min(indexes), max(indexes))
            else:
                key = 'cycle'
                indexes = str(self.epicController.getCycleOrdinalNumber(nums[0]))
        elif RentType.SEASON_RENT:
            key = 'season'
            _, endTimestamp = self.epicController.getSeasonTimeRange()
            indexes = str(getTimeStructInLocal(endTimestamp).tm_year)
        else:
            key = ''
            indexes = str(None)
            _logger.debug('GameSeasonType %s with RentType %s is not supported', seasonType, rentType)
        stage = _ms(VEHICLE_PREVIEW.getOfferName(key), value=indexes)
        event = _ms(ARENAS.TYPE_EPIC_NAME_INQUOTES)
        self._messageCtx = {'name': vehicle.shortUserName or 'Vehicle',
         'stage': text_styles.stats(stage or 'Stage'),
         'event': text_styles.stats(event or 'Event'),
         'price': formatPrice(price, reverse=True, useIcon=True)}
        return

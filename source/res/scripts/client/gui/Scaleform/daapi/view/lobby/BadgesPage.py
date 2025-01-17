# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/BadgesPage.py
import operator
from collections import defaultdict
import BigWorld
from gui.shared.gui_items.badge import Badge
from gui.shared.tutorial_helper import getTutorialGlobalStorage
from helpers import dependency, i18n
from account_helpers.AccountSettings import AccountSettings, LAST_BADGES_VISIT
from helpers.time_utils import getServerUTCTime
from skeletons.account_helpers.settings_core import ISettingsCore
from skeletons.gui.game_control import IBadgesController
from skeletons.gui.lobby_context import ILobbyContext
from skeletons.gui.shared import IItemsCache
from gui.Scaleform.daapi.view.meta.BadgesPageMeta import BadgesPageMeta
from gui.shared.event_dispatcher import showHangar
from gui.shared.formatters import text_styles
from gui.Scaleform.locale.BADGE import BADGE
from tutorial.control.context import GLOBAL_FLAG
_SUFFIX_BADGE_HINT_ID = 'BadgePageNewSuffixBadgeHint'

def _makeBadgeVO(badge):
    return {'id': badge.badgeID,
     'icon': badge.getBigIcon(),
     'title': text_styles.stats(badge.getUserName()),
     'description': text_styles.main(badge.getUserDescription()),
     'enabled': badge.isAchieved,
     'selected': badge.isSelected,
     'highlightIcon': badge.getHighlightIcon(),
     'isFirstLook': badge.isNew()}


class BadgesPage(BadgesPageMeta):
    itemsCache = dependency.descriptor(IItemsCache)
    lobbyContext = dependency.instance(ILobbyContext)
    settingsCore = dependency.descriptor(ISettingsCore)
    badgesController = dependency.descriptor(IBadgesController)

    def __init__(self, *args, **kwargs):
        super(BadgesPage, self).__init__(*args, **kwargs)
        self.__prefixBadgeID = None
        self.__receivedSuffixBadgeID = None
        self.__suffixBadgeSelected = False
        self.__tutorStorage = getTutorialGlobalStorage()
        if self.__tutorStorage is not None:
            hasNewBadges = self.__checkNewSuffixBadges()
            if hasNewBadges:
                self.__tutorStorage.setValue(GLOBAL_FLAG.BADGE_PAGE_HAS_NEW_SUFFIX_BADGE, True)
        return

    def onCloseView(self):
        AccountSettings.setSettings(LAST_BADGES_VISIT, getServerUTCTime())
        showHangar()

    def onSelectBadge(self, badgeID):
        self.__prefixBadgeID = badgeID
        self.__selectBadges()
        self.as_setSelectedBadgeImgS(Badge.getBigIconById(badgeID))

    def onDeselectBadge(self):
        self.__prefixBadgeID = None
        self.__selectBadges()
        self.as_setSelectedBadgeImgS('')
        return

    def onSelectSuffixBadge(self):
        self.__suffixBadgeSelected = True
        self.__selectBadges()

    def onDeselectSuffixBadge(self):
        self.__suffixBadgeSelected = False
        self.__selectBadges()

    def _populate(self):
        super(BadgesPage, self)._populate()
        userName = BigWorld.player().name
        self.as_setStaticDataS({'header': {'closeBtnLabel': BADGE.BADGESPAGE_HEADER_CLOSEBTN_LABEL,
                    'descrTf': text_styles.main(BADGE.BADGESPAGE_HEADER_DESCR),
                    'playerText': text_styles.grandTitle(self.lobbyContext.getPlayerFullName(userName))}})
        self.__updateBadges()
        self.badgesController.onUpdated += self.__updateBadges

    def _dispose(self):
        if self.__tutorStorage is not None:
            self.__tutorStorage.setValue(GLOBAL_FLAG.BADGE_PAGE_HAS_NEW_SUFFIX_BADGE, False)
        self.badgesController.onUpdated -= self.__updateBadges
        super(BadgesPage, self)._dispose()
        return

    def __updateBadges(self):
        receivedBadgesData = []
        notReceivedBadgesData = []
        prefixSelected, prefixBadges, lastSuffixBadge = self.__preprocessBadges()
        if prefixSelected is not None:
            self.__prefixBadgeID = prefixSelected.badgeID
            self.as_setSelectedBadgeImgS(prefixSelected.getBigIcon())
        self.__suffixBadgeSelected = False
        self.__receivedSuffixBadgeID = None
        sbImgPath = ''
        sbDescrText = ''
        if lastSuffixBadge is not None:
            self.__receivedSuffixBadgeID = lastSuffixBadge.badgeID
            sbImgPath = lastSuffixBadge.getSuffixSmallIcon()
            sbDescrText = i18n.makeString('#badge:suffix/badge_{}'.format(lastSuffixBadge.badgeID))
            if lastSuffixBadge.isSelected:
                self.__suffixBadgeSelected = True
        self.as_setSuffixBadgeImgS(sbImgPath, sbDescrText, self.__suffixBadgeSelected)
        for badge in prefixBadges:
            badgeVO = _makeBadgeVO(badge)
            if badge.isAchieved:
                receivedBadgesData.append(badgeVO)
            notReceivedBadgesData.append(badgeVO)

        self.as_setReceivedBadgesS({'badgesData': receivedBadgesData})
        self.as_setNotReceivedBadgesS({'title': text_styles.highTitle(BADGE.BADGESPAGE_BODY_UNCOLLECTED_TITLE),
         'badgesData': notReceivedBadgesData})
        return

    def __selectBadges(self):
        badges = []
        if self.__prefixBadgeID:
            badges.append(self.__prefixBadgeID)
        if self.__receivedSuffixBadgeID and self.__suffixBadgeSelected:
            badges.append(self.__receivedSuffixBadgeID)
        self.badgesController.select(badges)

    def __preprocessBadges(self):
        prefixSelected = self.badgesController.getPrefix()
        suffixBadge = self.badgesController.getSuffix()
        prefixBadges = []
        cache = defaultdict(list)
        for badge in self.itemsCache.items.getBadges().itervalues():
            if not badge.isPrefixLayout():
                continue
            badge.isSelected = False
            if prefixSelected is not None and badge.badgeID == prefixSelected.badgeID:
                badge.isSelected = True
            if badge.isObsolete() and not badge.isAchieved:
                continue
            if badge.isCollapsible():
                cache[badge.group].append(badge)
                continue
            prefixBadges.append(badge)

        for badges in cache.itervalues():
            byClass = sorted(badges, key=operator.methodcaller('getBadgeClass'), reverse=True)
            for badge in byClass:
                prefixBadges.append(badge)
                if badge.isAchieved:
                    break

        return (prefixSelected, sorted(prefixBadges), suffixBadge)

    def __checkNewSuffixBadges(self):
        suffix = self.badgesController.getSuffix()
        return suffix is not None and suffix.isNew()

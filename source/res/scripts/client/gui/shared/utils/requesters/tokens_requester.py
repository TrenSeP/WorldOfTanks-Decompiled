# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/shared/utils/requesters/tokens_requester.py
import logging
import BigWorld
from adisp import async, process
from constants import LOOTBOX_TOKEN_PREFIX
from helpers import dependency
from gui.shared.utils.requesters.abstract import AbstractSyncDataRequester
from skeletons.gui.shared.utils.requesters import ITokensRequester
from skeletons.gui.shared.gui_items import IGuiItemsFactory
from skeletons.gui.lobby_context import ILobbyContext
_logger = logging.getLogger(__name__)

class TokensRequester(AbstractSyncDataRequester, ITokensRequester):
    itemsFactory = dependency.descriptor(IGuiItemsFactory)
    lobbyContext = dependency.descriptor(ILobbyContext)

    def __init__(self):
        self.__lastShopRev = None
        self.__lootBoxCache = {}
        self.__lootBoxTotalCount = 0
        super(TokensRequester, self).__init__()
        return

    def clear(self):
        self.__lootBoxCache.clear()
        self.__lootBoxTotalCount = 0
        super(TokensRequester, self).clear()

    def getTokens(self):
        return self.getCacheValue('tokens', {})

    def getLootBoxes(self):
        return self.__lootBoxCache.copy()

    def getFreeLootBoxes(self):
        result = {}
        for boxTokenID, box in self.__lootBoxCache.iteritems():
            if box.isFree():
                result[boxTokenID] = box

        return result

    def getLootBoxesTotalCount(self):
        return self.__lootBoxTotalCount

    def getLootBoxesCountByType(self):
        boxes = self.__lootBoxCache.values()
        result = {}
        for box in boxes:
            boxType = box.getType()
            boxCount = box.getInventoryCount()
            boxCategory = box.getCategory()
            boxResult = result.setdefault(boxType, {'total': 0,
             'categories': {}})
            boxResult['total'] += boxCount
            categories = boxResult['categories']
            categories[boxCategory] = categories.get(boxCategory, 0) + boxCount

        return result

    def updateAllLootBoxes(self, data):
        lootBoxTokensList = self.__createLootBoxes(data)
        self.__clearLootBoxes(lootBoxTokensList, isRemove=True)
        self.__updateLootBoxes(self.getTokens())

    def getLootBoxByTokenID(self, tokenID):
        return self.__lootBoxCache.get(tokenID)

    @async
    @process
    def _requestCache(self, callback):
        result = yield self.__requestTokensCache()
        if 'tokens' in result:
            if not self.__lootBoxCache:
                self.__createLootBoxes(self.lobbyContext.getServerSettings().getLootBoxConfig())
            self.__updateLootBoxes(result['tokens'])
        callback(result)

    @async
    def __requestTokensCache(self, callback):
        BigWorld.player().tokens.getCache(lambda resID, value: self._response(resID, value, callback))

    def __createLootBoxes(self, data):
        lootBoxTokensList = []
        for lootBoxID, lootBoxData in data.iteritems():
            lootBoxTokenID = LOOTBOX_TOKEN_PREFIX + str(lootBoxID)
            lootBoxTokensList.append(lootBoxTokenID)
            if lootBoxTokenID not in self.__lootBoxCache:
                item = self.itemsFactory.createLootBox(lootBoxID, lootBoxData['type'], lootBoxData['category'], 0)
                self.__lootBoxCache[lootBoxTokenID] = item
            self.__lootBoxCache[lootBoxTokenID].update(lootBoxData['type'], lootBoxData['category'])

        return lootBoxTokensList

    def __updateLootBoxes(self, tokensCache):
        for lootBoxTokenID, data in tokensCache.items():
            _, count = data
            if lootBoxTokenID in self.__lootBoxCache:
                item = self.__lootBoxCache[lootBoxTokenID]
                self.__lootBoxTotalCount += count - item.getInventoryCount()
                item.updateCount(count)

        self.__clearLootBoxes(tokensCache)

    def __clearLootBoxes(self, data, isRemove=False):
        lootBoxIDs = self.__lootBoxCache.keys()
        for lootBoxID in lootBoxIDs:
            if lootBoxID not in data:
                item = self.__lootBoxCache[lootBoxID]
                self.__lootBoxTotalCount -= item.getInventoryCount()
                if not isRemove:
                    item.updateCount(invCount=0)
                else:
                    del self.__lootBoxCache[lootBoxID]

# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/shared/gui_items/loot_box.py
import typing
from gui.Scaleform.locale.LOOTBOXES import LOOTBOXES
from gui.shared.gui_items.gui_item import GUIItem
from helpers import i18n
from shared_utils import CONST_CONTAINER

class NewYearLootBoxes(CONST_CONTAINER):
    PREMIUM = 'newYear_premium'
    COMMON = 'newYear_usual'


class NewYearCategories(CONST_CONTAINER):
    NEWYEAR = 'NewYear'
    CHRISTMAS = 'Christmas'
    ORIENTAL = 'Oriental'
    FAIRYTALE = 'Fairytale'


GUI_ORDER = (NewYearLootBoxes.COMMON, NewYearLootBoxes.PREMIUM)
CATEGORIES_GUI_ORDER = (NewYearCategories.NEWYEAR,
 NewYearCategories.CHRISTMAS,
 NewYearCategories.ORIENTAL,
 NewYearCategories.FAIRYTALE)

class LootBox(GUIItem):
    __slots__ = ('__id', '__invCount', '__type', '__category')

    def __init__(self, lootBoxID, lootBoxType, lootBoxCategory, invCount):
        super(LootBox, self).__init__()
        self.__id = lootBoxID
        self.__invCount = invCount
        self.__type = lootBoxType
        self.__category = lootBoxCategory

    def __repr__(self):
        return 'LootBox(id=%d, type=%s, category=%s, count=%d)' % (self.getID(),
         self.getType(),
         self.getCategory(),
         self.getInventoryCount())

    def __cmp__(self, other):
        return cmp(self.getID(), other.getID())

    def updateCount(self, invCount):
        self.__invCount = invCount

    def update(self, lootBoxType, lootBoxCategory):
        self.__type = lootBoxType
        self.__category = lootBoxCategory

    def getInventoryCount(self):
        return self.__invCount

    def getID(self):
        return self.__id

    def getUserName(self):
        return i18n.makeString(LOOTBOXES.getLootboxName(self.__type))

    def getType(self):
        return self.__type

    def getCategory(self):
        return self.__category

    def isFree(self):
        return self.__type == NewYearLootBoxes.COMMON

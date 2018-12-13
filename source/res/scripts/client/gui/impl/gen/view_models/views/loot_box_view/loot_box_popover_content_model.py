# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/views/loot_box_view/loot_box_popover_content_model.py
import typing
from frameworks.wulf import Array
from frameworks.wulf import ViewModel

class LootBoxPopoverContentModel(ViewModel):
    __slots__ = ('onEventBtnClick',)

    def getCountSlot(self):
        return self._getNumber(0)

    def setCountSlot(self, value):
        self._setNumber(0, value)

    def getEntryList(self):
        return self._getArray(1)

    def setEntryList(self, value):
        self._setArray(1, value)

    def _initialize(self):
        super(LootBoxPopoverContentModel, self)._initialize()
        self._addNumberProperty('countSlot', 0)
        self._addArrayProperty('entryList', Array())
        self.onEventBtnClick = self._addCommand('onEventBtnClick')
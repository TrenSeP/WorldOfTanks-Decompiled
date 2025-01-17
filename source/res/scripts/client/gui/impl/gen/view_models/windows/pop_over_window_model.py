# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/windows/pop_over_window_model.py
from frameworks.wulf import ViewModel
from frameworks.wulf import View

class PopOverWindowModel(ViewModel):
    __slots__ = ('onCloseBtnClicked',)

    def getContent(self):
        return self._getView(0)

    def setContent(self, value):
        self._setView(0, value)

    def getBoundX(self):
        return self._getNumber(1)

    def setBoundX(self, value):
        self._setNumber(1, value)

    def getBoundY(self):
        return self._getNumber(2)

    def setBoundY(self, value):
        self._setNumber(2, value)

    def getBoundWidth(self):
        return self._getNumber(3)

    def setBoundWidth(self, value):
        self._setNumber(3, value)

    def getBoundHeight(self):
        return self._getNumber(4)

    def setBoundHeight(self, value):
        self._setNumber(4, value)

    def getDirectionType(self):
        return self._getNumber(5)

    def setDirectionType(self, value):
        self._setNumber(5, value)

    def getIsCloseBtnVisible(self):
        return self._getBool(6)

    def setIsCloseBtnVisible(self, value):
        self._setBool(6, value)

    def _initialize(self):
        super(PopOverWindowModel, self)._initialize()
        self._addViewProperty('content')
        self._addNumberProperty('boundX', 0)
        self._addNumberProperty('boundY', 0)
        self._addNumberProperty('boundWidth', 0)
        self._addNumberProperty('boundHeight', 0)
        self._addNumberProperty('directionType', 0)
        self._addBoolProperty('isCloseBtnVisible', True)
        self.onCloseBtnClicked = self._addCommand('onCloseBtnClicked')

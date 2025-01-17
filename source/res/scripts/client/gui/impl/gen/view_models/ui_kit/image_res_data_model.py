# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/ui_kit/image_res_data_model.py
from gui.impl.gen import R
from frameworks.wulf import ViewModel

class ImageResDataModel(ViewModel):
    __slots__ = ()

    def getImgSource(self):
        return self._getResource(0)

    def setImgSource(self, value):
        self._setResource(0, value)

    def _initialize(self):
        super(ImageResDataModel, self)._initialize()
        self._addResourceProperty('imgSource', R.invalid())

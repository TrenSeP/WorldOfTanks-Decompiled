# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/server_events/conditions.py
import operator
import weakref
from abc import ABCMeta, abstractmethod
import account_helpers
import constants
from debug_utils import LOG_WARNING
from gui import GUI_NATIONS_ORDER_INDICES
from gui.server_events import formatters
from gui.shared.utils.requesters import REQ_CRITERIA
from gui.shared.utils.requesters.ItemsRequester import RESEARCH_CRITERIA
from helpers import i18n, dependency
from items import vehicles
from shared_utils import CONST_CONTAINER
from skeletons.gui.game_control import IIGRController
from skeletons.gui.server_events import IEventsCache
from skeletons.gui.shared import IItemsCache
from gui.Scaleform.locale.QUESTS import QUESTS
_AVAILABLE_BONUS_TYPES_LABELS = {constants.ARENA_BONUS_TYPE.CYBERSPORT: 'team7x7'}
_RELATIONS = formatters.RELATIONS
_RELATIONS_SCHEME = formatters.RELATIONS_SCHEME
_ET = constants.EVENT_TYPE
_TOKEN_REQUIREMENT_QUESTS = set(_ET.LIKE_BATTLE_QUESTS + _ET.LIKE_TOKEN_QUESTS)

def _getArenaBonusType(preBattleCond):
    if preBattleCond is not None:
        squadNode = preBattleCond.getConditions().find('isSquad')
        if squadNode is not None and squadNode.getValue():
            return 'squad'
        bonusTypeNode = preBattleCond.getConditions().find('bonusTypes')
        if bonusTypeNode is not None:
            bonusTypes = list(bonusTypeNode.getValue())
            if len(bonusTypes) == 1 and bonusTypes[0] in _AVAILABLE_BONUS_TYPES_LABELS:
                return _AVAILABLE_BONUS_TYPES_LABELS[bonusTypes[0]]
    return 'formation'


class GROUP_TYPE(CONST_CONTAINER):
    OR = 'or'
    AND = 'and'


_SORT_ORDER = ('igrType', 'premiumAccount', 'inClan', 'GR', 'accountDossier', 'vehiclesUnlocked', 'vehiclesOwned', 'token', 'hasReceivedMultipliedXP', 'vehicleDossier', 'vehicleDescr', 'bonusTypes', 'isSquad', 'mapCamouflageKind', 'geometryNames', 'win', 'isAlive', 'achievements', 'results', 'unitResults', 'vehicleKills', 'vehicleDamage', 'vehicleStun', 'clanKills', 'cumulative', 'vehicleKillsCumulative', 'vehicleDamageCumulative', 'vehicleStunCumulative')
_SORT_ORDER_INDICES = dict(((name, idx) for idx, name in enumerate(_SORT_ORDER)))

def _handleRelation(relation, source, toCompare):
    if relation == _RELATIONS.EQ:
        return source == toCompare
    if relation == _RELATIONS.GT:
        return source > toCompare
    if relation == _RELATIONS.GTQ:
        return source >= toCompare
    if relation == _RELATIONS.LS:
        return source < toCompare
    if relation == _RELATIONS.LSQ:
        return source <= toCompare
    LOG_WARNING('Unknown kind of values relation', relation, source, toCompare)
    return False


def _findRelation(condDataKeys):
    res = set(_RELATIONS.ALL()) & set(condDataKeys)
    return res.pop() if len(res) else None


def _getNodeValue(node, key, default=None):
    if key in node:
        dNode = dict(node[key])
        if 'value' in dNode:
            return dNode['value']
    return default


def _prepareVehData(vehsList, predicate=None):
    predicate = predicate or (lambda *args: True)
    return map(lambda v: (v, (not v.isInInventory or predicate(v), None, None)), vehsList)


class _Negatable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def negate(self):
        pass


class _Updatable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, other, groupType):
        pass


class _AvailabilityCheckable(object):
    __metaclass__ = ABCMeta

    def isAvailable(self, *args, **kwargs):
        return self._isAvailable(*args, **kwargs)

    def _isAvailable(self, *args, **kwargs):
        return True


class _Condition(object):

    def __init__(self, name, data, uniqueName):
        super(_Condition, self).__init__()
        self._name = name
        self._data = data
        self._uniqueName = uniqueName

    def getName(self):
        return self._name

    def getData(self):
        return self._data

    def getUniqueName(self):
        return self._uniqueName

    def clearItemsCache(self):
        pass

    def getValue(self):
        raise NotImplementedError


class _ConditionsGroup(_AvailabilityCheckable, _Negatable):

    def __init__(self, groupType, isNegative=False):
        super(_ConditionsGroup, self).__init__()
        self.items = []
        self.type = groupType
        self.isNegative = isNegative

    def getName(self):
        return self.type

    def isAvailable(self, *args, **kwargs):
        res = self._isAvailable(*args, **kwargs)
        if self.isNegative:
            res = not res
        return res

    def add(self, condition):
        if isinstance(condition, list) or isinstance(condition, tuple):
            for cond in condition:
                self._addNewCondition(cond)

        else:
            self._addNewCondition(condition)

    def remove(self, condition):
        self.items.remove(condition)

    def find(self, condName):
        for cond in self.items:
            if cond.getName() == condName:
                return cond

        return None

    def findAll(self, condName):
        result = []
        for cond in self.items:
            if cond.getName() == condName:
                result.append(cond)

        return result

    def negate(self):
        self.isNegative = not self.isNegative

    def isEmpty(self):
        return not len(self.items)

    def getSortedItems(self):
        return sorted(self.items, cmp=self._sortItems, key=operator.methodcaller('getName'))

    @classmethod
    def _sortItems(cls, a, b):
        if a not in _SORT_ORDER:
            return 1
        return -1 if b not in _SORT_ORDER else _SORT_ORDER_INDICES[a] - _SORT_ORDER_INDICES[b]

    def _addNewCondition(self, cond):
        if isinstance(cond, _Updatable):
            otherCond = self.find(cond.getName())
            if otherCond is None:
                self.items = [ c for c in self.items if not cond.update(c, self.type) ]
            elif otherCond.update(cond, self.type):
                cond = None
        if cond is not None:
            self.items.append(cond)
        return

    def __repr__(self):
        return '%s<count=%d>' % (self.__class__.__name__, len(self.items))


class _Requirement(_Condition, _AvailabilityCheckable, _Negatable):
    itemsCache = dependency.descriptor(IItemsCache)

    def __repr__(self):
        return '%s<>' % self.__class__.__name__


class _VehicleRequirement(_Requirement):

    def _isAvailable(self, vehicle):
        """ Checks given vehicle availability
        """
        return True


class _VehsListParser(object):
    """ Mix-in for vehicles list parsing functionality
    """
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.__vehsCache = None
        return

    def isAnyVehicleAcceptable(self):
        return self._isAnyVehicleAcceptable(self._data)

    def _clearItemsCache(self):
        self.__vehsCache = None
        return

    def _postProcessCriteria(self, defaultCriteria, criteria):
        return defaultCriteria | criteria

    def _isAnyVehicleAcceptable(self, data):
        """ Checks for all vehicles acceptance
        """
        return not len(set(data.keys()) & {'types',
         'nations',
         'levels',
         'classes'})

    def getFilterCriteria(self, data):
        types, nations, levels, classes = self._parseFilters(data)
        defaultCriteria = self._getDefaultCriteria()
        if types:
            criteria = REQ_CRITERIA.VEHICLE.SPECIFIC_BY_CD(types)
        else:
            criteria = REQ_CRITERIA.EMPTY
            if nations:
                criteria |= REQ_CRITERIA.NATIONS(nations)
            if levels:
                criteria |= REQ_CRITERIA.VEHICLE.LEVELS(levels)
            if classes:
                criteria |= REQ_CRITERIA.VEHICLE.CLASSES(classes)
        return self._postProcessCriteria(defaultCriteria, criteria)

    def _getDefaultCriteria(self):
        return REQ_CRITERIA.DISCLOSABLE

    def _getVehiclesCache(self, data):
        if self.__vehsCache is None:
            self.__vehsCache = self.itemsCache.items.getVehicles(self.getFilterCriteria(data))
        return self.__vehsCache

    def _getVehiclesList(self, data):
        return self._getVehiclesCache(data).values()

    def _parseFilters(self, data):
        types, nations, levels, classes = (None, None, None, None)
        if 'types' in data:
            types = _getNodeValue(data, 'types')
        if 'nations' in data:
            nations = _getNodeValue(data, 'nations')
            nations = sorted(nations, key=GUI_NATIONS_ORDER_INDICES.get)
        if 'levels' in data:
            levels = _getNodeValue(data, 'levels')
        if 'classes' in data:
            acceptedClasses = _getNodeValue(data, 'classes')
            classes = [ name for name, index in constants.VEHICLE_CLASS_INDICES.items() if index in acceptedClasses ]
        return (types,
         nations,
         levels,
         classes)


class _VehsListCondition(_Condition, _VehsListParser):

    def __init__(self, name, data, path):
        super(_VehsListCondition, self).__init__(name, dict(data), path)
        self._relation = _findRelation(self._data.keys())
        self._relationValue = _getNodeValue(self._data, self._relation)
        self._isNegative = False

    @property
    def relationValue(self):
        return self._relationValue

    @property
    def relation(self):
        return self._relation

    @property
    def data(self):
        return self._data

    def isNegative(self):
        return self._isNegative

    def getVehiclesList(self):
        return self._getVehiclesList(self._data)

    def negate(self):
        if self._relation is not None:
            self._relation = _RELATIONS.getOppositeRelation(self._relation)
        else:
            self._isNegative = not self._isNegative
        return

    def clearItemsCache(self):
        self._clearItemsCache()

    def getVehiclesData(self):
        return []

    def parseFilters(self):
        return self._parseFilters(self._data)


class _VehsListRequirement(_VehsListCondition, _AvailabilityCheckable, _Negatable):

    def __init__(self, name, data, path):
        super(_VehsListRequirement, self).__init__(name, data, path)
        if self._relation is None:
            self._relation = _RELATIONS.GTQ
            self._relationValue = 1
        return

    def _isAvailable(self):
        vehsList = self._getVehiclesList(self._data)
        return _handleRelation(self._relation, len(filter(self._checkVehicle, vehsList)), self._relationValue) if self._relation is not None else True

    def _checkVehicle(self, vehicle):
        return True

    def __repr__(self):
        return '%s<%s=%r>' % (self.__class__.__name__, self._relation, self._relationValue)


class AndGroup(_ConditionsGroup):

    def __init__(self, isNegative=False):
        super(AndGroup, self).__init__(GROUP_TYPE.AND, isNegative)

    def _isAvailable(self, *args, **kwargs):
        res = True
        for cond in self.items:
            res = cond.isAvailable(*args, **kwargs)
            if not res:
                return res

        return res


class OrGroup(_ConditionsGroup):

    def __init__(self, isNegative=False):
        super(OrGroup, self).__init__(GROUP_TYPE.OR, isNegative)

    def _isAvailable(self, *args, **kwargs):
        for cond in self.items:
            if cond.isAvailable(*args, **kwargs):
                return True

        return False


class IGR(_Requirement, _Updatable):
    igrCtrl = dependency.descriptor(IIGRController)

    def __init__(self, path, data):
        super(IGR, self).__init__('igrType', dict(data), path)
        self._igrTypes = {self._data.get('value')}

    def getIgrTypes(self):
        return self._igrTypes

    def negate(self):
        igrTypes = constants.IGR_TYPE
        self._igrTypes ^= {igrTypes.BASE, igrTypes.PREMIUM}

    def update(self, other, groupType):
        if groupType == GROUP_TYPE.OR:
            if other.getName() == 'igrType':
                self._igrTypes |= other._igrTypes
                return True
        return False

    def _isAvailable(self):
        return self.igrCtrl.getRoomType() in self._igrTypes


class GlobalRating(_Requirement):

    def __init__(self, path, data):
        super(GlobalRating, self).__init__('GR', dict(data), path)
        self._relation = _findRelation(self._data.keys())
        self._relationValue = float(_getNodeValue(self._data, self._relation))

    @property
    def relation(self):
        return self._relation

    @property
    def relationValue(self):
        return self._relationValue

    def negate(self):
        self._relation = _RELATIONS.getOppositeRelation(self._relation)

    def _isAvailable(self):
        return False if self._relationValue is None else _handleRelation(self._relation, self.itemsCache.items.stats.globalRating, self._relationValue)


class PremiumAccount(_Requirement):

    def __init__(self, path, data):
        super(PremiumAccount, self).__init__('premiumAccount', dict(data), path)
        self._needValue = self._data.get('value')

    def isPremiumNeeded(self):
        return self._needValue

    def negate(self):
        self._needValue = not self._needValue

    def _isAvailable(self):
        if self._needValue is not None:
            isPremium = account_helpers.isPremiumAccount(self.itemsCache.items.stats.attributes)
            return isPremium == self._needValue
        else:
            return True


class InClan(_Requirement):

    def __init__(self, path, data):
        super(InClan, self).__init__('inClan', dict(data), path)
        self._ids = self._data.get('value') or None
        self._isNegative = False
        return

    def getClanIds(self):
        return self._ids

    def isNegative(self):
        return self._isNegative

    def negate(self):
        self._isNegative = not self._isNegative

    def _isAvailable(self):
        clanDBID = self.itemsCache.items.stats.clanDBID
        if self._ids is not None:
            if not self._isNegative:
                return clanDBID in self._ids
            else:
                return clanDBID not in self._ids
        return bool(clanDBID) != self._isNegative


class Token(_Requirement):
    eventsCache = dependency.descriptor(IEventsCache)

    def __init__(self, path, data):
        super(Token, self).__init__('token', dict(data), path)
        self._id = _getNodeValue(self._data, 'id')
        self._consumable = 'consume' in self._data
        self._relation = _findRelation(self._data.keys())
        self._relationValue = int(_getNodeValue(self._data, self._relation, 0))
        self._complex = formatters.parseComplexToken(self._id)

    def isConsumable(self):
        return self._consumable

    def getConsumeCount(self):
        if self.isConsumable():
            consumeData, forceData = self._data['consume']
            return dict(consumeData).get('value', 0)

    def getID(self):
        return self._id

    def isDisplayable(self):
        """ Token should be visualized only if it has a special marker
        """
        return self._complex.isDisplayable

    def getUserName(self):
        userName = self.eventsCache.prefetcher.getTokenInfo(self._complex.styleID)
        return userName

    def isOnSale(self):
        """ Returns true if token is on sale on the prem shop.
        """
        return self.eventsCache.prefetcher.isTokenOnSale(self._complex.webID)

    def getImage(self, size):
        return self.eventsCache.prefetcher.getTokenImage(self._complex.styleID, size)

    def getStyleID(self):
        """ Get identifier of token's visual resources (i.e. images, title, description)
        """
        return self._complex.styleID

    def getWebID(self):
        """ Get token's identifier on external web resources.
        """
        return self._complex.webID

    def negate(self):
        self._relation = _RELATIONS.getOppositeRelation(self._relation)

    def getNeededCount(self):
        return self._relationValue + 1 if self._relation == _RELATIONS.GT else self._relationValue

    def getReceivedCount(self):
        return self.eventsCache.questsProgress.getTokenCount(self.getID())

    def _isAvailable(self):
        return _handleRelation(self._relation, self.eventsCache.questsProgress.getTokenCount(self._id), self._relationValue)


class TokenQuestToken(Token):
    """ Token condition inside account requirements of TokenQuest.
    
    We don't check availability in this case (see WOTD-81694).
    """

    def _isAvailable(self):
        return True


class VehiclesUnlocked(_VehsListRequirement):

    def __init__(self, path, data):
        super(VehiclesUnlocked, self).__init__('vehiclesUnlocked', dict(data), path)

    def _checkVehicle(self, vehicle):
        return vehicle.isUnlocked and not vehicle.isInitiallyUnlocked

    def _getDefaultCriteria(self):
        return RESEARCH_CRITERIA.VEHICLE_TO_UNLOCK


class VehiclesOwned(_VehsListRequirement):

    def __init__(self, path, data):
        super(VehiclesOwned, self).__init__('vehiclesOwned', dict(data), path)

    def _checkVehicle(self, vehicle):
        return vehicle.isInInventory


class PremiumVehicle(_VehicleRequirement):

    def __init__(self, path, data):
        super(PremiumVehicle, self).__init__('premiumVehicle', dict(data), path)
        self._needValue = self._data.get('value')

    def negate(self):
        self._needValue = not self._needValue

    def getFilterCriteria(self, data):
        criteria = REQ_CRITERIA.DISCLOSABLE
        if self._needValue:
            return criteria | REQ_CRITERIA.VEHICLE.PREMIUM
        else:
            return criteria | ~REQ_CRITERIA.VEHICLE.PREMIUM

    def _isAvailable(self, vehicle):
        return vehicle.isPremium == self._needValue

    def __repr__(self):
        return 'PremiumVehicle<value=%r>' % self._needValue


class XPMultipliedVehicle(_VehicleRequirement):

    def __init__(self, path, data):
        super(XPMultipliedVehicle, self).__init__('hasReceivedMultipliedXP', dict(data), path)
        self._needValue = self._data.get('value')

    def negate(self):
        self._needValue = not self._needValue

    def isAvailableReason(self, vehicle):
        isOk = self._isAvailable(vehicle)
        if self._needValue:
            reason = 'xpMultReceived'
        else:
            reason = 'xpMultReceived/not'
        return (isOk, reason)

    def getValue(self):
        return self._needValue

    def _isAvailable(self, vehicle):
        return (vehicle.dailyXPFactor == -1) == self._needValue

    def __repr__(self):
        return 'XPMultipliedVehicle<value=%r>' % self._needValue


class VehicleDescr(_VehicleRequirement, _VehsListParser, _Updatable):

    def __init__(self, path, data):
        super(VehicleDescr, self).__init__('vehicleDescr', dict(data), path)
        self._otherCriteria = REQ_CRITERIA.EMPTY
        self._isNegative = False

    def clearItemsCache(self):
        self._clearItemsCache()

    def negate(self):
        self._isNegative = not self._isNegative

    def update(self, other, groupType):
        if groupType != GROUP_TYPE.AND:
            return False
        if other.getName() in ('vehicleDescr', 'premiumVehicle'):
            self._otherCriteria |= other.getFilterCriteria(other._data)
            return True
        return False

    def getVehiclesList(self):
        return self._getVehiclesList(self._data)

    def _postProcessCriteria(self, defaultCriteria, criteria):
        if self._isNegative:
            criteria = ~criteria
        return defaultCriteria | criteria | self._otherCriteria

    def _isAvailable(self, vehicle):
        return vehicle.intCD in self._getVehiclesCache(self._data)


class _DossierValue(_Requirement):

    def __init__(self, name, data, path):
        super(_DossierValue, self).__init__(name, dict(data), path)
        self._recordName = _getNodeValue(self._data, 'record', '').split(':')
        self._average = 'average' in self._data
        self._relation = _findRelation(self._data.keys())
        self._relationValue = float(_getNodeValue(self._data, self._relation, 0.0))

    @property
    def relation(self):
        return self._relation

    @property
    def relationValue(self):
        return self._relationValue

    @property
    def average(self):
        return self._average

    @property
    def recordName(self):
        return self._recordName

    def negate(self):
        self._relation = _RELATIONS.getOppositeRelation(self._relation)

    def _checkDossier(self, dossier):
        block, record = self._recordName
        dossierDescr = dossier.getDossierDescr()
        dossierValue = dossierDescr[block][record]
        if self._average:
            battlesCount = dossierDescr[block]['battlesCount']
            dossierValue /= float(battlesCount or 1)
        return _handleRelation(self._relation, dossierValue, self._relationValue)


class AccountDossierValue(_DossierValue):

    def __init__(self, path, data):
        super(AccountDossierValue, self).__init__('accountDossier', dict(data), path)

    def _isAvailable(self):
        return self._checkDossier(self.itemsCache.items.getAccountDossier())


class BattleBonusType(_Condition, _Negatable):

    def __init__(self, path, data):
        super(BattleBonusType, self).__init__('bonusTypes', dict(data), path)
        self._types = self._data.get('value')

    def negate(self):
        newTypes = []
        for bt in constants.ARENA_BONUS_TYPE.RANGE:
            if bt not in self._types:
                newTypes.append(bt)

        self._types = newTypes

    def getValue(self):
        return self._types

    def __repr__(self):
        return 'BonusType<types=%r>' % self._types


class BattleSquad(_Condition, _Negatable):

    def __init__(self, path, data):
        super(BattleSquad, self).__init__('isSquad', dict(data), path)
        self._isSquad = self._data.get('value')

    def negate(self):
        self._isSquad = not self._isSquad

    def getValue(self):
        return self._isSquad

    def __repr__(self):
        return 'BattleSquad<isSquad=%r>' % self._isSquad


class BattleClanMembership(_Condition, _Negatable):

    class VALUES(CONST_CONTAINER):
        ANY = 'any'
        SAME = 'same'

    def __init__(self, path, data, preBattleCondProxy=None):
        super(BattleClanMembership, self).__init__('clanMembership', dict(data), path)
        self._value = self._data.get('value')
        self.__proxy = weakref.proxy(preBattleCondProxy)

    def negate(self):
        pass

    def getValue(self):
        return self._value

    def getArenaBonusType(self):
        return _getArenaBonusType(self.__proxy)

    def __repr__(self):
        return 'BattleClanMembership<relation=%r; bonusType=%s>' % (self._value, _getArenaBonusType(self.__proxy))


class BattleCamouflage(_Condition, _Negatable):

    def __init__(self, path, data):
        super(BattleCamouflage, self).__init__('camouflageKind', dict(data), path)
        self._camos = self._data.get('value')

    def getValue(self):
        return self._camos

    def negate(self):
        newCamos = []
        for camoTypeName, camoID in vehicles.CAMOUFLAGE_KINDS.iteritems():
            if camoID not in self._camos:
                newCamos.append(camoID)

        self._camos = newCamos

    def __repr__(self):
        return 'BattleCamouflage<camos=%r>' % self._camos


class BattleMap(_Condition, _Negatable):

    def __init__(self, path, data):
        super(BattleMap, self).__init__('geometryNames', dict(data), path)
        self._maps = self._data.get('value')
        self._isNegative = False

    def negate(self):
        self._isNegative = not self._isNegative

    def isNegative(self):
        return self._isNegative

    def getMaps(self):
        return self._maps

    def __repr__(self):
        return 'BattleMap<maps=%r>' % self._maps


class Win(_Condition, _Negatable):

    def __init__(self, path, data):
        super(Win, self).__init__('win', dict(data), path)
        self._isWin = self._data.get('value')

    def negate(self):
        self._isWin = not self._isWin

    def getValue(self):
        return self._isWin

    def __repr__(self):
        return 'Win<value=%r>' % self._isWin


class Survive(_Condition, _Negatable):

    def __init__(self, path, data):
        super(Survive, self).__init__('isAlive', dict(data), path)
        self._isAlive = self._data.get('value')

    def negate(self):
        self._isAlive = not self._isAlive

    def getValue(self):
        return self._isAlive

    def __repr__(self):
        return 'Survive<value=%r>' % self._isAlive


class Achievements(_Condition, _Negatable, _Updatable):

    def __init__(self, path, data):
        super(Achievements, self).__init__('achievements', dict(data), path)
        self._achieves = set(self._data.get('value'))
        self._isNegative = False

    def negate(self):
        self._isNegative = not self._isNegative

    def update(self, other, groupType):
        if groupType == GROUP_TYPE.OR and other.getName() == 'achievements':
            self._achieves |= other._achieves
            return True
        return False

    def isNegative(self):
        return self._isNegative

    def getValue(self):
        return self._achieves

    def __repr__(self):
        return 'Achievements<idx=%r>' % self._achieves


class ClanKills(_Condition, _Negatable):

    def __init__(self, path, data):
        super(ClanKills, self).__init__('clanKills', dict(data), path)
        self._camos2ids = {}
        self._isNegative = False
        for camoName, ids in data:
            self._camos2ids[camoName] = ids

    def negate(self):
        self._isNegative = not self._isNegative

    def isNegative(self):
        return self._isNegative

    def getCamos2ids(self):
        return self._camos2ids

    def __repr__(self):
        return 'ClanKills<camos=%r>' % str(self._camos2ids)


class _Cumulativable(_Condition):
    __metaclass__ = ABCMeta

    def getProgressPerGroup(self, curProgData=None, prevProgData=None):
        return self._parseProgress(curProgData, prevProgData)

    def getUserString(self, battleTypeName=''):
        pass

    @abstractmethod
    def _getKey(self):
        pass

    @abstractmethod
    def getTotalValue(self):
        pass

    @abstractmethod
    def getBonusData(self):
        pass

    def _parseProgress(self, curProgData, prevProgData):
        result = {}
        bonus = self.getBonusData()
        curProgData = bonus.getProgress() if curProgData is None else curProgData
        if bonus is None:
            return result
        else:
            key = self._getKey()
            groupBy = bonus.getGroupByValue()
            total = self.getTotalValue()
            if groupBy is None:
                diff = 0
                curProg = curProgData.get(None, {})
                current = min(curProg.get(key, 0), total)
                if prevProgData is not None:
                    prevProg = prevProgData.get(None, {})
                    diff = current - min(prevProg.get(key, 0), total)
                result[None] = (min(curProg.get(key, 0), total),
                 total,
                 diff,
                 self.__isProgressCompleted(curProg))
            else:
                for gByKey, progress in curProgData.iteritems():
                    diff = 0
                    current = min(progress.get(key, 0), total)
                    if prevProgData is not None:
                        prevProg = prevProgData.get(gByKey, {})
                        diff = current - min(prevProg.get(key, 0), total)
                    result[gByKey] = (current,
                     total,
                     diff,
                     self.__isProgressCompleted(progress))

            return result

    def __getProgDiff(self, curProg, prevProg):
        if prevProg is None:
            return 0
        else:
            key = self._getKey()
            return curProg.get(key, 0) - prevProg.get(key, 0)

    def __isProgressCompleted(self, progress):
        bonusLimit = self.getBonusData().getBonusLimit()
        return progress.get('bonusCount', 0) >= bonusLimit if bonusLimit is not None else False


class BattlesCount(_Cumulativable):

    def __init__(self, path, data, bonusCond):
        super(BattlesCount, self).__init__('battles', dict(data), path)
        self._bonus = weakref.proxy(bonusCond)

    def getUserString(self, battleTypeName='random'):
        return i18n.makeString(QUESTS.getDetailsDossier(battleTypeName, self._getKey()))

    def _getKey(self):
        pass

    def getTotalValue(self):
        return _getNodeValue(self._data, 'count', 0)

    def hasUpperLimit(self):
        return _getNodeValue(self._data, 'upperLimit', False)

    def getBonusData(self):
        return self._bonus

    def __repr__(self):
        return 'BattlesCount<key=%s; total=%d>' % (self._getKey(), self.getTotalValue())


class BattleResults(_Condition, _Negatable, _Updatable):
    TOP_RANGE_HIGHEST = 1
    TOP_RANGE_LOWEST = 15

    def __init__(self, path, data, localeKey='single'):
        super(BattleResults, self).__init__('results', dict(data), path)
        self._keyName = _getNodeValue(self._data, 'key')
        self._max = (self.TOP_RANGE_HIGHEST, int(_getNodeValue(self._data, 'max', self.TOP_RANGE_LOWEST)))
        self._isTotal = 'total' in self._data
        self._isAvg = 'average' in self._data
        self._relation = _findRelation(self._data.keys())
        self._relationValue = _getNodeValue(self._data, self._relation)
        self._localeKey = localeKey
        self._isNegative = False

    @property
    def relationValue(self):
        return self._relationValue

    @property
    def localeKey(self):
        return self._localeKey

    @property
    def keyName(self):
        return self._keyName

    @property
    def relation(self):
        return self._relation

    def isNegative(self):
        return self._isNegative

    def isAvg(self):
        return self._isAvg

    def isTotal(self):
        return self._isTotal

    def getMaxRange(self):
        return self._max

    def getTopRange(self):
        return self._max if not self._isNegative else (min(self._max[1] + 1, self.TOP_RANGE_LOWEST), self.TOP_RANGE_LOWEST)

    def update(self, other, groupType):
        if groupType == GROUP_TYPE.AND:
            if other.getName() == 'results' and self._keyName == other._keyName:
                topRange, otherTopRange = self.getTopRange(), other.getTopRange()
                self._max = (max(topRange[0], otherTopRange[0]), min(topRange[1], otherTopRange[1]))
                return True
        return False

    def negate(self):
        self._relation = _RELATIONS.getOppositeRelation(self._relation)
        self._isNegative = not self._isNegative

    def __repr__(self):
        return 'BattleResults<key=%s; %s=%r; max=%r; total=%r; avg=%r>' % (self._keyName,
         self._relation,
         self._relationValue,
         self._max,
         self._isTotal,
         self._isAvg)


class UnitResults(_Condition, _Negatable):

    def __init__(self, path, data, preBattleCond=None):
        super(UnitResults, self).__init__('unitResults', dict(data), path)
        self._isAllAlive = _getNodeValue(self._data, 'allAlive')
        self._unitKey = _getArenaBonusType(preBattleCond)
        self._results = []
        for idx, (keyName, value) in enumerate(data):
            resultData, isNegative = None, False
            if keyName == 'not' and len(value):
                (_, resultData), isNegative = value[0], not isNegative
            elif keyName == 'results':
                resultData = value
            if resultData is not None:
                results = BattleResults('%s.battleResults%d' % (path, idx), resultData, localeKey=self._unitKey)
                if isNegative:
                    results.negate()
                self._results.append(results)

        return

    def negate(self):
        self._isAllAlive = not self._isAllAlive
        for result in self._results:
            result.negate()

    def getResults(self):
        return self._results

    def getUnitKey(self):
        return self._unitKey

    def isAllAlive(self):
        return self._isAllAlive

    def __repr__(self):
        return 'UnitResults<resultsCount=%d>' % len(self._results)


class CumulativeResult(_Cumulativable):

    def __init__(self, path, data, bonusCond, isUnit=False, preBattleCond=None):
        super(CumulativeResult, self).__init__('cumulative', dict(data), path)
        self._bonus = weakref.proxy(bonusCond)
        self._key, self._total = self._data.get('value', (None, 0))
        self._isUnit = isUnit
        self._unitName = _getArenaBonusType(preBattleCond)
        return None

    def getUserString(self, battleTypeName=''):
        return self.__getLabelString()

    def _getKey(self):
        return 'unit_%s' % self._key if self._isUnit else self._key

    @property
    def keyName(self):
        return self._key

    def getTotalValue(self):
        return self._total

    def getBonusData(self):
        return self._bonus

    def __getLabelString(self):
        param = i18n.makeString('#quests:details/conditions/cumulative/%s' % self._key)
        if self._isUnit:
            label = '#quests:details/conditions/cumulative/%s' % self._unitName
        else:
            label = '#quests:details/conditions/cumulative/single'
        return i18n.makeString(label, param=param)

    def __repr__(self):
        return 'CumulativeResult<key=%s; total=%d>' % (self._getKey(), self.getTotalValue())


class VehicleKills(_VehsListCondition):

    def __init__(self, path, data):
        super(VehicleKills, self).__init__('vehicleKills', dict(data), path)

    def getVehiclesData(self):
        return _prepareVehData(self._getVehiclesList(self._data))

    def _getLabelKey(self):
        pass

    def __repr__(self):
        return 'VehicleKills<%s=%d>' % (self._relation, self._relationValue)


class VehicleKillsCumulative(_Cumulativable, VehicleKills):

    def __init__(self, path, data, bonusCond):
        super(VehicleKills, self).__init__('vehicleKillsCumulative', dict(data), path)
        self._bonus = weakref.proxy(bonusCond)

    def getUserString(self, battleTypeName=''):
        return i18n.makeString(self._getLabelKey())

    def _getKey(self):
        pass

    def getTotalValue(self):
        return self._relationValue

    def getBonusData(self):
        return self._bonus

    def __repr__(self):
        return 'VehicleKills<key=%s; %s=%d; total=%d>' % (self._getKey(),
         self._relation,
         self._relationValue,
         self.getTotalValue())


class VehicleDamage(_VehsListCondition):

    def __init__(self, path, data):
        super(VehicleDamage, self).__init__('vehicleDamage', dict(data), path)

    def getVehiclesData(self):
        return _prepareVehData(self._getVehiclesList(self._data))

    def _getLabelKey(self):
        pass

    def __repr__(self):
        return 'VehicleDamage<%s=%d>' % (self._relation, self._relationValue)


class VehicleDamageCumulative(_Cumulativable, VehicleDamage):

    def __init__(self, path, data, bonusCond):
        super(VehicleDamage, self).__init__('vehicleDamageCumulative', dict(data), path)
        self._bonus = weakref.proxy(bonusCond)

    def getUserString(self, battleTypeName=''):
        return i18n.makeString(self._getLabelKey())

    def _getKey(self):
        pass

    def getTotalValue(self):
        return self._relationValue

    def getBonusData(self):
        return self._bonus

    def __repr__(self):
        return 'VehicleDamage<key=%s; %s=%d; total=%d>' % (self._getKey(),
         self._relation,
         self._relationValue,
         self.getTotalValue())


class VehicleStun(_VehsListCondition):

    def __init__(self, path, data):
        super(VehicleStun, self).__init__('vehicleStun', dict(data), path)

    def getVehiclesData(self):
        return _prepareVehData(self._getVehiclesList(self._data))

    def getEventCount(self):
        return _getNodeValue(self._data, 'eventCount', default=False)

    def _getLabelKey(self):
        key = 'vehicleStunEventCount' if self.getEventCount() else 'vehicleStun'
        return '#quests:details/conditions/%s' % key

    def __repr__(self):
        return 'VehicleStun<%s=%d>' % (self._relation, self._relationValue)


class VehicleStunCumulative(_Cumulativable, VehicleStun):

    def __init__(self, path, data, bonusCond):
        super(VehicleStun, self).__init__('vehicleStunCumulative', dict(data), path)
        self._bonus = weakref.proxy(bonusCond)

    def getUserString(self, battleTypeName=''):
        return i18n.makeString(self._getLabelKey())

    def _getLabelKey(self):
        return '#quests:details/conditions/%s/cumulative' % self._getKey()

    def _getKey(self):
        return 'vehicleStunEventCount' if self.getEventCount() else 'vehicleStun'

    def getTotalValue(self):
        return self._relationValue

    def getBonusData(self):
        return self._bonus

    def __repr__(self):
        return 'VehicleStun<key=%s; %s=%d; total=%d>' % (self._getKey(),
         self._relation,
         self._relationValue,
         self.getTotalValue())


class RefSystemRalXPPoolCondition(_Requirement):

    def __init__(self, path, data):
        super(RefSystemRalXPPoolCondition, self).__init__('refSystemRalXPPool', dict(data), path)
        self._relation = _findRelation(self._data.keys())
        self._relationValue = float(_getNodeValue(self._data, self._relation))

    def negate(self):
        self._relation = _RELATIONS.getOppositeRelation(self._relation)

    def getValue(self):
        return self._relationValue

    def __repr__(self):
        return 'RefSystemRalXPPoolCondition<%s=%s>' % (self._relation, str(self._relationValue))


class RefSystemRalBought10Lvl(_Requirement):

    def __init__(self, path, data):
        super(RefSystemRalBought10Lvl, self).__init__('refSystemRalBought10Lvl', dict(data), path)
        self._relation = bool(self._data['value'])

    def negate(self):
        self._relation = not self._relation

    def getValue(self):
        return self._relation

    def __repr__(self):
        return 'RefSystemRalBought10Lvl<value=%r>' % self._relation

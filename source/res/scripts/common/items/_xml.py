# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/common/items/_xml.py
from functools import wraps, partial
from soft_exception import SoftException
from constants import SEASON_TYPE_BY_NAME, RentType, IS_BASEAPP
_g_floats = {'count': 0}
_g_intTuples = {'count': 0}
_g_floatTuples = {'count': 0}

def cacheTuple(f, valueStorage, tupleStorage):

    @wraps(f)
    def wrapper(*args, **kwargs):
        v = f(*args, **kwargs)
        if not tupleStorage:
            return v
        else:
            tupleStorage['count'] += 1
            cached = tupleStorage.get(v, None)
            if cached is not None:
                return cached
            cached = tuple([ valueStorage.setdefault(fl, fl) for fl in v ])
            tupleStorage[cached] = cached
            return cached

    return wrapper


def _cacheValue(f, storage):

    @wraps(f)
    def wrapper(*args, **kwargs):
        v = f(*args, **kwargs)
        if not storage:
            return v
        storage['count'] += 1
        return storage.setdefault(v, v)

    return wrapper


cacheFloat = partial(_cacheValue, storage=_g_floats)
cacheIntTuples = partial(_cacheValue, storage=_g_intTuples)
cacheFloatTuples = partial(cacheTuple, valueStorage=_g_floats, tupleStorage=_g_floatTuples)

@cacheFloat
def cachedFloat(v):
    return v


def clearCaches():
    global _g_floatTuples
    global _g_floats
    global _g_intTuples
    _g_floats.clear()
    _g_intTuples.clear()
    _g_floatTuples.clear()


def raiseWrongXml(xmlContext, subsectionName, msg):
    fileName = subsectionName
    while xmlContext is not None:
        fileName = xmlContext[1] + ('/' + fileName if fileName else '')
        xmlContext = xmlContext[0]

    raise SoftException("error in '" + fileName + "': " + msg)
    return


def raiseWrongSection(xmlContext, subsectionName):
    raiseWrongXml(xmlContext, '', "subsection '%s' is missing or wrong" % subsectionName)


def getChildren(xmlCtx, section, subsectionName, throwIfMissing=True):
    subsection = section[subsectionName]
    if subsection is None:
        if throwIfMissing:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
        else:
            return []
    return subsection.items()


def getSubsection(xmlCtx, section, subsectionName, throwIfMissing=True):
    subsection = section[subsectionName]
    if subsection is None and throwIfMissing:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return subsection


def getSubSectionWithContext(xmlCtx, section, subsectionName, throwIfMissing=True):
    subsection = getSubsection(xmlCtx, section, subsectionName, throwIfMissing)
    subXmlCtx = (xmlCtx, subsectionName)
    return (subXmlCtx, subsection)


def getItemsWithContext(xmlCtx, section, selectSubSectionName=None):
    return [ (subsectionName, ((xmlCtx, subsectionName), subsection)) for subsectionName, subsection in section.items() if selectSubSectionName is None or selectSubSectionName == subsectionName ]


def getChildrenWithContext(xmlCtx, section, subsectionName, throwIfMissing=True):
    subXmlCtx, subsection = getSubSectionWithContext(xmlCtx, section, subsectionName, throwIfMissing)
    return getItemsWithContext(subXmlCtx, subsection)


def readString(xmlCtx, section, subsectionName):
    subsection = section[subsectionName]
    if subsection is None:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return intern(subsection.asString)


def readStringOrNone(xmlCtx, section, subsectionName):
    subsection = section[subsectionName]
    return None if subsection is None else intern(subsection.asString)


def readStringOrEmpty(xmlCtx, section, subsectionName):
    subsection = section[subsectionName]
    return intern('') if subsection is None else intern(subsection.asString)


def readNonEmptyString(xmlCtx, section, subsectionName):
    v = section.readString(subsectionName)
    if not v:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return intern(v)


def readBool(xmlCtx, section, subsectionName, default=None):
    subsection = section[subsectionName]
    if subsection is None:
        if default is not None:
            return default
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return subsection.asBool


def readInt(xmlCtx, section, subsectionName, minVal=None, maxVal=None):
    wrongVal = -123456789
    v = section.readInt(subsectionName, wrongVal)
    if v == wrongVal:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    if minVal is not None and v < minVal or maxVal is not None and v > maxVal:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return v


def readPositiveInt(xmlCtx, section, subsectionName):
    return readInt(xmlCtx, section, subsectionName, minVal=1)


def readNonNegativeInt(xmlCtx, section, subsectionName):
    return readInt(xmlCtx, section, subsectionName, minVal=0)


def readIntOrNone(xmlCtx, section, subsectionName):
    subsection = section[subsectionName]
    if subsection is None:
        return
    else:
        try:
            return int(subsection.asString, 0)
        except ValueError:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)

        return


@cacheFloat
def readFloat(xmlCtx, section, subsectionName, defaultValue=None):
    if defaultValue is not None and not section.has_key(subsectionName):
        return defaultValue
    else:
        wrongVal = -1000000.0
        v = section.readFloat(subsectionName, wrongVal)
        if v < wrongVal + 1.0:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
        return v


@cacheFloat
def readPositiveFloat(xmlCtx, section, subsectionName, defaultValue=None):
    if defaultValue is not None and not section.has_key(subsectionName):
        return defaultValue
    else:
        v = section.readFloat(subsectionName, -1000000.0)
        if v <= 0.0:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
        return v


@cacheFloat
def readNonNegativeFloat(xmlCtx, section, subsectionName, defaultValue=None):
    if defaultValue is not None and not section.has_key(subsectionName):
        return defaultValue
    else:
        v = section.readFloat(subsectionName, -1000000.0)
        if v < 0.0:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
        return v


@cacheFloat
def readFraction(xmlCtx, section, subsectionName):
    v = section.readFloat(subsectionName, -1000000.0)
    if not 0.0 <= v <= 1.0:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return v


def readVector2(xmlCtx, section, subsectionName):
    wrongVal = (-1000000.0, -1000000.0)
    v = section.readVector2(subsectionName, wrongVal)
    if v[0] < wrongVal[0] + 1.0:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return v


def readPositiveVector2(xmlCtx, section, subsectionName):
    wrongVal = (-1000000.0, -1000000.0)
    v = section.readVector2(subsectionName, wrongVal)
    if v.x <= 0.0 or v.y <= 0.0:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return v


def readVector3(xmlCtx, section, subsectionName):
    wrongVal = (-1000000.0, -1000000.0, -1000000.0)
    v = section.readVector3(subsectionName, wrongVal)
    if v[0] < wrongVal[0] + 1.0:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return v


def readVector3OrNone(xmlCtx, section, subsectionName):
    wrongVal = (-1000000.0, -1000000.0, -1000000.0)
    v = section.readVector3(subsectionName, wrongVal)
    if wrongVal == tuple(v):
        return None
    else:
        if v[0] < wrongVal[0] + 1.0:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
        return v


@cacheFloatTuples
def readTupleOfFloats(xmlCtx, section, subsectionName, count=None):
    strings = getSubsection(xmlCtx, section, subsectionName).asString.split()
    if count is not None and len(strings) != count:
        raiseWrongXml(xmlCtx, subsectionName, '%d floats expected' % count)
    try:
        return tuple(map(float, strings))
    except Exception:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)

    return


@cacheFloatTuples
def readTupleOfPositiveFloats(xmlCtx, section, subsectionName, count=None):
    floats = readTupleOfFloats(xmlCtx, section, subsectionName, count)
    if sum((1 for val in floats if val <= 0)):
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return floats


@cacheFloatTuples
def readTupleOfNonNegativeFloats(xmlCtx, section, subsectionName, count=None):
    floats = readTupleOfFloats(xmlCtx, section, subsectionName, count)
    if sum((1 for val in floats if val < 0)):
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return floats


@cacheIntTuples
def readTupleOfInts(xmlCtx, section, subsectionName, count=None):
    strings = getSubsection(xmlCtx, section, subsectionName).asString.split()
    if count is not None and len(strings) != count:
        raiseWrongXml(xmlCtx, subsectionName, '%d ints expected' % count)
    try:
        return tuple((int(float(s)) for s in strings))
    except Exception:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)

    return


@cacheIntTuples
def readTupleOfPositiveInts(xmlCtx, section, subsectionName, count=None):
    ints = readTupleOfInts(xmlCtx, section, subsectionName, count)
    if sum((1 for val in ints if val <= 0)):
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return ints


@cacheIntTuples
def readTupleOfNonNegativeInts(xmlCtx, section, subsectionName, count=None):
    ints = readTupleOfInts(xmlCtx, section, subsectionName, count)
    if sum((1 for val in ints if val < 0)):
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
    return ints


def readTupleOfStrings(xmlCtx, section, subsectionName, count=None, separator=' '):
    strings = getSubsection(xmlCtx, section, subsectionName).asString.split(separator)
    if count is not None and len(strings) != count:
        raiseWrongXml(xmlCtx, subsectionName, '%d strings expected' % count)
    return tuple(strings)


def readTupleOfBools(xmlCtx, section, subsectionName, count=None):
    strings = getSubsection(xmlCtx, section, subsectionName).asString.split()
    if count is not None and len(strings) != count:
        raiseWrongXml(xmlCtx, subsectionName, '%d bools expected' % count)
    try:
        return tuple(map(lambda s: s.lower() == 'true', strings))
    except Exception:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)

    return


def readPrice(xmlCtx, section, subsectionName):
    key = 'credits'
    if section[subsectionName + '/gold'] is not None:
        key = 'gold'
    if section[subsectionName + '/crystal'] is not None:
        key = 'crystal'
    return {key: readInt(xmlCtx, section, subsectionName, 0)}


def readRentPrice(xmlCtx, section, subsectionName):
    rentPrices = {}
    previousRentDays = []
    previousSeasonIDs = []
    if section[subsectionName] is not None:
        for rentPackageName, subSection in section[subsectionName].items():
            readRentDays(xmlCtx, rentPrices, previousRentDays, subSection, 'days', rentPackageName)
            readRentSeason(xmlCtx, rentPrices, previousSeasonIDs, subSection, 'season', rentPackageName)

    return rentPrices


def raiseWrongSeasonID(xmlCtx, rentPackageName, subsectionName):
    raiseWrongXml(xmlCtx, rentPackageName, '<{}><id> has wrong format. Expected: season_YYYYMMDD.'.format(subsectionName))


def raiseWrongSeasonCycleID(xmlCtx, rentPackageName, subsectionName, cycleID):
    raiseWrongXml(xmlCtx, rentPackageName, '<{}><cycles><{}> has wrong format. Expected: cycle_YYYYMMDD.'.format(subsectionName, cycleID))


def readRentDays(xmlCtx, rentPrices, previousRentDays, section, subsectionName, rentPackageName):
    days = readIntOrNone(xmlCtx, section, subsectionName)
    if days is not None:
        if days <= 0:
            raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)
        elif days in previousRentDays:
            raiseWrongXml(xmlCtx, rentPackageName, '<days> Rent duration for time rent is not unique.')
        price = readPrice(xmlCtx, section, 'cost')
        compensation = readPrice(xmlCtx, section, 'compensation')
        rentConfig = {'cost': (price.get('credits', 0), price.get('gold', 0)),
         'compensation': (compensation.get('credits', 0), compensation.get('gold', 0))}
        previousRentDays.append(days)
        rentPrices.setdefault(RentType.TIME_RENT, {})[days] = rentConfig
    return


def readRentSeason(xmlCtx, rentPrices, previousSeasonIDs, section, subsectionName, rentPackageName):
    season = section[subsectionName]
    if season is not None:
        seasonID = None
        seasonIDString = readString(xmlCtx, season, 'id')
        if not seasonIDString.startswith('season_'):
            raiseWrongSeasonID(xmlCtx, rentPackageName, subsectionName)
        try:
            seasonID = int(seasonIDString[7:])
        except ValueError:
            raiseWrongSeasonID(xmlCtx, rentPackageName, subsectionName)

        if seasonID in previousSeasonIDs:
            raiseWrongXml(xmlCtx, rentPackageName, '<{}><id> Season ID is not unique.'.format(subsectionName))
        defaultCyclePrice = readPrice(xmlCtx, season, 'cycleCost')
        defaultCycleCompensation = readPrice(xmlCtx, season, 'cycleCompensation')
        seasonType = SEASON_TYPE_BY_NAME.get(readString(xmlCtx, season, 'type'), None)
        if seasonType is None:
            raiseWrongXml(xmlCtx, rentPackageName, '<season><type> has wrong format. Expected any valid type in constants.SEASON_TYPE_BY_NAME.')
        cycles = readRentSeasonCycles(xmlCtx, season, 'cycles', defaultCyclePrice, defaultCycleCompensation, seasonType, rentPackageName)
        seasonPrice = readPrice(xmlCtx, section, 'cost')
        seasonCompensation = readPrice(xmlCtx, section, 'compensation')
        seasonRentConfig = {'cost': (seasonPrice.get('credits', 0), seasonPrice.get('gold', 0)),
         'compensation': (seasonCompensation.get('credits', 0), seasonCompensation.get('gold', 0)),
         'seasonType': seasonType,
         'defaultCycleCost': (defaultCyclePrice.get('credits', 0), defaultCyclePrice.get('gold', 0)),
         'cycles': cycles.keys()}
        rentPrices.setdefault(RentType.SEASON_CYCLE_RENT, {}).update(cycles)
        rentPrices.setdefault(RentType.SEASON_RENT, {})[seasonID] = seasonRentConfig
    return


def readRentSeasonCycles(xmlCtx, section, subsectionName, defaultPrice, defaultCompensation, seasonType, packageName):
    cyclesRentPrices = {}
    cycles = section[subsectionName]
    if cycles is not None:
        for cycleIDString, cycle in cycles.items():
            if not cycleIDString.startswith('cycle_'):
                raiseWrongSeasonCycleID(xmlCtx, packageName, subsectionName, cycleIDString)
            cycleID = None
            try:
                cycleID = int(cycleIDString[6:])
            except ValueError:
                raiseWrongSeasonCycleID(xmlCtx, packageName, subsectionName, cycleIDString)

            if cycle['cost'] is not None:
                cyclePrice = readPrice(xmlCtx, cycle, 'cost')
            else:
                cyclePrice = defaultPrice
            if cycle['compensation'] is not None:
                compensation = readPrice(xmlCtx, cycle, 'compensation')
            else:
                compensation = defaultCompensation
            cycleRentConfig = {'cost': (cyclePrice.get('credits', 0), cyclePrice.get('gold', 0)),
             'seasonType': seasonType,
             'compensation': (compensation.get('credits', 0), compensation.get('gold', 0))}
            cyclesRentPrices[cycleID] = cycleRentConfig

    else:
        raiseWrongXml(xmlCtx, packageName, '<{}><{}> missing!'.format(subsectionName, subsectionName))
    return cyclesRentPrices


def readIcon(xmlCtx, section, subsectionName):
    strings = getSubsection(xmlCtx, section, subsectionName).asString.split()
    try:
        return (strings[0], int(strings[1]), int(strings[2]))
    except Exception:
        raiseWrongSection(xmlCtx, subsectionName if subsectionName else section.name)

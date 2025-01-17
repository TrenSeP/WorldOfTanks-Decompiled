# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/battle_control/avatar_getter.py
import logging
import BigWorld
import Math
from gui import GUI_CTRL_MODE_FLAG
_logger = logging.getLogger(__name__)

def isForcedGuiControlMode(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.isForcedGuiControlMode()
    except AttributeError:
        _logger.warning('Attribute "isForcedGuiControlMode" not found')
        result = False

    return result


def getForcedGuiControlModeFlags(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.getForcedGuiControlModeFlags()
    except AttributeError:
        _logger.warning('Attribute "getForcedGuiControlModeFlags" not found')
        result = 0

    return result


def setForcedGuiControlMode(value, stopVehicle=False, enableAiming=True, cursorVisible=True):
    if value:
        flags = GUI_CTRL_MODE_FLAG.CURSOR_ATTACHED
        if stopVehicle:
            flags |= GUI_CTRL_MODE_FLAG.MOVING_DISABLED
        if enableAiming:
            flags |= GUI_CTRL_MODE_FLAG.AIMING_ENABLED
        if cursorVisible:
            flags |= GUI_CTRL_MODE_FLAG.CURSOR_VISIBLE
    else:
        flags = GUI_CTRL_MODE_FLAG.CURSOR_DETACHED
    try:
        return BigWorld.player().setForcedGuiControlMode(flags)
    except AttributeError:
        _logger.exception('Attribute "setForcedGuiControlMode" not found')
        return False


def getPlayerName(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.name
    except AttributeError:
        _logger.warning('Attribute "name" not found')
        result = ''

    return result


def getPlayerTeam(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    return getattr(avatar, 'team', 0)


def getPlayerVehicleID(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    return getattr(avatar, 'playerVehicleID', 0)


def isPlayerTeamKillSuspected():
    return bool(getattr(BigWorld.player(), 'tkillIsSuspected', 0))


def isVehicleAlive(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.isVehicleAlive
    except AttributeError:
        _logger.warning('Attribute "isVehicleAlive" not found')
        result = False

    return result


def isVehicleOverturned(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.isVehicleOverturned
    except AttributeError:
        _logger.warning('Attribute "isVehicleOverturned" not found')
        result = False

    return result


def isVehicleBarrelUnderWater(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.isOwnBarrelUnderWater
    except AttributeError:
        _logger.warning('Attribute "isOwnBarrelUnderWater" not found')
        result = False

    return result


def isVehicleInFire(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.fireInVehicle
    except AttributeError:
        _logger.warning('Attribute "fireInVehicle" not found')
        result = False

    return result


def getVehicleDeviceStates(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.deviceStates
    except AttributeError:
        _logger.warning('Attribute "deviceStates" not found')
        result = {}

    return result


def getVehicleTypeDescriptor(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.vehicleTypeDescriptor
    except AttributeError:
        _logger.warning('Attribute "vehicleTypeDescriptor" not found')
        result = None

    return result


def getVehicleExtrasDict(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.vehicleTypeDescriptor.extrasDict
    except AttributeError:
        _logger.warning('Attribute "vehicleTypeDescriptor.extrasDict" not found')
        result = {}

    return result


def getSoundNotifications(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.soundNotifications
    except AttributeError:
        _logger.warning('Attribute "soundNotifications" not found')
        result = None

    return result


def isPlayerOnArena(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.isOnArena
    except AttributeError:
        _logger.warning('Attribute "isOnArena" not found')
        result = False

    return result


def getInputHandler(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.inputHandler
    except AttributeError:
        _logger.warning('Attribute "inputHandler" not found')
        result = None

    return result


def getArena(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.arena
    except AttributeError:
        _logger.warning('Attribute "arena" not found')
        result = None

    return result


def getArenaUniqueID(avatar=None):
    try:
        return getArena(avatar).arenaUniqueID
    except AttributeError:
        _logger.warning('Attribute "arenaUniqueID" not found')

    return None


def updateVehicleSetting(code, value, avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    vehicleid = avatar.playerVehicleID
    if avatar.getVehicleAttached() is not None:
        vehicleid = avatar.getVehicleAttached().id
    try:
        avatar.updateVehicleSetting(vehicleid, code, value)
    except AttributeError:
        _logger.exception('Attribute "updateVehicleSetting" not found')

    return


def changeVehicleSetting(code, value, avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        avatar.base.vehicle_changeSetting(code, value)
    except AttributeError:
        _logger.warning('Attribute "base.vehicle_changeSetting" not found')

    return


def activateAvatarEquipment(equipmentID, avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        avatar.cell.activateEquipment(equipmentID)
    except AttributeError:
        _logger.warning('Attribute "cell.activateEquipment" not found')

    return


def leaveArena(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        avatar.leaveArena()
    except AttributeError:
        _logger.warning('Attribute "leaveArena" not found')

    return


def switchToOtherPlayer(vehicleID, avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        avatar.selectPlayer(vehicleID)
    except AttributeError:
        _logger.warning('Attribute "selectPlayer" not found')

    return


def setComponentsVisibility(flag, avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        avatar.setComponentsVisibility(flag)
    except AttributeError:
        _logger.warning('Attribute "setComponentsVisibility" not found')

    return


def getOwnVehiclePosition(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        position = avatar.getOwnVehiclePosition()
    except AttributeError:
        position = None
        _logger.warning('Attribute "getOwnVehiclePosition" not found')

    return position


def getDistanceToTarget(target, avatar=None):
    ownPosition = getOwnVehiclePosition(avatar=avatar)
    return (target.position - ownPosition).length if ownPosition is not None else 0.0


def getDistanceToGunMarker(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    ownPosition = getOwnVehiclePosition(avatar=avatar)
    if ownPosition is None:
        return 0.0
    else:
        try:
            gunPosition = avatar.gunRotator.markerInfo[0]
        except AttributeError:
            _logger.warning('Attribute "gunRotator.markerInfo" not found')
            return 0.0

        return (ownPosition - Math.Vector3(*gunPosition)).length


def isVehicleStunned():
    attachedVehicle = BigWorld.player().getVehicleAttached()
    return attachedVehicle.stunInfo > 0.0 if attachedVehicle is not None else False


def getHealthPercentage(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        hp = avatar.getHealthPercentage()
    except AttributeError:
        _logger.warning('Attribute "getHealthPercentage" not found')
        return [0.0, 0.0]

    return hp


def getLastRecoveryArgs(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.getLastRecoveryArgs()
    except AttributeError:
        _logger.warning('Attribute "getLastRecoveryArgs" not found')
        result = None

    return result


def getVehicleIDAttached(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        result = avatar.getVehicleAttached().id
    except AttributeError:
        _logger.warning('Attribute "getVehicleAttached" is not found')
        result = None

    return result


def setClientReady(avatar=None):
    if avatar is None:
        avatar = BigWorld.player()
    try:
        avatar.setClientReady()
    except AttributeError:
        _logger.warning('Attribute "setClientReady" not found')

    return

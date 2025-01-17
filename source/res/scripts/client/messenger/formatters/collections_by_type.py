# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/messenger/formatters/collections_by_type.py
from chat_shared import SYS_MESSAGE_TYPE as _SM_TYPE
from messenger.formatters import service_channel as _sc
from messenger.m_constants import SCH_CLIENT_MSG_TYPE
SERVER_FORMATTERS = {_SM_TYPE.serverReboot.index(): _sc.ServerRebootFormatter(),
 _SM_TYPE.serverRebootCancelled.index(): _sc.ServerRebootCancelledFormatter(),
 _SM_TYPE.battleResults.index(): _sc.BattleResultsFormatter(),
 _SM_TYPE.invoiceReceived.index(): _sc.InvoiceReceivedFormatter(),
 _SM_TYPE.adminTextMessage.index(): _sc.AdminMessageFormatter(),
 _SM_TYPE.accountTypeChanged.index(): _sc.AccountTypeChangedFormatter(),
 _SM_TYPE.giftReceived.index(): _sc.GiftReceivedFormatter(),
 _SM_TYPE.autoMaintenance.index(): _sc.AutoMaintenanceFormatter(),
 _SM_TYPE.premiumBought.index(): _sc.PremiumBoughtFormatter(),
 _SM_TYPE.premiumExtended.index(): _sc.PremiumExtendedFormatter(),
 _SM_TYPE.premiumExpired.index(): _sc.PremiumExpiredFormatter(),
 _SM_TYPE.prbArenaFinish.index(): _sc.PrebattleArenaFinishFormatter(),
 _SM_TYPE.prbKick.index(): _sc.PrebattleKickFormatter(),
 _SM_TYPE.prbDestruction.index(): _sc.PrebattleDestructionFormatter(),
 _SM_TYPE.vehicleCamouflageTimedOut.index(): _sc.VehCamouflageTimedOutFormatter(),
 _SM_TYPE.vehiclePlayerEmblemTimedOut.index(): _sc.VehEmblemTimedOutFormatter(),
 _SM_TYPE.vehiclePlayerInscriptionTimedOut.index(): _sc.VehInscriptionTimedOutFormatter(),
 _SM_TYPE.vehTypeLockExpired.index(): _sc.VehicleTypeLockExpired(),
 _SM_TYPE.serverDowntimeCompensation.index(): _sc.ServerDowntimeCompensation(),
 _SM_TYPE.achievementReceived.index(): _sc.AchievementFormatter(),
 _SM_TYPE.converter.index(): _sc.ConverterFormatter(),
 _SM_TYPE.tokenQuests.index(): _sc.TokenQuestsFormatter(),
 _SM_TYPE.notificationsCenter.index(): _sc.NCMessageFormatter(),
 _SM_TYPE.clanEvent.index(): _sc.ClanMessageFormatter(),
 _SM_TYPE.fortEvent.index(): _sc.StrongholdMessageFormatter(),
 _SM_TYPE.vehicleRented.index(): _sc.VehicleRentedFormatter(),
 _SM_TYPE.rentalsExpired.index(): _sc.RentalsExpiredFormatter(),
 _SM_TYPE.potapovQuestBonus.index(): _sc.PersonalMissionsFormatter(),
 _SM_TYPE.goodieRemoved.index(): _sc.GoodyRemovedFormatter(),
 _SM_TYPE.goodieDisabled.index(): _sc.GoodyDisabledFormatter(),
 _SM_TYPE.telecomOrderCreated.index(): _sc.TelecomReceivedInvoiceFormatter(),
 _SM_TYPE.telecomOrderUpdated.index(): _sc.TelecomStatusFormatter(),
 _SM_TYPE.telecomOrderDeleted.index(): _sc.TelecomRemovedInvoiceFormatter(),
 _SM_TYPE.prbVehicleKick.index(): _sc.PrbVehicleKickFormatter(),
 _SM_TYPE.vehicleGroupLocked.index(): _sc.RotationGroupLockFormatter(),
 _SM_TYPE.vehicleGroupUnlocked.index(): _sc.RotationGroupUnlockFormatter(),
 _SM_TYPE.rankedQuests.index(): _sc.RankedQuestFormatter(),
 _SM_TYPE.bootcamp.index(): _sc.BootcampResultsFormatter(),
 _SM_TYPE.prbVehicleMaxSpgKick.index(): _sc.PrbVehicleMaxSpgKickFormatter(),
 _SM_TYPE.hangarQuests.index(): _sc.TokenQuestsFormatter(),
 _SM_TYPE.currencyUpdate.index(): _sc.CurrencyUpdateFormatter(),
 _SM_TYPE.personalMissionFailed.index(): _sc.PersonalMissionFailedFormatter(),
 _SM_TYPE.customizationChanged.index(): _sc.CustomizationChangedFormatter(),
 _SM_TYPE.lootBoxesAutoOpenReward.index(): _sc.LootBoxAutoOpenFormatter(),
 _SM_TYPE.progressiveReward.index(): _sc.ProgressiveRewardFormatter()}
CLIENT_FORMATTERS = {SCH_CLIENT_MSG_TYPE.SYS_MSG_TYPE: _sc.ClientSysMessageFormatter(),
 SCH_CLIENT_MSG_TYPE.PREMIUM_ACCOUNT_EXPIRY_MSG: _sc.PremiumAccountExpiryFormatter(),
 SCH_CLIENT_MSG_TYPE.AOGAS_NOTIFY_TYPE: _sc.AOGASNotifyFormatter(),
 SCH_CLIENT_MSG_TYPE.ACTION_NOTIFY_TYPE: _sc.ActionNotificationFormatter(),
 SCH_CLIENT_MSG_TYPE.BATTLE_TUTORIAL_RESULTS_TYPE: _sc.BattleTutorialResultsFormatter(),
 SCH_CLIENT_MSG_TYPE.KOREA_PARENTAL_CONTROL_TYPE: _sc.KoreaParentalControlFormatter()}

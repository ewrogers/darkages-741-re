# Client packets

These messages travel from the game client to the server.

The binary exposes only the client packet base class through RTTI. Concrete names therefore come from local builder behavior and project-owner protocol knowledge. Each page states its name source and lists known UI or subsystem owners without mixing in address-level lookup data.

Plain packet bodies begin with the command byte. `CBaram` is listed for sequence research, but its five-byte `baram` body is a special control message rather than an ordinary packet.

| Command | Packet | Encoding |
| --- | --- | --- |
| `0x00` (0) | [Version (`CVersion`)](000-0x00-version.md) | none |
| `0x02` (2) | [New User (`CNewUser`)](002-0x02-new-user.md) | startup key |
| `0x03` (3) | [Login (`CLogin`)](003-0x03-login.md) | startup key |
| `0x04` (4) | [New User Appearance (`CNewUserAppearance`)](004-0x04-new-user-appearance.md) | startup key |
| `0x05` (5) | [Map Request (`CMapRequest`)](005-0x05-map-request.md) | session key |
| `0x06` (6) | [Move (`CMove`)](006-0x06-move.md) | session key |
| `0x07` (7) | [Get (`CGet`)](007-0x07-get.md) | session key |
| `0x08` (8) | [Drop (`CDrop`)](008-0x08-drop.md) | session key |
| `0x0B` (11) | [Quit (`CQuit`)](011-0x0b-quit.md) | startup key |
| `0x0C` (12) | [Put Ground (`CPutGround`)](012-0x0c-put-ground.md) | session key |
| `0x0D` (13) | [Block Listen (`CBlockListen`)](013-0x0d-block-listen.md) | session key |
| `0x0E` (14) | [Say (`CSay`)](014-0x0e-say.md) | session key |
| `0x0F` (15) | [Use Spell (`CUseSpell`)](015-0x0f-use-spell.md) | session key |
| `0x10` (16) | [Transfer Server (`CTransferServer`)](016-0x10-transfer-server.md) | none |
| `0x11` (17) | [Change Direction (`CChangeDirection`)](017-0x11-change-direction.md) | session key |
| `0x13` (19) | [Attack (`CAttack`)](019-0x13-attack.md) | session key |
| `0x18` (24) | [Who (`CWho`)](024-0x18-who.md) | session key |
| `0x19` (25) | [Tell (`CTell`)](025-0x19-tell.md) | session key |
| `0x1B` (27) | [User Setting (`CUserSetting`)](027-0x1b-user-setting.md) | session key |
| `0x1C` (28) | [Use (`CUse`)](028-0x1c-use.md) | session key |
| `0x1D` (29) | [Emotion (`CEmotion`)](029-0x1d-emotion.md) | session key |
| `0x23` (35) | [Exit Editing Mode (`CExitEditingMode`)](035-0x23-exit-editing-mode.md) | session key |
| `0x24` (36) | [Drop Gold (`CDropGold`)](036-0x24-drop-gold.md) | session key |
| `0x26` (38) | [Change Password (`CChangePassword`)](038-0x26-change-password.md) | startup key |
| `0x29` (41) | [Give (`CGive`)](041-0x29-give.md) | session key |
| `0x2A` (42) | [Give Gold (`CGiveGold`)](042-0x2a-give-gold.md) | session key |
| `0x2D` (45) | [Self Look (`CSelfLook`)](045-0x2d-self-look.md) | startup key |
| `0x2E` (46) | [Group (`CGroup`)](046-0x2e-group.md) | session key |
| `0x2F` (47) | [Group Toggle (`CGroupToggle`)](047-0x2f-group-toggle.md) | session key |
| `0x30` (48) | [Change Slot (`CChangeSlot`)](048-0x30-change-slot.md) | session key |
| `0x31` (49) | [Confirm (`CConfirm`)](049-0x31-confirm.md) | session key |
| `0x38` (56) | [Refresh User (`CRefreshUser`)](056-0x38-refresh-user.md) | session key |
| `0x39` (57) | [Merchant (`CMenuCode`)](057-0x39-merchant.md) | session key |
| `0x3A` (58) | [Pursuit (`CMessage`)](058-0x3a-pursuit.md) | startup key |
| `0x3B` (59) | [Bulletin (`CBulletin`)](059-0x3b-bulletin.md) | session key |
| `0x3E` (62) | [Use Skill (`CUseSkill`)](062-0x3e-use-skill.md) | session key |
| `0x3F` (63) | [Field Map (`CFieldMap`)](063-0x3f-field-map.md) | session key |
| `0x42` (66) | [Exception (`CException`)](066-0x42-exception.md) | startup key |
| `0x43` (67) | [Request Object Info (`CRequestObjectInfo`)](067-0x43-request-object-info.md) | startup key |
| `0x44` (68) | [Remove Equipment (`CRemoveEquipment`)](068-0x44-remove-equipment.md) | session key |
| `0x45` (69) | [Reply CRC (`CReplyCRC`)](069-0x45-reply-crc.md) | session key |
| `0x47` (71) | [Add Stat (`CAddStat`)](071-0x47-add-stat.md) | session key |
| `0x48` (72) | [Request Patch (`CRequestPatch`)](072-0x48-request-patch.md) | none |
| `0x4A` (74) | [Exchange (`CExchange`)](074-0x4a-exchange.md) | session key |
| `0x4B` (75) | [Stipulation (`CStipulation`)](075-0x4b-stipulation.md) | startup key |
| `0x4D` (77) | [Spell Delay Request (`CSpellDelayRequest`)](077-0x4d-spell-delay-request.md) | session key |
| `0x4E` (78) | [Spell Delay Say (`CSpellDelaySay`)](078-0x4e-spell-delay-say.md) | session key |
| `0x4F` (79) | [Send Portrait (`CSendPortrait`)](079-0x4f-send-portrait.md) | session key |
| `0x54` (84) | [Mercenary (`CMercenary`)](084-0x54-mercenary.md) | session key |
| `0x55` (85) | [Manual (`CManual`)](085-0x55-manual.md) | session key |
| `0x57` (87) | [Multi Server (`CMulti`)](087-0x57-multi-server.md) | startup key |
| `0x62` (ASCII `b`) | [Baram (`CBaram`)](098-0x62-baram.md) | startup key |
| `0x68` (104) | [Request Homepage (`CRequestHomepage`)](104-0x68-request-homepage.md) | startup key |
| `0x6A` (106) | [Mini Game (`CMiniGame`)](106-0x6a-mini-game.md) | session key |
| `0x6C` (108) | [Cash Shop (`CCashShop`)](108-0x6c-cash-shop.md) | session key |
| `0x71` (113) | [Send Alive (`CSendAlive`)](113-0x71-send-alive.md) | startup key |
| `0x73` (115) | [Web Board (`CWebBoard`)](115-0x73-web-board.md) | startup key |
| `0x75` (117) | [Check Time (`CCheckTime`)](117-0x75-check-time.md) | session key |
| `0x79` (121) | [User Change State (`CUserChangeState`)](121-0x79-user-change-state.md) | session key |
| `0x7A` (122) | [Request Family Name (`CRequestFamilyName`)](122-0x7a-request-family-name.md) | session key |
| `0x7B` (123) | [Meta Data (`CMetaData`)](123-0x7b-meta-data.md) | startup key |

Shared framing and encoding rules are in [Network transport](../transport.md) and [Packet transforms](../packet-transforms.md).

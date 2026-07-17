# Client packets

These messages travel from the game client to the server.

The binary exposes only the client packet base class through RTTI. Concrete names therefore come from local builder behavior and project-owner protocol knowledge. Each page states its name source and lists known UI or subsystem owners without mixing in address-level lookup data.

Body schemas use the shared [packet body notation](../packet-body-notation.md). All multibyte packet integers are big-endian. Reused enum and bit-flag values live in [Shared protocol types](../protocol-types.md).

Plain packet bodies begin with the command byte. For ordinary client packets, `net_submit_client_packet` appends one transmitted zero byte after the builder-provided fields. `CHello` is listed for sequence research, but its `baram` text is a special control message rather than a compiler-recovered packet class.

| Packet | Encoding |
| --- | --- |
| [0x00 - Version (`CVersion`)](000-0x00-version.md) | raw |
| [0x02 - New User (`CNewUser`)](002-0x02-new-user.md) | startup key |
| [0x03 - Login (`CLogin`)](003-0x03-login.md) | startup key |
| [0x04 - New User Appearance (`CNewUserAppearance`)](004-0x04-new-user-appearance.md) | startup key |
| [0x05 - Map Request (`CMapRequest`)](005-0x05-map-request.md) | session key |
| [0x06 - Move (`CMove`)](006-0x06-move.md) | session key |
| [0x07 - Get (`CGet`)](007-0x07-get.md) | session key |
| [0x08 - Drop (`CDrop`)](008-0x08-drop.md) | session key |
| [0x0B - Quit (`CQuit`)](011-0x0b-quit.md) | startup key |
| [0x0C - Put Ground (`CPutGround`)](012-0x0c-put-ground.md) | session key |
| [0x0D - Block Listen (`CBlockListen`)](013-0x0d-block-listen.md) | session key |
| [0x0E - Say (`CSay`)](014-0x0e-say.md) | session key |
| [0x0F - Use Spell (`CUseSpell`)](015-0x0f-use-spell.md) | session key |
| [0x10 - Transfer Server (`CTransferServer`)](016-0x10-transfer-server.md) | none |
| [0x11 - Change Direction (`CChangeDirection`)](017-0x11-change-direction.md) | session key |
| [0x13 - Attack (`CAttack`)](019-0x13-attack.md) | session key |
| [0x18 - Who (`CWho`)](024-0x18-who.md) | session key |
| [0x19 - Tell (`CTell`)](025-0x19-tell.md) | session key |
| [0x1B - User Setting (`CUserSetting`)](027-0x1b-user-setting.md) | session key |
| [0x1C - Use (`CUse`)](028-0x1c-use.md) | session key |
| [0x1D - Emotion (`CEmotion`)](029-0x1d-emotion.md) | session key |
| [0x23 - Exit Editing Mode (`CExitEditingMode`)](035-0x23-exit-editing-mode.md) | session key |
| [0x24 - Drop Gold (`CDropGold`)](036-0x24-drop-gold.md) | session key |
| [0x26 - Change Password (`CChangePassword`)](038-0x26-change-password.md) | startup key |
| [0x29 - Give (`CGive`)](041-0x29-give.md) | session key |
| [0x2A - Give Gold (`CGiveGold`)](042-0x2a-give-gold.md) | session key |
| [0x2D - Self Look (`CSelfLook`)](045-0x2d-self-look.md) | startup key |
| [0x2E - Group (`CGroup`)](046-0x2e-group.md) | session key |
| [0x2F - Group Toggle (`CGroupToggle`)](047-0x2f-group-toggle.md) | session key |
| [0x30 - Change Slot (`CChangeSlot`)](048-0x30-change-slot.md) | session key |
| [0x31 - Confirm (`CConfirm`)](049-0x31-confirm.md) | session key |
| [0x38 - Refresh User (`CRefreshUser`)](056-0x38-refresh-user.md) | session key |
| [0x39 - Merchant (`CMerchant`)](057-0x39-merchant.md) | session key |
| [0x3A - Pursuit (`CPursuit`)](058-0x3a-pursuit.md) | startup key |
| [0x3B - Bulletin (`CBulletin`)](059-0x3b-bulletin.md) | session key |
| [0x3E - Use Skill (`CUseSkill`)](062-0x3e-use-skill.md) | session key |
| [0x3F - Field Map (`CFieldMap`)](063-0x3f-field-map.md) | session key |
| [0x42 - Exception (`CException`)](066-0x42-exception.md) | startup key |
| [0x43 - Request Object Info (`CRequestObjectInfo`)](067-0x43-request-object-info.md) | startup key |
| [0x44 - Remove Equipment (`CRemoveEquipment`)](068-0x44-remove-equipment.md) | session key |
| [0x45 - Reply CRC (`CReplyCRC`)](069-0x45-reply-crc.md) | session key |
| [0x47 - Add Stat (`CAddStat`)](071-0x47-add-stat.md) | session key |
| [0x48 - Request Patch (`CRequestPatch`)](072-0x48-request-patch.md) | none |
| [0x4A - Exchange (`CExchange`)](074-0x4a-exchange.md) | session key |
| [0x4B - Stipulation (`CStipulation`)](075-0x4b-stipulation.md) | startup key |
| [0x4D - Spell Delay Request (`CSpellDelayRequest`)](077-0x4d-spell-delay-request.md) | session key |
| [0x4E - Spell Delay Say (`CSpellDelaySay`)](078-0x4e-spell-delay-say.md) | session key |
| [0x4F - Send Portrait (`CSendPortrait`)](079-0x4f-send-portrait.md) | session key |
| [0x54 - Mercenary (`CMercenary`)](084-0x54-mercenary.md) | session key |
| [0x55 - Manual (`CManual`)](085-0x55-manual.md) | session key |
| [0x57 - Multi Server (`CMulti`)](087-0x57-multi-server.md) | startup key |
| [0x62 - Hello (`CHello`)](098-0x62-hello.md) | static |
| [0x68 - Request Homepage (`CRequestHomepage`)](104-0x68-request-homepage.md) | startup key |
| [0x6A - Mini Game (`CMiniGame`)](106-0x6a-mini-game.md) | session key |
| [0x6C - Cash Shop (`CCashShop`)](108-0x6c-cash-shop.md) | session key |
| [0x71 - Send Alive (`CSendAlive`)](113-0x71-send-alive.md) | startup key |
| [0x73 - Web Board (`CWebBoard`)](115-0x73-web-board.md) | startup key |
| [0x75 - Check Time (`CCheckTime`)](117-0x75-check-time.md) | session key |
| [0x79 - User Change State (`CUserChangeState`)](121-0x79-user-change-state.md) | session key |
| [0x7A - Request Family Name (`CRequestFamilyName`)](122-0x7a-request-family-name.md) | session key |
| [0x7B - Meta Data (`CMetaData`)](123-0x7b-meta-data.md) | startup key |

Shared framing and encoding rules are in [Network transport](../transport.md) and [Packet transforms](../packet-transforms.md).

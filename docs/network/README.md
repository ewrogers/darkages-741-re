# Packet opcode master list

`SPacket` means server-to-client and `CPacket` means client-to-server.

## SPackets: server to client

The 61 names in the main table below are recovered from MSVC RTTI and the factory registry at `0x595F00`. They are the RTTI-backed subset, not the complete supported opcode set.

Lobby/login opcodes `0x00-0x02` are documented separately because they are absent from that 61-entry game-server registry:

| Opcode | Lobby/internal name | Status |
|---:|---|---|
| [0x00](server/000-0x00-version-check.md) | `SVersionCheckPacket` | raw handler recovered; subtype 0 installs salt selector and replacement key; not in game RTTI registry |
| [0x01](server/001-0x01-new-user-check.md) | `SNewUserCheckPacket?` | local primary-key decrypt support; semantics uncertain |
| [0x02](server/002-0x02-check.md) | `SCheckPacket` / `LoginCheck` | known lobby packet with local primary-key decrypt support |

`0x03 STransferServer` remains in the confirmed local registry and can perform the lobby-to-game-server handoff.

The active game dispatcher also recognizes six server opcodes directly from the preserved post-decrypt body, without an RTTI factory:

| Opcode | Internal/related name | Local status |
|---:|---|---|
| [0x1B](server/027-0x1b-enter-editing-mode.md) | `SEnterEditingModePacket?` / `EnterEditingMode` | confirmed; opens editable paper UI |
| 0x31 | `SBulletinPacket?` / `BoardResult` | raw handler confirmed; payload audit pending |
| 0x34 | `SObjectInfoReplyPacket?` / `UserProfile` | raw handler confirmed; payload audit pending |
| [0x35](server/053-0x35-show-paper.md) | `SShowPaper` | confirmed; read-only paper UI, dismissed locally without a client packet |
| 0x36 | `SUserListPacket?` / `WorldList` | raw handler confirmed; payload audit pending |
| 0x4F | `SMercPacket?` | raw handler confirmed; payload audit pending |

| Opcode | SPacket |
|---:|---|
| [0x03](server/003-0x03-transfer-server.md) | STransferServer |
| [0x04](server/004-0x04-user-position.md) | SUserPosition |
| [0x05](server/005-0x05-user-appearance.md) | SUserAppearance |
| [0x06](server/006-0x06-map.md) | SMap |
| [0x07](server/007-0x07-draw-objects.md) | SDrawObjects |
| [0x08](server/008-0x08-status.md) | SStatus |
| [0x0A](server/010-0x0a-message.md) | SMessage |
| [0x0B](server/011-0x0b-move.md) | SMove |
| [0x0C](server/012-0x0c-move-object.md) | SMoveObject |
| [0x0D](server/013-0x0d-say.md) | SSay |
| [0x0E](server/014-0x0e-remove-objects.md) | SRemoveObjects |
| [0x0F](server/015-0x0f-add-inventory.md) | SAddInventory |
| [0x10](server/016-0x10-remove-inventory.md) | SRemoveInventory |
| [0x11](server/017-0x11-change-direction.md) | SChangeDirection |
| [0x13](server/019-0x13-damage-effect.md) | SDamageEffect |
| [0x15](server/021-0x15-map-size.md) | SMapSize |
| [0x17](server/023-0x17-add-spell.md) | SAddSpell |
| [0x18](server/024-0x18-remove-spell.md) | SRemoveSpell |
| [0x19](server/025-0x19-sound-effect.md) | SSoundEffect |
| [0x1A](server/026-0x1a-motion.md) | SMotion |
| [0x1F](server/031-0x1f-change-weather.md) | SChangeWeather |
| [0x20](server/032-0x20-change-hour.md) | SChangeHour |
| [0x21](server/033-0x21-self-save-ok.md) | SSelfSaveOK |
| [0x29](server/041-0x29-effect-layer.md) | SEffectLayer |
| [0x2C](server/044-0x2c-add-skill.md) | SAddSkill |
| [0x2D](server/045-0x2d-remove-skill.md) | SRemoveSkill |
| [0x2E](server/046-0x2e-field-map.md) | SFieldMap |
| [0x2F](server/047-0x2f-screen-menu.md) | SScreenMenu |
| [0x30](server/048-0x30-pursuit-message.md) | SPursuitMessage |
| [0x32](server/050-0x32-static-object-state.md) | SStaticObjectState |
| [0x33](server/051-0x33-draw-human-objects.md) | SDrawHumanObjects |
| [0x37](server/055-0x37-add-equip.md) | SAddEquip |
| [0x38](server/056-0x38-remove-equip.md) | SRemoveEquip |
| [0x39](server/057-0x39-self-look.md) | SSelfLook |
| [0x3A](server/058-0x3a-spelled.md) | SSpelled |
| [0x3B](server/059-0x3b-request-crc.md) | SRequestCRC |
| [0x3C](server/060-0x3c-map-part.md) | SMapPart |
| [0x3D](server/061-0x3d-level-point.md) | SLevelPoint |
| [0x3E](server/062-0x3e-window-change.md) | SWindowChange |
| [0x3F](server/063-0x3f-action-delay.md) | SActionDelay |
| [0x42](server/066-0x42-exchange.md) | SExchange |
| [0x44](server/068-0x44-add-user.md) | SAddUser |
| [0x45](server/069-0x45-item-shop.md) | SItemShop |
| [0x47](server/071-0x47-num-users.md) | SNumUsers |
| [0x48](server/072-0x48-spell-delay-cancel.md) | SSpellDelayCancel |
| [0x49](server/073-0x49-request-portrait.md) | SRequestPortrait |
| [0x4A](server/074-0x4a-bad-guy.md) | SBadGuy |
| [0x4B](server/075-0x4b-bounce.md) | SBounce |
| [0x4C](server/076-0x4c-quit.md) | SQuit |
| [0x50](server/080-0x50-manual.md) | SManual |
| [0x51](server/081-0x51-block-input.md) | SBlockInput |
| [0x56](server/086-0x56-multi.md) | SMulti |
| [0x5B](server/091-0x5b-advertisement.md) | SAdvertisement |
| [0x60](server/096-0x60-stipulation.md) | SStipulation |
| [0x62](server/098-0x62-web-board.md) | SWebBoard |
| [0x63](server/099-0x63-group.md) | SGroup |
| [0x64](server/100-0x64-mini-game.md) | SMiniGame |
| [0x66](server/102-0x66-browser.md) | SBrowser |
| [0x68](server/104-0x68-check-time.md) | SCheckTime |
| [0x6B](server/107-0x6b-screen-shot.md) | SScreenShot |
| [0x6D](server/109-0x6d-family-name.md) | SFamilyName |

## CPackets: client to server

The **66 local CPacket candidates** use recovered class vocabulary and user-provided related-engine terminology where local behavior supports the match. Local opcode, payload, and caller evidence remains authoritative when another game differs. A trailing `?` marks a reconstructed C++ class spelling. See the [full client packet index](client/README.md) for provenance and send-transform details.

| Opcode | Internal packet name | Local behavioral alias | Evidence |
|---:|---|---|---|
| [000 / 0x00](client/000-0x00-version.md) | `CVersionPacket` | `Version` | concrete builder in `sub_579090`; version `741` |
| [002 / 0x02](client/002-0x02-new-user.md) | `CNewUserPacket` | `CreateCharacterName` | 1 concrete builder/sender call site |
| [003 / 0x03](client/003-0x03-login.md) | `CLoginPacket` | `Login` | 1 concrete builder/sender call site |
| [004 / 0x04](client/004-0x04-new-user-info.md) | `CNewUserInfoPacket` | `CreateCharacterAppearance` | 1 concrete builder/sender call site |
| [005 / 0x05](client/005-0x05-map-crc.md) | `CMapCRCPacket` | `RequestMapData` | 1 concrete builder/sender call site |
| [006 / 0x06](client/006-0x06-move.md) | `CMovePacket` | `Walk` | 1 concrete builder/sender call site |
| [007 / 0x07](client/007-0x07-get.md) | `CGetPacket` | `PickupItem` | 2 concrete builder/sender call sites |
| [008 / 0x08](client/008-0x08-drop.md) | `CDropPacket` | `DropItem` | 1 concrete builder/sender call site |
| [009 / 0x09](client/009-0x09-look.md) | `CLookPacket?` | `Look / LookAhead` | user-researched local command; fixed builder call site not yet isolated |
| [010 / 0x0a](client/010-0x0a-far-look.md) | `CFarLookPacket?` | `FarLook / LookTile` | user-researched local command; fixed builder call site not yet isolated |
| [011 / 0x0b](client/011-0x0b-quit.md) | `CQuitPacket` | `RequestExit` | 3 concrete builder/sender call sites |
| [012 / 0x0c](client/012-0x0c-put-request.md) | `CPutRequestPacket` | `RequestEntity` | 1 concrete builder/sender call site |
| [013 / 0x0d](client/013-0x0d-block-listen.md) | `CBlockListenPacket?` | `BlockListen / IgnoreUser` | 3 concrete builder/sender call sites |
| [014 / 0x0e](client/014-0x0e-say.md) | `CSayPacket` | `Say` | 5 concrete builder/sender call sites |
| [015 / 0x0f](client/015-0x0f-use-spell.md) | `CUseSpellPacket` | `CastSpell` | 1 concrete builder/sender call site |
| [016 / 0x10](client/016-0x10-transfer-server.md) | `CTransferServerPacket` | `Authenticate` | 2 concrete builder/sender call sites |
| [017 / 0x11](client/017-0x11-change-dir.md) | `CChangeDirPacket` | `Turn` | 1 concrete builder/sender call site |
| [019 / 0x13](client/019-0x13-attack.md) | `CAttackPacket` | `Assail` | 1 concrete builder/sender call site |
| [024 / 0x18](client/024-0x18-who.md) | `CWhoPacket` | `RequestWorldList` | 1 concrete builder/sender call site |
| [025 / 0x19](client/025-0x19-tell.md) | `CTellPacket` | `Whisper` | 1 concrete builder/sender call site |
| [026 / 0x1a](client/026-0x1a-eat-item.md) | `CEatItemPacket?` | `EatItem` | user-researched local command; fixed builder call site not yet isolated |
| [027 / 0x1b](client/027-0x1b-user-status.md) | `CUserStatusPacket` | `ToggleSetting` | 1 concrete builder/sender call site |
| [028 / 0x1c](client/028-0x1c-use.md) | `CUsePacket` | `UseItem` | 1 concrete builder/sender call site |
| [029 / 0x1d](client/029-0x1d-emotion.md) | `CEmotionPacket` | `Emote` | 1 concrete builder/sender call site |
| [035 / 0x23](client/035-0x23-exit-editing-mode.md) | `CExitEditingModePacket?` | `ExitEditingMode / EditNotepad (Paper)` | 1 concrete builder/sender call site |
| [036 / 0x24](client/036-0x24-drop-gold.md) | `CDropGoldPacket?` | `DropGold` | 1 concrete builder/sender call site |
| [038 / 0x26](client/038-0x26-change-password.md) | `CChangePasswordPacket` | `ChangePassword` | 2 concrete builder/sender call sites |
| [041 / 0x29](client/041-0x29-give.md) | `CGivePacket?` | `Give / GiveItem` | 1 concrete builder/sender call site |
| [042 / 0x2a](client/042-0x2a-give-gold.md) | `CGiveGoldPacket?` | `GiveGold` | 1 concrete builder/sender call site |
| [045 / 0x2d](client/045-0x2d-self-look.md) | `CSelfLookPacket` | `RequestProfile` | 4 concrete builder/sender call sites |
| [046 / 0x2e](client/046-0x2e-party.md) | `CPartyPacket` | `GroupInvite` | 10 concrete builder/sender call sites |
| [047 / 0x2f](client/047-0x2f-group-toggle.md) | `CGroupTogglePacket?` | `GroupToggle / ToggleGroup` | 3 concrete builder/sender call sites |
| [048 / 0x30](client/048-0x30-change-slot.md) | `CChangeSlotPacket` | `SwapSlot` | 3 concrete builder/sender call sites |
| [049 / 0x31](client/049-0x31-user-confirm.md) | `CUserConfirmPacket` | `ConfirmUser` | 1 concrete builder/sender call site |
| [056 / 0x38](client/056-0x38-refresh.md) | `CRefreshPacket` | `Refresh` | 1 concrete builder/sender call site |
| [057 / 0x39](client/057-0x39-merchant.md) | `CMerchantPacket` | `DialogMenuChoice` | 16 concrete builder/sender call sites |
| [058 / 0x3a](client/058-0x3a-pursuit.md) | `CPursuitPacket` | `DialogChoice` | 22 concrete builder/sender call sites |
| [059 / 0x3b](client/059-0x3b-bulletin.md) | `CBulletinPacket` | `BoardAction` | 15 concrete builder/sender call sites |
| [062 / 0x3e](client/062-0x3e-use-skill.md) | `CUseSkillPacket` | `UseSkill` | 1 concrete builder/sender call site |
| [063 / 0x3f](client/063-0x3f-field-map.md) | `CFieldMapPacket?` | `FieldMap / WorldMapClick` | 2 concrete builder/sender call sites |
| [065 / 0x41](client/065-0x41-get-parcel.md) | `CGetParcelPacket?` | `GetParcel / DismissParcel` | user-researched local command; fixed builder call site not yet isolated |
| [066 / 0x42](client/066-0x42-exception.md) | `CExceptionPacket` | `Exception` | 2 concrete builder/sender call sites |
| [067 / 0x43](client/067-0x43-object-info-request.md) | `CObjectInfoRequestPacket` | `Interact` | 5 concrete builder/sender call sites |
| [068 / 0x44](client/068-0x44-remove-equipment.md) | `CRemoveEquipmentPacket` | `UnequipItem` | 3 concrete builder/sender call sites |
| [069 / 0x45](client/069-0x45-reply-crc.md) | `CReplyCRCPacket` | `Heartbeat / CRC challenge reply` | 1 concrete builder/sender call site |
| [071 / 0x47](client/071-0x47-add-stat.md) | `CAddStatPacket?` | `AddStat / RaiseStat` | 1 concrete builder/sender call site |
| [072 / 0x48](client/072-0x48-patch.md) | `CPatchPacket` | `Patch` | explicit branch in `net_send_client_packet`; concrete builder not yet isolated |
| [074 / 0x4a](client/074-0x4a-exchange.md) | `CExchangePacket` | `ExchangeAction` | 7 concrete builder/sender call sites |
| [075 / 0x4b](client/075-0x4b-stipulation.md) | `CStipulationPacket` | `RequestLoginNotice` | 2 concrete builder/sender call sites |
| [077 / 0x4d](client/077-0x4d-spell-delay-request.md) | `CSpellDelayRequestPacket?` | `SpellDelayRequest / BeginSpellCast` | 1 concrete builder/sender call site |
| [078 / 0x4e](client/078-0x4e-spell-delay-say.md) | `CSpellDelaySayPacket?` | `SpellDelaySay / SpellChant` | 3 concrete builder/sender call sites |
| [079 / 0x4f](client/079-0x4f-send-portrait.md) | `CSendPortraitPacket?` | `SendPortrait / UserPortrait` | 1 concrete builder/sender call site |
| [084 / 0x54](client/084-0x54-merc.md) | `CMercPacket` | `Mercenary dialog` | 6 concrete builder/sender call sites |
| [085 / 0x55](client/085-0x55-black-smith.md) | `CBlackSmithPacket` | `Manufacture` | 2 concrete builder/sender call sites |
| [086 / 0x56](client/086-0x56-human-info-request.md) | `CHumanInfoRequestPacket` | `RequestUserId` | user-researched local command; fixed builder call site not yet isolated |
| [087 / 0x57](client/087-0x57-multi-server.md) | `CMultiServerPacket` | `RequestServerTable` | 2 concrete builder/sender call sites |
| [098 / 0x62](client/098-0x62-request-sequence.md) | `CRequestSequencePacket?` | `Client codename ("baram") / RequestSequence?` | concrete pre-version builder in `sub_579090`; complete body spells `"baram"` |
| [104 / 0x68](client/104-0x68-request-homepage.md) | `CRequestHomepagePacket?` | `RequestHomepage` | 1 concrete builder/sender call site |
| [106 / 0x6a](client/106-0x6a-mini-game.md) | `CMiniGamePacket` | `MiniGame` | 4 concrete builder/sender call sites |
| [108 / 0x6c](client/108-0x6c-item-shop.md) | `CItemShopPacket` | `ItemShop` | 3 concrete builder/sender call sites |
| [113 / 0x71](client/113-0x71-alive.md) | `CAlivePacket` | `Alive` | 1 concrete builder/sender call site |
| [115 / 0x73](client/115-0x73-web-board.md) | `CWebBoardPacket` | `WebBoard` | 2 concrete builder/sender call sites |
| [117 / 0x75](client/117-0x75-check-time.md) | `CCheckTimePacket?` | `CheckTime / SyncTicks` | 1 concrete builder/sender call site |
| [121 / 0x79](client/121-0x79-user-change-state.md) | `CUserChangeStatePacket?` | `UserChangeState / SetStatus` | 1 concrete builder/sender call site |
| [122 / 0x7a](client/122-0x7a-request-family-name.md) | `CRequestFamilyNamePacket?` | `RequestFamilyName / RequestFamilyList` | 1 concrete builder/sender call site |
| [123 / 0x7b](client/123-0x7b-meta-data.md) | `CMetaDataPacket` | `RequestMetadata` | 2 concrete builder/sender call sites |

# Client-to-server packet master list

This client assembles outgoing packets inline and submits them through `net_submit_client_packet` at `0x563E00`; `net_send_client_packet` at `0x5648A0` applies opcode-dependent transformation and the `0xAA + u16be size` frame.

Names follow this evidence order:

1. This client's binary and runtime behavior are the source of truth for the local opcode and payload.
2. Leaked registered `CPacket` templates provide exact company/engine class vocabulary where the semantic match holds.
3. User-provided related-engine terminology helps where the leaked class list moved or renamed a feature.
4. Behavioral aliases are retained as navigation aids and are not treated as internal class names.

A trailing `?` means the C++ class spelling is reconstructed rather than recovered from a registered class list. A related-game enum symbol can still be strong terminology evidence even when the synthesized `C...` spelling retains `?`.

Concrete display names omit the redundant class suffix. For example, the version template is written as `CVersion`. The generic term `CPacket` still means any client-to-server packet.

The index contains **60 opcodes with concrete builder call sites**, **1 send-policy-only opcode** (`0x48`), and **5 additional locally researched candidates** (`0x09`, `0x0A`, `0x1A`, `0x41`, and `0x56`): **66 local CPacket candidates total**. Future-only opcodes from the related game are not added without local evidence. The `0xFF` enum value is an unknown/sentinel value, not counted as a confirmed packet.

The related-game outgoing enum includes `0x01 ClientSize`, which may belong to its lobby flow. No fixed `0x01` builder, special send-policy branch, or current-client capture has been recovered here, so it remains comparison-only rather than becoming a 67th local candidate.

Filenames begin with a zero-padded decimal opcode, followed by the hexadecimal opcode, so ordinary filesystem sorting remains numeric.

| Opcode | Name | Related-game enum | Local behavioral alias | Naming basis | Evidence | Send handling |
|---:|---|---|---|---|---|---|
| [000 / 0x00](./000-0x00-version.md) | Version (`CVersion`) | `Version` | `Version` | leaked class + local confirmation | concrete builder in `sub_579090`; version `741` | no common encryption transform |
| [002 / 0x02](./002-0x02-new-user.md) | New User (`CNewUser`) | `NewUser` | `CreateCharacterName` | leaked class + local confirmation | 1 concrete builder/sender call site | common transform mode 0 |
| [003 / 0x03](./003-0x03-login.md) | Login (`CLogin`) | `UserTile` | `Login` | leaked class, locally remapped | 1 concrete builder/sender call site | common transform mode 0 |
| [004 / 0x04](./004-0x04-new-user-info.md) | New User Info (`CNewUserInfo`) | `Login` | `CreateCharacterAppearance` | leaked class, locally remapped | 1 concrete builder/sender call site | common transform mode 0 |
| [005 / 0x05](./005-0x05-map-crc.md) | Map CRC (`CMapCRC`) | `MapRequest` | `RequestMapData` | leaked class, locally remapped | 1 concrete builder/sender call site | default common transform mode 1 |
| [006 / 0x06](./006-0x06-move.md) | Move (`CMove`) | `Move` | `Walk` | leaked class, locally remapped | 1 concrete builder/sender call site | default common transform mode 1 |
| [007 / 0x07](./007-0x07-get.md) | Get (`CGet`) | `Get` | `PickupItem` | leaked class + local confirmation | 2 concrete builder/sender call sites | default common transform mode 1 |
| [008 / 0x08](./008-0x08-drop.md) | Drop (`CDrop`) | `Drop` | `DropItem` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [009 / 0x09](./009-0x09-look.md) | Look (`CLook?`) | `Look` | `Look / LookAhead` | related-game enum candidate | user-researched local command; fixed builder call site not yet isolated | not yet recovered from a concrete builder |
| [010 / 0x0a](./010-0x0a-far-look.md) | Far Look (`CFarLook?`) | `FarLook` | `FarLook / LookTile` | related-game enum candidate | user-researched local command; fixed builder call site not yet isolated | not yet recovered from a concrete builder |
| [011 / 0x0b](./011-0x0b-quit.md) | Quit (`CQuit`) | `Quit` | `RequestExit` | leaked class + local confirmation | 3 concrete builder/sender call sites | common transform mode 0 |
| [012 / 0x0c](./012-0x0c-put-request.md) | Put Request (`CPutRequest`) | `PutGround` | `RequestEntity` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [013 / 0x0d](./013-0x0d-block-listen.md) | Block Listen (`CBlockListen?`) | `BlockListen` | `BlockListen / IgnoreUser` | related-game enum + local evidence | 3 concrete builder/sender call sites | default common transform mode 1 |
| [014 / 0x0e](./014-0x0e-say.md) | Say (`CSay`) | `Say` | `Say` | leaked class + local confirmation | 5 concrete builder/sender call sites | default common transform mode 1 |
| [015 / 0x0f](./015-0x0f-use-spell.md) | Use Spell (`CUseSpell`) | `UseSpell` | `CastSpell` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [016 / 0x10](./016-0x10-transfer-server.md) | Transfer Server (`CTransferServer`) | `TransferServer` | `Authenticate` | leaked class + local confirmation | 2 concrete builder/sender call sites | no common encryption transform |
| [017 / 0x11](./017-0x11-change-dir.md) | Change Dir (`CChangeDir`) | `ChangeDirection` | `Turn` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [019 / 0x13](./019-0x13-attack.md) | Attack (`CAttack`) | `Attack` | `Assail` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [024 / 0x18](./024-0x18-who.md) | Who (`CWho`) | `Who` | `RequestWorldList` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [025 / 0x19](./025-0x19-tell.md) | Tell (`CTell`) | `` | `Whisper` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [026 / 0x1a](./026-0x1a-eat-item.md) | Eat Item (`CEatItem?`) | `` | `EatItem` | local internal-style inference | user-researched local command; fixed builder call site not yet isolated | not yet recovered from a concrete builder |
| [027 / 0x1b](./027-0x1b-user-status.md) | User Status (`CUserStatus`) | `` | `ToggleSetting` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [028 / 0x1c](./028-0x1c-use.md) | Use (`CUse`) | `Use` | `UseItem` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [029 / 0x1d](./029-0x1d-emotion.md) | Emotion (`CEmotion`) | `Emotion` | `Emote` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [035 / 0x23](./035-0x23-exit-editing-mode.md) | Exit Editing Mode (`CExitEditingMode?`) | `ExitEditingMode` | `ExitEditingMode / EditNotepad (Paper)` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [036 / 0x24](./036-0x24-drop-gold.md) | Drop Gold (`CDropGold?`) | `DropGold` | `DropGold` | local internal-style inference | 1 concrete builder/sender call site | default common transform mode 1 |
| [038 / 0x26](./038-0x26-change-password.md) | Change Password (`CChangePassword`) | `ChangePassword` | `ChangePassword` | leaked class + local confirmation | 2 concrete builder/sender call sites | common transform mode 0 |
| [041 / 0x29](./041-0x29-give.md) | Give (`CGive?`) | `Give` | `Give / GiveItem` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [042 / 0x2a](./042-0x2a-give-gold.md) | Give Gold (`CGiveGold?`) | `GiveGold` | `GiveGold` | local internal-style inference | 1 concrete builder/sender call site | default common transform mode 1 |
| [045 / 0x2d](./045-0x2d-self-look.md) | Self Look (`CSelfLook`) | `SelfLook` | `RequestProfile` | leaked class + local confirmation | 4 concrete builder/sender call sites | common transform mode 0 |
| [046 / 0x2e](./046-0x2e-party.md) | Party (`CParty`) | `Group` | `GroupInvite` | leaked class + local confirmation | 10 concrete builder/sender call sites | default common transform mode 1 |
| [047 / 0x2f](./047-0x2f-group-toggle.md) | Group Toggle (`CGroupToggle?`) | `GroupToggle` | `GroupToggle / ToggleGroup` | related-game enum + local evidence | 3 concrete builder/sender call sites | default common transform mode 1 |
| [048 / 0x30](./048-0x30-change-slot.md) | Change Slot (`CChangeSlot`) | `ChangeSlot` | `SwapSlot` | leaked class + local confirmation | 3 concrete builder/sender call sites | default common transform mode 1 |
| [049 / 0x31](./049-0x31-user-confirm.md) | User Confirm (`CUserConfirm`) | `Confirm` | `ConfirmUser` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [056 / 0x38](./056-0x38-refresh.md) | Refresh (`CRefresh`) | `RefreshUser` | `Refresh` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [057 / 0x39](./057-0x39-merchant.md) | Merchant (`CMerchant`) | `MenuCode` | `DialogMenuChoice` | leaked class + local confirmation | 16 concrete builder/sender call sites | default common transform mode 1 |
| [058 / 0x3a](./058-0x3a-pursuit.md) | Pursuit (`CPursuit`) | `Message` | `DialogChoice` | leaked class + local confirmation | 22 concrete builder/sender call sites | common transform mode 0 |
| [059 / 0x3b](./059-0x3b-bulletin.md) | Bulletin (`CBulletin`) | `Bulletin` | `BoardAction` | leaked class + local confirmation | 15 concrete builder/sender call sites | default common transform mode 1 |
| [062 / 0x3e](./062-0x3e-use-skill.md) | Use Skill (`CUseSkill`) | `UseSkill` | `UseSkill` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [063 / 0x3f](./063-0x3f-field-map.md) | Field Map (`CFieldMap?`) | `FieldMap` | `FieldMap / WorldMapClick` | related-game enum + local evidence | 2 concrete builder/sender call sites | default common transform mode 1 |
| [065 / 0x41](./065-0x41-get-parcel.md) | Get Parcel (`CGetParcel?`) | `GetParcel` | `GetParcel / DismissParcel` | related-game enum candidate | user-researched local command; fixed builder call site not yet isolated | not yet recovered from a concrete builder |
| [066 / 0x42](./066-0x42-exception.md) | Exception (`CException`) | `Exception` | `Exception` | leaked class + local confirmation | 2 concrete builder/sender call sites | common transform mode 0 |
| [067 / 0x43](./067-0x43-object-info-request.md) | Object Info Request (`CObjectInfoRequest`) | `RequestBubbleInfo` | `Interact` | leaked class + local confirmation | 5 concrete builder/sender call sites | common transform mode 0 |
| [068 / 0x44](./068-0x44-remove-equipment.md) | Remove Equipment (`CRemoveEquipment`) | `RemoveEquip` | `UnequipItem` | leaked class + local confirmation | 3 concrete builder/sender call sites | default common transform mode 1 |
| [069 / 0x45](./069-0x45-reply-crc.md) | Reply CRC (`CReplyCRC`) | `ReplyCRC` | `Heartbeat / CRC challenge reply` | leaked class + local confirmation | 1 concrete builder/sender call site | default common transform mode 1 |
| [071 / 0x47](./071-0x47-add-stat.md) | Add Stat (`CAddStat?`) | `AddStat` | `AddStat / RaiseStat` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [072 / 0x48](./072-0x48-patch.md) | Patch (`CPatch`) | `RequestPatch` | `Patch` | leaked class + local confirmation | explicit branch in `net_send_client_packet`; concrete builder not yet isolated | no common encryption transform |
| [074 / 0x4a](./074-0x4a-exchange.md) | Exchange (`CExchange`) | `Exchange` | `ExchangeAction` | leaked class + local confirmation | 7 concrete builder/sender call sites | default common transform mode 1 |
| [075 / 0x4b](./075-0x4b-stipulation.md) | Stipulation (`CStipulation`) | `Stipulation` | `RequestLoginNotice` | leaked class + local confirmation | 2 concrete builder/sender call sites | common transform mode 0 |
| [077 / 0x4d](./077-0x4d-spell-delay-request.md) | Spell Delay Request (`CSpellDelayRequest?`) | `SpellDelayRequest` | `SpellDelayRequest / BeginSpellCast` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [078 / 0x4e](./078-0x4e-spell-delay-say.md) | Spell Delay Say (`CSpellDelaySay?`) | `SpellDelaySay` | `SpellDelaySay / SpellChant` | related-game enum + local evidence | 3 concrete builder/sender call sites | default common transform mode 1 |
| [079 / 0x4f](./079-0x4f-send-portrait.md) | Send Portrait (`CSendPortrait?`) | `SendPortrait` | `SendPortrait / UserPortrait` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [084 / 0x54](./084-0x54-merc.md) | Merc (`CMerc`) | `Mercenary` | `Mercenary dialog` | leaked class + local confirmation | 6 concrete builder/sender call sites | default common transform mode 1 |
| [085 / 0x55](./085-0x55-black-smith.md) | Black Smith (`CBlackSmith`) | `Manual` | `Manufacture` | leaked class + local confirmation | 2 concrete builder/sender call sites | default common transform mode 1 |
| [086 / 0x56](./086-0x56-human-info-request.md) | Human Info Request (`CHumanInfoRequest`) | `` | `RequestUserId` | leaked class, locally remapped | user-researched local command; fixed builder call site not yet isolated | not yet recovered from a concrete builder |
| [087 / 0x57](./087-0x57-multi-server.md) | Multi Server (`CMultiServer`) | `Multi` | `RequestServerTable` | leaked class + local confirmation | 2 concrete builder/sender call sites | common transform mode 0 |
| [098 / 0x62](./098-0x62-request-sequence.md) | Request Sequence (`CRequestSequence?`) | `` | `Client codename ("baram") / RequestSequence?` | local internal-style inference + user tribal knowledge | concrete pre-version builder in `sub_579090`; complete body spells `"baram"` | common transform mode 0; consumes rolling sequence |
| [104 / 0x68](./104-0x68-request-homepage.md) | Request Homepage (`CRequestHomepage?`) | `SlotScroll` | `RequestHomepage` | local internal-style inference | 1 concrete builder/sender call site | common transform mode 0 |
| [106 / 0x6a](./106-0x6a-mini-game.md) | Mini Game (`CMiniGame`) | `MiniGame` | `MiniGame` | leaked class + local confirmation | 4 concrete builder/sender call sites | default common transform mode 1 |
| [108 / 0x6c](./108-0x6c-item-shop.md) | Item Shop (`CItemShop`) | `CashShop` | `ItemShop` | leaked class + local confirmation | 3 concrete builder/sender call sites | default common transform mode 1 |
| [113 / 0x71](./113-0x71-alive.md) | Alive (`CAlive`) | `SendAlive` | `Alive` | leaked class + local confirmation | 1 concrete builder/sender call site | common transform mode 0 |
| [115 / 0x73](./115-0x73-web-board.md) | Web Board (`CWebBoard`) | `WebBoard` | `WebBoard` | leaked class + local confirmation | 2 concrete builder/sender call sites | common transform mode 0 |
| [117 / 0x75](./117-0x75-check-time.md) | Check Time (`CCheckTime?`) | `CheckTime` | `CheckTime / SyncTicks` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [121 / 0x79](./121-0x79-user-change-state.md) | User Change State (`CUserChangeState?`) | `UserChangeState` | `UserChangeState / SetStatus` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [122 / 0x7a](./122-0x7a-request-family-name.md) | Request Family Name (`CRequestFamilyName?`) | `RequestLoverName` | `RequestFamilyName / RequestFamilyList` | related-game enum + local evidence | 1 concrete builder/sender call site | default common transform mode 1 |
| [123 / 0x7b](./123-0x7b-meta-data.md) | Meta Data (`CMetaData`) | `MetaData` | `RequestMetadata` | leaked class + local confirmation | 2 concrete builder/sender call sites | common transform mode 0 |

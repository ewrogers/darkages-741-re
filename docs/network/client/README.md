# Client-to-server packet index

The client builds outbound packets inline and submits opcode-first bodies through `net_submit_client_packet` at `0x00563E00`. There are no derived client packet RTTI classes.

This initial index contains 61 locally evidenced opcodes: 60 with a concrete builder call site and `0x48` from the explicit raw send-policy branch. The executable does not expose client packet RTTI, so internal names record project-owner protocol knowledge or cautious reconstructions matched against local behavior. A trailing `?` means the spelling remains uncertain. Descriptive aliases are recorded on individual pages when they differ from the internal name.

Each packet page lists every direct static call to its representative builder. A listed RTTI owner is exact compiler evidence. “Reachable from” means the owner was found by following callers and may enqueue or route the action rather than call the builder directly. “Owner not yet identified” means the direct call address is known but no reliable pane or subsystem owner has been recovered yet. Indirect runtime calls can still exist beyond these static cross-references.

Transform names link to [Packet transforms](../packet-transforms.md). Payload fields remain intentionally incomplete until they are recovered from the target.

| Opcode | Name | Transform | Representative local evidence |
| ---: | --- | --- | --- |
| [000 / 0x00](000-0x00-version.md) | Version (`CVersion`) | raw | `0x00579090` |
| [002 / 0x02](002-0x02-new-user.md) | New User (`CNewUser`) | static | `0x0043D820` |
| [003 / 0x03](003-0x03-login.md) | Login (`CLogin`) | static | `0x004BAA80` |
| [004 / 0x04](004-0x04-new-user-appearance.md) | New User Appearance (`CNewUserAppearance`) | static | `0x0043E8F0` |
| [005 / 0x05](005-0x05-map-request.md) | Map Request (`CMapRequest`) | derived | `0x005F1BF0` |
| [006 / 0x06](006-0x06-move.md) | Move (`CMove`) | derived | `0x005F4580` |
| [007 / 0x07](007-0x07-get.md) | Get (`CGet`) | derived | `0x00498550` |
| [008 / 0x08](008-0x08-drop.md) | Drop (`CDrop`) | derived | `0x00496C90` |
| [011 / 0x0b](011-0x0b-quit.md) | Quit (`CQuit`) | static | `0x004B79C0` |
| [012 / 0x0c](012-0x0c-put-ground.md) | Put Ground (`CPutGround`) | derived | `0x005F4430` |
| [013 / 0x0d](013-0x0d-block-listen.md) | Block Listen (`CBlockListen?`) | derived | `0x00550AA0` |
| [014 / 0x0e](014-0x0e-say.md) | Say (`CSay`) | derived | `0x0054FD90` |
| [015 / 0x0f](015-0x0f-use-spell.md) | Use Spell (`CUseSpell`) | derived | `0x00428690` |
| [016 / 0x10](016-0x10-transfer-server.md) | Transfer Server (`CTransferServer`) | raw | `0x004B9510` |
| [017 / 0x11](017-0x11-change-direction.md) | Change Direction (`CChangeDirection`) | derived | `0x005F4510` |
| [019 / 0x13](019-0x13-attack.md) | Attack (`CAttack`) | derived | `0x005F44B0` |
| [024 / 0x18](024-0x18-who.md) | Who (`CWho`) | derived | `0x0059D7D0` |
| [025 / 0x19](025-0x19-tell.md) | Tell (`CTell`) | derived | `0x00550590` |
| [027 / 0x1b](027-0x1b-user-setting.md) | User Setting (`CUserSetting`) | derived | `0x00542E60` |
| [028 / 0x1c](028-0x1c-use.md) | Use (`CUse`) | derived | `0x00496E90` |
| [029 / 0x1d](029-0x1d-emotion.md) | Emotion (`CEmotion`) | derived | `0x005F46C0` |
| [035 / 0x23](035-0x23-exit-editing-mode.md) | Exit Editing Mode (`CExitEditingMode?`) | derived | `0x0054A7D0` |
| [036 / 0x24](036-0x24-drop-gold.md) | Drop Gold (`CDropGold?`) | derived | `0x004975C0` |
| [038 / 0x26](038-0x26-change-password.md) | Change Password (`CChangePassword`) | static | `0x004BC050` |
| [041 / 0x29](041-0x29-give.md) | Give (`CGive?`) | derived | `0x00496D90` |
| [042 / 0x2a](042-0x2a-give-gold.md) | Give Gold (`CGiveGold?`) | derived | `0x00497B10` |
| [045 / 0x2d](045-0x2d-self-look.md) | Self Look (`CSelfLook`) | static | `0x0041B840` |
| [046 / 0x2e](046-0x2e-group.md) | Group (`CGroup`) | derived | `0x00462DC0` |
| [047 / 0x2f](047-0x2f-group-toggle.md) | Group Toggle (`CGroupToggle?`) | derived | `0x0041B8E0` |
| [048 / 0x30](048-0x30-change-slot.md) | Change Slot (`CChangeSlot`) | derived | `0x00490F40` |
| [049 / 0x31](049-0x31-confirm.md) | Confirm (`CConfirm`) | derived | `0x005922A0` |
| [056 / 0x38](056-0x38-refresh-user.md) | Refresh User (`CRefreshUser`) | derived | `0x005F4640` |
| [057 / 0x39](057-0x39-merchant.md) | Merchant (`CMenuCode`) | derived | `0x004CFE60` |
| [058 / 0x3a](058-0x3a-pursuit.md) | Pursuit (`CMessage`) | static | `0x004DBC90` |
| [059 / 0x3b](059-0x3b-bulletin.md) | Bulletin (`CBulletin`) | derived | `0x0041CBC0` |
| [062 / 0x3e](062-0x3e-use-skill.md) | Use Skill (`CUseSkill`) | derived | `0x00499420` |
| [063 / 0x3f](063-0x3f-field-map.md) | Field Map (`CFieldMap?`) | derived | `0x00430D30` |
| [066 / 0x42](066-0x42-exception.md) | Exception (`CException`) | static | `0x00468B40` |
| [067 / 0x43](067-0x43-request-object-info.md) | Request Object Info (`CRequestObjectInfo`) | static | `0x004CD350` |
| [068 / 0x44](068-0x44-remove-equipment.md) | Remove Equipment (`CRemoveEquipment`) | derived | `0x00460330` |
| [069 / 0x45](069-0x45-reply-crc.md) | Reply CRC (`CReplyCRC`) | derived | `0x005F2CF0` |
| [071 / 0x47](071-0x47-add-stat.md) | Add Stat (`CAddStat?`) | derived | `0x005755C0` |
| [072 / 0x48](072-0x48-request-patch.md) | Request Patch (`CRequestPatch`) | raw | send-policy branch at `0x0056492A` |
| [074 / 0x4a](074-0x4a-exchange.md) | Exchange (`CExchange`) | derived | `0x0046A390` |
| [075 / 0x4b](075-0x4b-stipulation.md) | Stipulation (`CStipulation`) | static | `0x004B8570` |
| [077 / 0x4d](077-0x4d-spell-delay-request.md) | Spell Delay Request (`CSpellDelayRequest?`) | derived | `0x0049BAB0` |
| [078 / 0x4e](078-0x4e-spell-delay-say.md) | Spell Delay Say (`CSpellDelaySay?`) | derived | `0x00499330` |
| [079 / 0x4f](079-0x4f-send-portrait.md) | Send Portrait (`CSendPortrait?`) | derived | `0x005B1160` |
| [084 / 0x54](084-0x54-mercenary.md) | Mercenary (`CMercenary`) | derived | `0x0045C500` |
| [085 / 0x55](085-0x55-manual.md) | Manual (`CManual`) | derived | `0x004C26D0` |
| [087 / 0x57](087-0x57-multi-server.md) | Multi Server (`CMulti`) | static | `0x0055A090` |
| [098 / 0x62](098-0x62-baram.md) | Baram (`CBaram`) | static | literal body at `0x00579832` |
| [104 / 0x68](104-0x68-request-homepage.md) | Request Homepage (`CRequestHomepage?`) | static | `0x004BA0C0` |
| [106 / 0x6a](106-0x6a-mini-game.md) | Mini Game (`CMiniGame`) | derived | `0x0050C600` |
| [108 / 0x6c](108-0x6c-cash-shop.md) | Cash Shop (`CCashShop`) | derived | `0x004A03B0` |
| [113 / 0x71](113-0x71-send-alive.md) | Send Alive (`CSendAlive`) | static | `0x004BA010` |
| [115 / 0x73](115-0x73-web-board.md) | Web Board (`CWebBoard`) | static | `0x004160A0` |
| [117 / 0x75](117-0x75-check-time.md) | Check Time (`CCheckTime`) | derived | `0x005F7830` |
| [121 / 0x79](121-0x79-user-change-state.md) | User Change State (`CUserChangeState?`) | derived | `0x005FC790` |
| [122 / 0x7a](122-0x7a-request-family-name.md) | Request Family Name (`CRequestFamilyName`) | derived | `0x004719B0` |
| [123 / 0x7b](123-0x7b-meta-data.md) | Meta Data (`CMetaData`) | static | `0x004E52F0` |

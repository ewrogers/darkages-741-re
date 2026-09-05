# Server packets

These messages travel from the server to the game client.

Most concrete names come directly from RTTI and the server packet factory. A decoded network event also retains the opcode-first body beside its optional packet object, so panes and managers can handle a message without a factory class.

## Raw event coverage

The raw-event audit checked every target-client function that reads the decoded body field and every direct comparison of its first byte. It found no additional server opcode beyond the packet index below.

| Route | Opcodes | Result |
| --- | --- | --- |
| No factory class, handled from the decoded body | `0x00`, `0x01`, `0x02`, `0x1B`, `0x31`, `0x34`, `0x35`, `0x36`, `0x4F`, `0x6F` | Lobby panes, the world dispatcher, bulletin panes, `GUIBackPane`, `EmployeeDialogPane`, or the metadata manager own the behavior. |
| No factory class and no decoded-body consumer | `0x1E`, `0x40`, `0x58`, `0x67` | The body remains available in the event, but no pane or manager acts on it. `0x40` has only a transport-policy entry. |
| Factory-backed, but also watched or reparsed as raw body bytes | `0x06`, `0x2E`, `0x2F`, `0x30`, `0x3B`, `0x3C`, `0x42`, `0x63` | These remain the RTTI-backed packet named on their pages. The raw route is an additional consumer, not a second packet schema. |
| Initial raw receive before decoded-body events | `0x7E` | `TerminalPane2` recognizes the startup control in the complete received bytes. |

The central world dispatcher owns the factory-less `0x1B`, `0x31`, `0x34`, `0x35`, `0x36`, and `0x4F` routes. Their handlers open editing, bulletin, object-information, paper, user-list, and employee UI. The other direct consumers are state-specific. For example, the creation pane accepts raw `0x30` as a no-op, while `DescPane` closes when it sees raw `0x42` or `0x63` without reading either packet body.

Body schemas use the shared [packet body notation](../packet-body-notation.md). All multibyte packet integers are big-endian. Reused enum and bit-flag values live in [Shared protocol types](../protocol-types.md).

| Packet | Transform |
| --- | --- |
| [0x00 - Version Check (`SVersionCheck`)](000-0x00-version-check.md) | `raw` |
| [0x01 - New User Check Alias (`SNewUserCheck`)](001-0x01-new-user-check.md) | `static` |
| [0x02 - Lobby Account Result (`SLoginCheck` / `SNewUserCheck`)](002-0x02-login-check.md) | `static` |
| [0x03 - Transfer Server (`STransferServer`)](003-0x03-transfer-server.md) | `raw` |
| [0x04 - User Position (`SUserPosition`)](004-0x04-user-position.md) | `derived` |
| [0x05 - User Appearance (`SUserAppearance`)](005-0x05-user-appearance.md) | `derived` |
| [0x06 - Map (`SMap`)](006-0x06-map.md) | `derived` |
| [0x07 - Draw Objects (`SDrawObjects`)](007-0x07-draw-objects.md) | `derived` |
| [0x08 - Status (`SStatus`)](008-0x08-status.md) | `derived` |
| [0x0A - Message (`SMessage`)](010-0x0a-message.md) | `static` |
| [0x0B - Move (`SMove`)](011-0x0b-move.md) | `derived` |
| [0x0C - Move Object (`SMoveObject`)](012-0x0c-move-object.md) | `derived` |
| [0x0D - Say (`SSay`)](013-0x0d-say.md) | `derived` |
| [0x0E - Remove Objects (`SRemoveObjects`)](014-0x0e-remove-objects.md) | `derived` |
| [0x0F - Add Inventory (`SAddInventory`)](015-0x0f-add-inventory.md) | `derived` |
| [0x10 - Remove Inventory (`SRemoveInventory`)](016-0x10-remove-inventory.md) | `derived` |
| [0x11 - Change Direction (`SChangeDirection`)](017-0x11-change-direction.md) | `derived` |
| [0x13 - Damage Effect (`SDamageEffect`)](019-0x13-damage-effect.md) | `derived` |
| [0x15 - Map Size (`SMapSize`)](021-0x15-map-size.md) | `derived` |
| [0x17 - Add Spell (`SAddSpell`)](023-0x17-add-spell.md) | `derived` |
| [0x18 - Remove Spell (`SRemoveSpell`)](024-0x18-remove-spell.md) | `derived` |
| [0x19 - Sound Effect (`SSoundEffect`)](025-0x19-sound-effect.md) | `derived` |
| [0x1A - Motion (`SMotion`)](026-0x1a-motion.md) | `derived` |
| [0x1B - Enter Editing Mode (`SEnterEditingMode`)](027-0x1b-enter-editing-mode.md) | `derived` |
| [0x1E - Change Day (`SChangeDay`)](030-0x1e-change-day.md) | `derived` |
| [0x1F - Change Weather (`SChangeWeather`)](031-0x1f-change-weather.md) | `derived` |
| [0x20 - Change Hour (`SChangeHour`)](032-0x20-change-hour.md) | `derived` |
| [0x21 - Self Save OK (`SSelfSaveOK`)](033-0x21-self-save-ok.md) | `derived` |
| [0x29 - Effect Layer (`SEffectLayer`)](041-0x29-effect-layer.md) | `derived` |
| [0x2C - Add Skill (`SAddSkill`)](044-0x2c-add-skill.md) | `derived` |
| [0x2D - Remove Skill (`SRemoveSkill`)](045-0x2d-remove-skill.md) | `derived` |
| [0x2E - Field Map (`SFieldMap`)](046-0x2e-field-map.md) | `derived` |
| [0x2F - Screen Menu (`SScreenMenu`)](047-0x2f-screen-menu.md) | `derived` |
| [0x30 - Pursuit Message (`SPursuitMessage`)](048-0x30-pursuit-message.md) | `derived` |
| [0x31 - Bulletin (`SBulletin`)](049-0x31-bulletin.md) | `derived` |
| [0x32 - Static Object State (`SStaticObjectState`)](050-0x32-static-object-state.md) | `derived` |
| [0x33 - Draw Human Objects (`SDrawHumanObjects`)](051-0x33-draw-human-objects.md) | `derived` |
| [0x34 - Object Info (`SObjectInfo`)](052-0x34-object-info.md) | `derived` |
| [0x35 - Show Paper (`SShowPaper`)](053-0x35-show-paper.md) | `derived` |
| [0x36 - Show Users (`SShowUsers`)](054-0x36-show-users.md) | `derived` |
| [0x37 - Add Equip (`SAddEquip`)](055-0x37-add-equip.md) | `derived` |
| [0x38 - Remove Equip (`SRemoveEquip`)](056-0x38-remove-equip.md) | `derived` |
| [0x39 - Self Look (`SSelfLook`)](057-0x39-self-look.md) | `derived` |
| [0x3A - Spelled (`SSpelled`)](058-0x3a-spelled.md) | `derived` |
| [0x3B - Request CRC (`SRequestCRC`)](059-0x3b-request-crc.md) | `derived` |
| [0x3C - Map Part (`SMapPart`)](060-0x3c-map-part.md) | `derived` |
| [0x3D - Level Point (`SLevelPoint`)](061-0x3d-level-point.md) | `derived` |
| [0x3E - Window Change (`SWindowChange`)](062-0x3e-window-change.md) | `derived` |
| [0x3F - Action Delay (`SActionDelay`)](063-0x3f-action-delay.md) | `derived` |
| [0x40 - Send Patch (`SSendPatch`)](064-0x40-send-patch.md) | `raw` |
| [0x42 - Exchange (`SExchange`)](066-0x42-exchange.md) | `derived` |
| [0x44 - Add User (`SAddUser`)](068-0x44-add-user.md) | `derived` |
| [0x45 - Item Shop (`SItemShop`)](069-0x45-item-shop.md) | `derived` |
| [0x47 - Num Users (`SNumUsers`)](071-0x47-num-users.md) | `derived` |
| [0x48 - Spell Delay Cancel (`SSpellDelayCancel`)](072-0x48-spell-delay-cancel.md) | `derived` |
| [0x49 - Request Portrait (`SRequestPortrait`)](073-0x49-request-portrait.md) | `derived` |
| [0x4A - Bad Guy (`SBadGuy`)](074-0x4a-bad-guy.md) | `derived` |
| [0x4B - Bounce (`SBounce`)](075-0x4b-bounce.md) | `derived` |
| [0x4C - Quit (`SQuit`)](076-0x4c-quit.md) | `derived` |
| [0x4F - Mercenary (`SMercenary`)](079-0x4f-mercenary.md) | `derived` |
| [0x50 - Manual (`SManual`)](080-0x50-manual.md) | `derived` |
| [0x51 - Block Input (`SBlockInput`)](081-0x51-block-input.md) | `derived` |
| [0x56 - Multi Server (`SMulti`)](086-0x56-multi.md) | `static` |
| [0x58 - Unhandled Control](088-0x58-unhandled-control.md) | `derived` |
| [0x5B - Advertisement (`SAdvertisement`)](091-0x5b-advertisement.md) | `derived` |
| [0x60 - Stipulation (`SStipulation`)](096-0x60-stipulation.md) | `static` |
| [0x62 - Web Board (`SWebBoard`)](098-0x62-web-board.md) | `static` |
| [0x63 - Group (`SGroup`)](099-0x63-group.md) | `derived` |
| [0x64 - Mini Game (`SMiniGame`)](100-0x64-mini-game.md) | `derived` |
| [0x66 - Browser (`SBrowser`)](102-0x66-browser.md) | `static` |
| [0x67 - Unhandled Field/Map Control](103-0x67-unhandled-field-map-control.md) | `derived` |
| [0x68 - Check Time (`SCheckTime`)](104-0x68-check-time.md) | `derived` |
| [0x6B - Town Map (`SScreenShot`)](107-0x6b-town-map.md) | `derived` |
| [0x6D - Family Name (`SFamilyName`)](109-0x6d-family-name.md) | `derived` |
| [0x6F - Meta Data (`SMetaData`)](111-0x6f-meta-data.md) | `static` |
| [0x7E - Hello (`SHello`)](126-0x7e-hello.md) | `raw` during the initial raw-stream receive mode |

Shared framing and encoding rules are in [Network transport](../transport.md) and [Packet transforms](../packet-transforms.md).

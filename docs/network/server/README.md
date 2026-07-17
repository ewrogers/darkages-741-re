# Server packets

These messages travel from the server to the game client.

Most concrete names come directly from RTTI and the server packet factory. A few early or manager-owned messages are handled as decoded byte buffers instead. Their pages explain that difference.

Body schemas use the shared [packet body notation](../packet-body-notation.md). All multibyte packet integers are big-endian. Reused enum and bit-flag values live in [Shared protocol types](../protocol-types.md).

| Packet | Encoding |
| --- | --- |
| [0x00 - Version Check (`SVersionCheck`)](000-0x00-version-check.md) | none |
| [0x01 - New User Check Alias (`SNewUserCheck`)](001-0x01-new-user-check.md) | startup key |
| [0x02 - Lobby Account Result (`SLoginCheck` / `SNewUserCheck`)](002-0x02-login-check.md) | startup key |
| [0x03 - Transfer Server (`STransferServer`)](003-0x03-transfer-server.md) | none |
| [0x04 - User Position (`SUserPosition`)](004-0x04-user-position.md) | session key |
| [0x05 - User Appearance (`SUserAppearance`)](005-0x05-user-appearance.md) | session key |
| [0x06 - Map (`SMap`)](006-0x06-map.md) | session key |
| [0x07 - Draw Objects (`SDrawObjects`)](007-0x07-draw-objects.md) | session key |
| [0x08 - Status (`SStatus`)](008-0x08-status.md) | session key |
| [0x0A - Message (`SMessage`)](010-0x0a-message.md) | startup key |
| [0x0B - Move (`SMove`)](011-0x0b-move.md) | session key |
| [0x0C - Move Object (`SMoveObject`)](012-0x0c-move-object.md) | session key |
| [0x0D - Say (`SSay`)](013-0x0d-say.md) | session key |
| [0x0E - Remove Objects (`SRemoveObjects`)](014-0x0e-remove-objects.md) | session key |
| [0x0F - Add Inventory (`SAddInventory`)](015-0x0f-add-inventory.md) | session key |
| [0x10 - Remove Inventory (`SRemoveInventory`)](016-0x10-remove-inventory.md) | session key |
| [0x11 - Change Direction (`SChangeDirection`)](017-0x11-change-direction.md) | session key |
| [0x13 - Damage Effect (`SDamageEffect`)](019-0x13-damage-effect.md) | session key |
| [0x15 - Map Size (`SMapSize`)](021-0x15-map-size.md) | session key |
| [0x17 - Add Spell (`SAddSpell`)](023-0x17-add-spell.md) | session key |
| [0x18 - Remove Spell (`SRemoveSpell`)](024-0x18-remove-spell.md) | session key |
| [0x19 - Sound Effect (`SSoundEffect`)](025-0x19-sound-effect.md) | session key |
| [0x1A - Motion (`SMotion`)](026-0x1a-motion.md) | session key |
| [0x1E - Change Day (`SChangeDay`)](030-0x1e-change-day.md) | session key |
| [0x1F - Change Weather (`SChangeWeather`)](031-0x1f-change-weather.md) | session key |
| [0x20 - Change Hour (`SChangeHour`)](032-0x20-change-hour.md) | session key |
| [0x21 - Self Save OK (`SSelfSaveOK`)](033-0x21-self-save-ok.md) | session key |
| [0x29 - Effect Layer (`SEffectLayer`)](041-0x29-effect-layer.md) | session key |
| [0x2C - Add Skill (`SAddSkill`)](044-0x2c-add-skill.md) | session key |
| [0x2D - Remove Skill (`SRemoveSkill`)](045-0x2d-remove-skill.md) | session key |
| [0x2E - Field Map (`SFieldMap`)](046-0x2e-field-map.md) | session key |
| [0x2F - Screen Menu (`SScreenMenu`)](047-0x2f-screen-menu.md) | session key |
| [0x30 - Pursuit Message (`SPursuitMessage`)](048-0x30-pursuit-message.md) | session key |
| [0x32 - Static Object State (`SStaticObjectState`)](050-0x32-static-object-state.md) | session key |
| [0x33 - Draw Human Objects (`SDrawHumanObjects`)](051-0x33-draw-human-objects.md) | session key |
| [0x37 - Add Equip (`SAddEquip`)](055-0x37-add-equip.md) | session key |
| [0x38 - Remove Equip (`SRemoveEquip`)](056-0x38-remove-equip.md) | session key |
| [0x39 - Self Look (`SSelfLook`)](057-0x39-self-look.md) | session key |
| [0x3A - Spelled (`SSpelled`)](058-0x3a-spelled.md) | session key |
| [0x3B - Request CRC (`SRequestCRC`)](059-0x3b-request-crc.md) | session key |
| [0x3C - Map Part (`SMapPart`)](060-0x3c-map-part.md) | session key |
| [0x3D - Level Point (`SLevelPoint`)](061-0x3d-level-point.md) | session key |
| [0x3E - Window Change (`SWindowChange`)](062-0x3e-window-change.md) | session key |
| [0x3F - Action Delay (`SActionDelay`)](063-0x3f-action-delay.md) | session key |
| [0x40 - Send Patch (`SSendPatch`)](064-0x40-send-patch.md) | none |
| [0x42 - Exchange (`SExchange`)](066-0x42-exchange.md) | session key |
| [0x44 - Add User (`SAddUser`)](068-0x44-add-user.md) | session key |
| [0x45 - Item Shop (`SItemShop`)](069-0x45-item-shop.md) | session key |
| [0x47 - Num Users (`SNumUsers`)](071-0x47-num-users.md) | session key |
| [0x48 - Spell Delay Cancel (`SSpellDelayCancel`)](072-0x48-spell-delay-cancel.md) | session key |
| [0x49 - Request Portrait (`SRequestPortrait`)](073-0x49-request-portrait.md) | session key |
| [0x4A - Bad Guy (`SBadGuy`)](074-0x4a-bad-guy.md) | session key |
| [0x4B - Bounce (`SBounce`)](075-0x4b-bounce.md) | session key |
| [0x4C - Quit (`SQuit`)](076-0x4c-quit.md) | session key |
| [0x50 - Manual (`SManual`)](080-0x50-manual.md) | session key |
| [0x51 - Block Input (`SBlockInput`)](081-0x51-block-input.md) | session key |
| [0x56 - Multi Server (`SMulti`)](086-0x56-multi.md) | startup key |
| [0x58 - Unhandled Control](088-0x58-unhandled-control.md) | session key |
| [0x5B - Advertisement (`SAdvertisement`)](091-0x5b-advertisement.md) | session key |
| [0x60 - Stipulation (`SStipulation`)](096-0x60-stipulation.md) | startup key |
| [0x62 - Web Board (`SWebBoard`)](098-0x62-web-board.md) | startup key |
| [0x63 - Group (`SGroup`)](099-0x63-group.md) | session key |
| [0x64 - Mini Game (`SMiniGame`)](100-0x64-mini-game.md) | session key |
| [0x66 - Browser (`SBrowser`)](102-0x66-browser.md) | startup key |
| [0x67 - Unhandled Map-Transfer Control](103-0x67-unhandled-map-transfer-control.md) | session key |
| [0x68 - Check Time (`SCheckTime`)](104-0x68-check-time.md) | session key |
| [0x6B - Screen Shot (`SScreenShot`)](107-0x6b-screen-shot.md) | session key |
| [0x6D - Family Name (`SFamilyName`)](109-0x6d-family-name.md) | session key |
| [0x6F - Meta Data (`SMetaData`)](111-0x6f-meta-data.md) | startup key |
| [0x7E - Hello (`SHello`)](126-0x7e-hello.md) | raw startup control |

Shared framing and encoding rules are in [Network transport](../transport.md) and [Packet transforms](../packet-transforms.md).

# Server-to-client packet index

`net_server_packet_factory_ctor` at `0x00595F00` registers 61 concrete server packet classes by opcode. Each registered constructor calls `net_server_packet_base_ctor` with the opcode and installs a class-specific RTTI-backed vtable.

Five additional opcodes have no registered RTTI packet class. `SVersionCheck`, `SNewUserCheck`, `SLoginCheck`, and `SMetaData` have confirmed out-of-factory handlers owned by RTTI-backed UI or manager classes. Project-owner protocol knowledge identifies opcode `0x40` as `SSendPatch`; its local parser is still unknown. Transform names link to [Packet transforms](../packet-transforms.md).

| Opcode | Name | Transform | Evidence |
| ---: | --- | --- | --- |
| [000 / 0x00](000-0x00-version-check.md) | Version Check (`SVersionCheck`) | raw | handler `0x004B7F80` |
| [001 / 0x01](001-0x01-new-user-check.md) | New User Check (`SNewUserCheck`) | static | handler `0x0043F820` |
| [002 / 0x02](002-0x02-login-check.md) | Login Check (`SLoginCheck`) | static | handler `0x004B8420` |
| [003 / 0x03](003-0x03-transfer-server.md) | Transfer Server (`STransferServer`) | raw | RTTI constructor `0x0059CA10` |
| [004 / 0x04](004-0x04-user-position.md) | User Position (`SUserPosition`) | derived | RTTI constructor `0x0059CCA0` |
| [005 / 0x05](005-0x05-user-appearance.md) | User Appearance (`SUserAppearance`) | derived | RTTI constructor `0x0059CB40` |
| [006 / 0x06](006-0x06-map.md) | Map (`SMap`) | derived | RTTI constructor `0x00599CE0` |
| [007 / 0x07](007-0x07-draw-objects.md) | Draw Objects (`SDrawObjects`) | derived | RTTI constructor `0x00598A40` |
| [008 / 0x08](008-0x08-status.md) | Status (`SStatus`) | derived | RTTI constructor `0x0059C3E0` |
| [010 / 0x0a](010-0x0a-message.md) | Message (`SMessage`) | static | RTTI constructor `0x0059A0D0` |
| [011 / 0x0b](011-0x0b-move.md) | Move (`SMove`) | derived | RTTI constructor `0x0059A520` |
| [012 / 0x0c](012-0x0c-move-object.md) | Move Object (`SMoveObject`) | derived | RTTI constructor `0x0059A680` |
| [013 / 0x0d](013-0x0d-say.md) | Say (`SSay`) | derived | RTTI constructor `0x0059B590` |
| [014 / 0x0e](014-0x0e-remove-objects.md) | Remove Objects (`SRemoveObjects`) | derived | RTTI constructor `0x0059B050` |
| [015 / 0x0f](015-0x0f-add-inventory.md) | Add Inventory (`SAddInventory`) | derived | RTTI constructor `0x00597400` |
| [016 / 0x10](016-0x10-remove-inventory.md) | Remove Inventory (`SRemoveInventory`) | derived | RTTI constructor `0x0059AF40` |
| [017 / 0x11](017-0x11-change-direction.md) | Change Direction (`SChangeDirection`) | derived | RTTI constructor `0x00597FB0` |
| [019 / 0x13](019-0x13-damage-effect.md) | Damage Effect (`SDamageEffect`) | derived | RTTI constructor `0x00598400` |
| [021 / 0x15](021-0x15-map-size.md) | Map Size (`SMapSize`) | derived | RTTI constructor `0x00599F60` |
| [023 / 0x17](023-0x17-add-spell.md) | Add Spell (`SAddSpell`) | derived | RTTI constructor `0x005976C0` |
| [024 / 0x18](024-0x18-remove-spell.md) | Remove Spell (`SRemoveSpell`) | derived | RTTI constructor `0x0059B270` |
| [025 / 0x19](025-0x19-sound-effect.md) | Sound Effect (`SSoundEffect`) | derived | RTTI constructor `0x0059BF00` |
| [026 / 0x1a](026-0x1a-motion.md) | Motion (`SMotion`) | derived | RTTI constructor `0x0059A3F0` |
| [031 / 0x1f](031-0x1f-change-weather.md) | Change Weather (`SChangeWeather`) | derived | RTTI constructor `0x005981E0` |
| [032 / 0x20](032-0x20-change-hour.md) | Change Hour (`SChangeHour`) | derived | RTTI constructor `0x005980D0` |
| [033 / 0x21](033-0x21-self-save-ok.md) | Self Save OK (`SSelfSaveOK`) | derived | RTTI constructor `0x0059BE00` |
| [041 / 0x29](041-0x29-effect-layer.md) | Effect Layer (`SEffectLayer`) | derived | RTTI constructor `0x00598DB0` |
| [044 / 0x2c](044-0x2c-add-skill.md) | Add Skill (`SAddSkill`) | derived | RTTI constructor `0x00597590` |
| [045 / 0x2d](045-0x2d-remove-skill.md) | Remove Skill (`SRemoveSkill`) | derived | RTTI constructor `0x0059B160` |
| [046 / 0x2e](046-0x2e-field-map.md) | Field Map (`SFieldMap`) | derived | RTTI constructor `0x00599290` |
| [047 / 0x2f](047-0x2f-screen-menu.md) | Screen Menu (`SScreenMenu`) | derived | RTTI constructor `0x0059B6C0` |
| [048 / 0x30](048-0x30-pursuit-message.md) | Pursuit Message (`SPursuitMessage`) | derived | RTTI constructor `0x0059AA00` |
| [050 / 0x32](050-0x32-static-object-state.md) | Static Object State (`SStaticObjectState`) | derived | RTTI constructor `0x0059C260` |
| [051 / 0x33](051-0x33-draw-human-objects.md) | Draw Human Objects (`SDrawHumanObjects`) | derived | RTTI constructor `0x00598540` |
| [055 / 0x37](055-0x37-add-equip.md) | Add Equip (`SAddEquip`) | derived | RTTI constructor `0x00597290` |
| [056 / 0x38](056-0x38-remove-equip.md) | Remove Equip (`SRemoveEquip`) | derived | RTTI constructor `0x0059AE30` |
| [057 / 0x39](057-0x39-self-look.md) | Self Look (`SSelfLook`) | derived | RTTI constructor `0x0059BA40` |
| [058 / 0x3a](058-0x3a-spelled.md) | Spelled (`SSpelled`) | derived | RTTI constructor `0x0059C140` |
| [059 / 0x3b](059-0x3b-request-crc.md) | Request CRC (`SRequestCRC`) | derived | RTTI constructor `0x0059B380` |
| [060 / 0x3c](060-0x3c-map-part.md) | Map Part (`SMapPart`) | derived | RTTI constructor `0x00599E40` |
| [061 / 0x3d](061-0x3d-level-point.md) | Level Point (`SLevelPoint`) | derived | RTTI constructor `0x005999C0` |
| [062 / 0x3e](062-0x3e-window-change.md) | Window Change (`SWindowChange`) | derived | RTTI constructor `0x0059CFD0` |
| [063 / 0x3f](063-0x3f-action-delay.md) | Action Delay (`SActionDelay`) | derived | RTTI constructor `0x00597160` |
| [064 / 0x40](064-0x40-send-patch.md) | Send Patch (`SSendPatch`) | raw | transform policy and owner protocol name |
| [066 / 0x42](066-0x42-exchange.md) | Exchange (`SExchange`) | derived | RTTI constructor `0x00598F50` |
| [068 / 0x44](068-0x44-add-user.md) | Add User (`SAddUser`) | derived | RTTI constructor `0x00597830` |
| [069 / 0x45](069-0x45-item-shop.md) | Item Shop (`SItemShop`) | derived | RTTI constructor `0x005996C0` |
| [071 / 0x47](071-0x47-num-users.md) | Num Users (`SNumUsers`) | derived | RTTI constructor `0x0059A8F0` |
| [072 / 0x48](072-0x48-spell-delay-cancel.md) | Spell Delay Cancel (`SSpellDelayCancel`) | derived | RTTI constructor `0x0059C040` |
| [073 / 0x49](073-0x49-request-portrait.md) | Request Portrait (`SRequestPortrait`) | derived | RTTI constructor `0x0059B490` |
| [074 / 0x4a](074-0x4a-bad-guy.md) | Bad Guy (`SBadGuy`) | derived | RTTI constructor `0x00597A90` |
| [075 / 0x4b](075-0x4b-bounce.md) | Bounce (`SBounce`) | derived | RTTI constructor `0x00597CF0` |
| [076 / 0x4c](076-0x4c-quit.md) | Quit (`SQuit`) | derived | RTTI constructor `0x0059AD20` |
| [080 / 0x50](080-0x50-manual.md) | Manual (`SManual`) | derived | RTTI constructor `0x00599AE0` |
| [081 / 0x51](081-0x51-block-input.md) | Block Input (`SBlockInput`) | derived | RTTI constructor `0x00597BC0` |
| [086 / 0x56](086-0x56-multi.md) | Multi Server (`SMulti`) | static | RTTI constructor `0x0059A7C0` |
| [091 / 0x5b](091-0x5b-advertisement.md) | Advertisement (`SAdvertisement`) | derived | RTTI constructor `0x00597930` |
| [096 / 0x60](096-0x60-stipulation.md) | Stipulation (`SStipulation`) | static | RTTI constructor `0x0059C8B0` |
| [098 / 0x62](098-0x62-web-board.md) | Web Board (`SWebBoard`) | static | RTTI constructor `0x0059CDC0` |
| [099 / 0x63](099-0x63-group.md) | Group (`SGroup`) | derived | RTTI constructor `0x005994C0` |
| [100 / 0x64](100-0x64-mini-game.md) | Mini Game (`SMiniGame`) | derived | RTTI constructor `0x0059A240` |
| [102 / 0x66](102-0x66-browser.md) | Browser (`SBrowser`) | static | RTTI constructor `0x00597E20` |
| [104 / 0x68](104-0x68-check-time.md) | Check Time (`SCheckTime`) | derived | RTTI constructor `0x005982F0` |
| [107 / 0x6b](107-0x6b-screen-shot.md) | Screen Shot (`SScreenShot`) | derived | RTTI constructor `0x0059B930` |
| [109 / 0x6d](109-0x6d-family-name.md) | Family Name (`SFamilyName`) | derived | RTTI constructor `0x00599180` |
| [111 / 0x6f](111-0x6f-meta-data.md) | Meta Data (`SMetaData`) | static | handler `0x004E4EA0` |

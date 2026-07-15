# Server-to-client packet registry

The client registers **61** RTTI-backed receive opcodes in `net_register_server_packet_factories` at `0x595F00`. This is not the complete set of supported server opcodes: the active game dispatcher also recognizes some packets directly from the preserved post-decrypt body.

Names are recovered from Visual C++ RTTI and are therefore stronger than guesses, although friendly protocol names may be changed later. Concrete display names omit the redundant class suffix. Payload models describe bytes after the opcode and before any encryption trailer removed by the client.

## Lobby/login packets outside the game registry

The loaded game-server factory registry does **not** register opcodes `0x00`, `0x01`, or `0x02`. All 61 cross-references to `net_register_server_packet_factory` come from the one registry constructor. However, the local receive crypto switch explicitly classifies `0x00` as raw and `0x01`/`0x02` as primary-key encrypted. The raw `0x00` handler has now been recovered outside the registry; `0x01` and `0x02` still require further lobby-state tracing.

| Opcode | Internal/related name | Current status |
|---:|---|---|
| [0x00](./000-0x00-version-check.md) | `SVersionCheck` / `VersionCheck` | raw handler recovered; subtype 0 installs salt selector and replacement key |
| [0x01](./001-0x01-new-user-check.md) | `SNewUserCheck?` / `NewUserCheck` | local decrypt support confirmed; semantics/handler uncertain |
| [0x02](./002-0x02-check.md) | `SCheck` / `LoginCheck` / `LoginResult` | local decrypt support confirmed; payload handler not yet isolated |
| [0x03](./003-0x03-transfer-server.md) | `STransferServer` | locally RTTI-registered; the lobby can use it to hand the client to a game server |

The 61-entry table below remains the source of truth for packet-object support in the currently recovered game-server registry.

## Manual raw-body handlers outside the RTTI registry

`event_dispatch` retains both the raw post-decrypt body and, when available, the packet object created by `net_deserialize_server_packet`. `net_dispatch_game_server_message` at `0x5ED990` uses both representations. Consequently, an opcode may be supported even when no factory is registered for it.

These six opcodes are checked by the game dispatcher but are absent from the 61-entry RTTI registry:

| Opcode | Internal/related name | Raw handler | Current status |
|---:|---|---:|---|
| [0x1B](./027-0x1b-enter-editing-mode.md) | `SEnterEditingMode?` / `EnterEditingMode` | `net_handle_s_enter_editing_mode` (`0x5F71C0`) | confirmed local parser; opens the paper editor |
| 0x31 | `SBulletin?` / `BoardResult` | `0x5F6CB0` | manual handler confirmed; payload audit pending |
| 0x34 | `SObjectInfoReply?` / `UserProfile` | `0x5F1590` | manual handler confirmed; payload audit pending |
| [0x35](./053-0x35-show-paper.md) | `SShowPaper` | `net_handle_s_show_paper` (`0x5F7250`) | confirmed; read-only paper UI, dismissed locally without a client packet |
| 0x36 | `SUserList?` / `WorldList` | `0x5F7B80` | manual handler confirmed; payload audit pending |
| 0x4F | `SMerc?` | `0x5F6BF0` | manual handler confirmed; payload audit pending |

The same dispatcher also performs raw-body checks for registered opcodes `0x06`, `0x2E`, `0x3B`, `0x3C`, and `0x42`. Those packets therefore have both an RTTI object and a raw-body path available to downstream code.

| Opcode | RTTI packet class | Preliminary payload model | Deserializer |
|---:|---|---|---:|
| [0x03](./003-0x03-transfer-server.md) | STransferServer | u32be, u16be, string[u8 length] | `0x59CA40` |
| [0x04](./004-0x04-user-position.md) | SUserPosition | u16be, u16be | `0x59CCD0` |
| [0x05](./005-0x05-user-appearance.md) | SUserAppearance | u32be, u8, u8, u8, u8, u8 | `0x59CB70` |
| [0x06](./006-0x06-map.md) | SMap | u8, u8, u8, u8, remaining-view | `0x599D10` |
| [0x07](./007-0x07-draw-objects.md) | SDrawObjects | u16be value subreader over all remaining payload bytes Note: the apparent loop in this method does not consume fields; detailed object records are handled downstream. | `0x598AB0` |
| [0x08](./008-0x08-status.md) | SStatus | `u8 flags`, then conditional fixed character (`0x20`), current vitals (`0x10`), experience/currency (`0x08`), and extended status (`0x04`) groups. High bits encode a client state; `0x02` and `0x01` consume no bytes. | `0x59C410` |
| [0x0A](./010-0x0a-message.md) | SMessage | u8 message_type if message_type == 0x11: u8, u8, string[u8 length] u16be data_length bytes[data_length] | `0x59A100` |
| [0x0B](./011-0x0b-move.md) | SMove | u8, u16be, u16be, u16be, u16be, u8 | `0x59A550` |
| [0x0C](./012-0x0c-move-object.md) | SMoveObject | u32be, u16be, u16be, u8 | `0x59A6B0` |
| [0x0D](./013-0x0d-say.md) | SSay | u8, u32be, string[u8 length] | `0x59B5C0` |
| [0x0E](./014-0x0e-remove-objects.md) | SRemoveObjects | u32be | `0x59B080` |
| [0x0F](./015-0x0f-add-inventory.md) | SAddInventory | u8, u16be, u8, string[u8 length], u32be, u8, u32be, u32be | `0x597430` |
| [0x10](./016-0x10-remove-inventory.md) | SRemoveInventory | u8 | `0x59AF70` |
| [0x11](./017-0x11-change-direction.md) | SChangeDirection | u32be, u8 | `0x597FE0` |
| [0x13](./019-0x13-damage-effect.md) | SDamageEffect | u32be, u8, u8, u8 | `0x598430` |
| [0x15](./021-0x15-map-size.md) | SMapSize | u16be, u8, u8, u8, u8, u24be, string[u8 length] | `0x599F90` |
| [0x17](./023-0x17-add-spell.md) | SAddSpell | u8, u16be, u8, string[u8 length], string[u8 length], u8 | `0x5976F0` |
| [0x18](./024-0x18-remove-spell.md) | SRemoveSpell | u8 | `0x59B2A0` |
| [0x19](./025-0x19-sound-effect.md) | SSoundEffect | u8 sound_id if sound_id == 0xFF: u8 extended_sound_id | `0x59BF30` |
| [0x1A](./026-0x1a-motion.md) | SMotion | u32be, u8, u16be | `0x59A420` |
| [0x1F](./031-0x1f-change-weather.md) | SChangeWeather | u8 | `0x598210` |
| [0x20](./032-0x20-change-hour.md) | SChangeHour | u8 | `0x598100` |
| [0x21](./033-0x21-self-save-ok.md) | SSelfSaveOK | none | `0x59BE30` |
| [0x29](./041-0x29-effect-layer.md) | SEffectLayer | u32be discriminator if discriminator != 0: u32be u16be if discriminator != 0: u16be u16be if discriminator == 0: u16be, u16be | `0x598DE0` |
| [0x2C](./044-0x2c-add-skill.md) | SAddSkill | u8, u16be, string[u8 length] | `0x5975C0` |
| [0x2D](./045-0x2d-remove-skill.md) | SRemoveSkill | u8 | `0x59B190` |
| [0x2E](./046-0x2e-field-map.md) | SFieldMap | string[u8 length] name u8 record_count u8 mode_or_flags repeat record_count times:   u16be   u16be   u8 data_length   bytes[data_length]   u16be   u16be   u16be   u16be | `0x5992C0` |
| [0x2F](./047-0x2f-screen-menu.md) | SScreenMenu | u8, u8, u32be skip/view 1 byte u16be, u8 skip/view 4 bytes u8 string[u8 length] u16be data_length bytes[data_length] subreader over remaining payload | `0x59B730` |
| [0x30](./048-0x30-pursuit-message.md) | SPursuitMessage | u8 message_type if message_type != 0x0A:   u8, u32be   skip/view 1 byte   u16be, u8   skip/view 4 bytes   u16be, u16be, u8, u8, u8   string[u8 length]   if message_type in {0,2,4,6,9}:     u16be data_length     bytes[data_length]   subreader over remaining payload | `0x59AA70` |
| [0x32](./050-0x32-static-object-state.md) | SStaticObjectState | u8 record_count repeat record_count times:   u8   u8   u8   u8 | `0x59C290` |
| [0x33](./051-0x33-draw-human-objects.md) | SDrawHumanObjects | u16be, u16be, u8, u32be, u16be appearance_id if appearance_id != special_appearance_constant:   packed/variant fields: u8, u16be, u8, u16be, u8, u16be, u8, u8, u8, u16be, u8, u16be, u8, u16be, u8, u8, u8, u16be, u8, u8, u8, u8, u8 else:   u16be, u8, u8, u8, skip/view 5 bytes, u8 string[u8 length] string[u8 length] Several packed appearance bits are normalized after reading. | `0x598570` |
| [0x37](./055-0x37-add-equip.md) | SAddEquip | u8, u16be, u8, string[u8 length], view(n), u32be, u32be | `0x5972C0` |
| [0x38](./056-0x38-remove-equip.md) | SRemoveEquip | u8 | `0x59AE60` |
| [0x39](./057-0x39-self-look.md) | SSelfLook | u8, string[u8 length], string[u8 length], string[u8 length], u8 u8 optional_block_present if optional_block_present == 1:   string[u8 length] x 3   u8, u8   repeat 5 times: {u8, u8} u8, u8, u8 string[u8 length], string[u8 length] u8 record_count repeat record_count times:   u8, u8   string[u8 length]   string[u8 length] | `0x59BA70` |
| [0x3A](./058-0x3a-spelled.md) | SSpelled | u16be, u8 | `0x59C170` |
| [0x3B](./059-0x3b-request-crc.md) | SRequestCRC | u16be | `0x59B3B0` |
| [0x3C](./060-0x3c-map-part.md) | SMapPart | u16be, remaining-view | `0x599E70` |
| [0x3D](./061-0x3d-level-point.md) | SLevelPoint | u8, u8 | `0x5999F0` |
| [0x3E](./062-0x3e-window-change.md) | SWindowChange | u8 | `0x59D000` |
| [0x3F](./063-0x3f-action-delay.md) | SActionDelay | u8, u8, u32be | `0x597190` |
| [0x42](./066-0x42-exchange.md) | SExchange | u8 variant variant 0: u32be, string[u8 length] variant 1: u8 variant 2: u8, u8, u16be, u8, string[u8 length] variant 3: u8, u32be variant 4: u8, string[u8 length] variant 5: u8, string[u8 length] | `0x598F80` |
| [0x44](./068-0x44-add-user.md) | SAddUser | none | `0x597860` |
| [0x45](./069-0x45-item-shop.md) | SItemShop | u8 variant if variant == 0:   u8   subreader over remaining payload | `0x599730` |
| [0x47](./071-0x47-num-users.md) | SNumUsers | u16be | `0x59A920` |
| [0x48](./072-0x48-spell-delay-cancel.md) | SSpellDelayCancel | none | `0x59C070` |
| [0x49](./073-0x49-request-portrait.md) | SRequestPortrait | none | `0x59B4C0` |
| [0x4A](./074-0x4a-bad-guy.md) | SBadGuy | u8 mode, u8 marker byte, u32be guard | `0x597AC0` |
| [0x4B](./075-0x4b-bounce.md) | SBounce | u16be, view(n) | `0x597D20` |
| [0x4C](./076-0x4c-quit.md) | SQuit | u8 | `0x59AD50` |
| [0x50](./080-0x50-manual.md) | SManual | u8, u8 u8 variant variant 0: u8 variant 1:   u8, u16be   u8 length_1, bytes[length_1]   u16be length_2, bytes[length_2]   u16be length_3, bytes[length_3]   u8 | `0x599B10` |
| [0x51](./081-0x51-block-input.md) | SBlockInput | u8 state if state == 0: u8 | `0x597BF0` |
| [0x56](./086-0x56-multi.md) | SMulti | u16be, view(n) | `0x59A7F0` |
| [0x5B](./091-0x5b-advertisement.md) | SAdvertisement | u16be, view(n), u16be, u16be, u8 | `0x597960` |
| [0x60](./096-0x60-stipulation.md) | SStipulation | u8 variant variant 0: u32be variant 1: u16be data_length, bytes[data_length] | `0x59C8E0` |
| [0x62](./098-0x62-web-board.md) | SWebBoard | u8 variant if variant == 3:   string[u8 length] URL else:   string[u8 length]   string[u8 length] string[u8 length] common trailing field | `0x59CDF0` |
| [0x63](./099-0x63-group.md) | SGroup | u8 variant variant 1: string[u8 length] variant 4:   string[u8 length] x 3   u8, u8   repeat 5 times: {u8, u8} variant 5: string[u8 length] | `0x5994F0` |
| [0x64](./100-0x64-mini-game.md) | SMiniGame | u8 variant variant 3: u8 variant 4: u8 variant 7: u32be, u32be variant 8: u8 other observed variants consume no additional fields here | `0x59A270` |
| [0x66](./102-0x66-browser.md) | SBrowser | u8 variant variant 1 or 2:   u16be length_1, bytes[length_1]   u16be length_2, bytes[length_2] variant 3: string[u8 length] | `0x597E50` |
| [0x68](./104-0x68-check-time.md) | SCheckTime | u32be | `0x598320` |
| [0x6B](./107-0x6b-screen-shot.md) | SScreenShot | u8 | `0x59B960` |
| [0x6D](./109-0x6d-family-name.md) | SFamilyName | string[u8 length] | `0x5991B0` |

## Notation

- `string[u8 length]`: one-byte length followed by that many string bytes.
- `view(n)` / `bytes[n]`: a zero-copy or copied byte range of the stated size.
- `subreader(remaining)`: the packet object retains a reader for a nested structure parsed downstream.
- `repeat N times`: an actual counted packet substructure recovered from a backward control-flow edge.
- Variant and flag branches are mutually exclusive or conditional; they must not be flattened into one unconditional layout.

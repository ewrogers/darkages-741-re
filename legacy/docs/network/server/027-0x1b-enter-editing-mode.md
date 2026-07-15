# 027 / 0x1B: Enter Editing Mode (`SEnterEditingMode?`)

- Direction: server to client
- Internal/related name: `EnterEditingMode`
- Reconstructed C++ class name: `SEnterEditingMode?`
- Name provenance: related-engine internal enum name, confirmed by this client's local behavior and its paired `0x23 ExitEditingMode` response
- Receive handling: default derived-key transform, followed by a manual raw-body handler
- RTTI factory: none in the recovered 61-entry game registry

## Local receive path

`net_dispatch_game_server_message` (`0x5ED990`) compares the first byte of the preserved post-decrypt body with `0x1B` and calls `net_handle_s_enter_editing_mode` (`0x5F71C0`). The handler opens the paper UI in editable mode through `ui_open_paper_window` (`0x54A470`), which selects `net_parse_s_enter_editing_mode_payload` (`0x54A530`).

This is an ordinary framed and transformed server packet. It was absent from the earlier inventory only because that inventory was generated from RTTI factory registrations; this packet bypasses packet-object construction and is parsed directly from the raw body.

## Post-decrypt body

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x1B` |
| 1 | `u8` | editor mode; retained and echoed by client packet `0x23` |
| 2 | `u8` | paper/editor configuration byte A |
| 3 | `u8` | paper/editor configuration byte B |
| 4 | `u8` | paper/editor configuration byte C |
| 5 | `u16be` | text length |
| 7 | `bytes[text_length]` | initial editor text |

The meanings of the three configuration bytes are not yet named confidently. The editor mode is stored at editor-object offset `+0x634`; `net_send_c_exit_editing_mode` later writes that value as byte 1 of the `0x23` response.

## Paired client packet

See [CExitEditingMode? (`0x23`)](../client/035-0x23-exit-editing-mode.md). Its post-transform plaintext body is:

```text
23 [u8 editor_mode] [u16be text_length] [text bytes...]
```

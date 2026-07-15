# 053 / 0x35: Show Paper (`SShowPaper`)

- Direction: server to client
- Internal name: `SShowPaper`
- Name provenance: user-provided internal name, independently confirmed by this client's read-only paper UI and close paths
- Receive handling: default derived-key transform, followed by a manual raw-body handler
- RTTI factory: none in the recovered 61-entry game registry

## Local receive path

`net_dispatch_game_server_message` (`0x5ED990`) checks the preserved post-decrypt body for opcode `0x35` and calls `net_handle_s_show_paper` (`0x5F7250`). It opens the same paper UI used by `0x1B`, but passes read-only mode to `ui_open_paper_window` (`0x54A470`) and selects `net_parse_s_show_paper_payload` (`0x54A680`).

The mode is stored at paper-window offset `+0x638`:

- `0`: editable `0x1B EnterEditingMode`
- `1`: read-only `0x35 SShowPaper`

`ui_handle_paper_close_action` (`0x54A9B0`) tests this mode when the player closes the window or presses Escape. It calls `net_send_c_exit_editing_mode` only for mode `0`. Mode `1` skips the send and goes directly to `ui_dismiss_paper_window` (`0x54A9F0`), so dismissing `SShowPaper` produces no client packet.

## Post-decrypt body

| Offset | Type | Meaning |
|---:|---|---|
| 0 | `u8` | opcode `0x35` |
| 1 | `u8` | paper/UI configuration byte A |
| 2 | `u8` | paper/UI configuration byte B |
| 3 | `u8` | paper/UI configuration byte C |
| 4 | `u8` | paper/UI configuration byte D |
| 5 | `u16be` | text length |
| 7 | `bytes[text_length]` | paper text |

The four configuration-byte meanings remain to be established from their UI consumers.

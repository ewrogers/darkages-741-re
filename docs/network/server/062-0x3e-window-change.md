# Window Change (`SWindowChange`)

`SWindowChange` chooses the active panel shown in the lower interface tray. It does not move or resize the game window. The server can select Items, Skills, Spells, Chat, or Status while leaving the tray expanded or collapsed as it already was.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3E` (62) |
| Transform | `derived` |
| UI owner | `GUIBackPane` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SWindowChange {
    u8 opcode                 // 0x3E
    u8 window_code
}
```

The concrete deserializer reads exactly one byte after the opcode. It does not read a count, window coordinates, or trailing fields.

## Page selection

| `window_code` | Internal page mode | Visible page |
| --- | --- | --- |
| `0` | `0` | Items (`ItemInventoryPane`) |
| `1` | `3` | Skills (`NewSkillInventoryPane`) |
| `2` | `1` | Spells (`NewSpellInventoryPane`) |
| `3` | `5` | Chat (`NewChattingPane`) |
| `4` | `7` | Status (`NewStatusInfoPane`) |

The skill, spell, chat, and status groups each have a second local subpage. This packet always selects the first page in those groups. The normal tray buttons can toggle between both pages.

## Client effect

`GUIBackPane` handles opcode `0x3E`. Its handler reads the current expanded flag, converts `window_code` to the internal page mode, and calls the same page-selection interface used by the local tray buttons. The selector hides the previous page, shows the selected page, updates the button and layout state, and redraws the tray.

The packet therefore changes only which lower-tray page is active. It preserves whether that tray is expanded or collapsed. Values outside `0` through `4` are accepted and consumed, but they do not change the page.

No client reply or paired request was found. Local clicks perform the same selection directly without sending a packet, so this appears to be a server-directed UI convenience rather than a state synchronization exchange.

Static addresses, names, and evidence are kept in the [function reference](../../appendix/functions.md) and `analysis/exports/packets.yaml`.

# User Setting (`CUserSetting`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x1B` (27) |
| Encoding | session key |
| Name provenance | Project-owner protocol name, confirmed by the Game Settings and Options dialog call sites |

## Purpose

The client sends this message for **user setting**.

The builder sends a two-byte body. The Game Settings dialog calls it when a setting changes, while the Options path also sends value `0` during its request or initialization flow. Individual setting identifiers remain to be mapped.

The prior `CUserStatus` reconstruction came from related vocabulary and was not supported by local RTTI. The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- `DialogPane::OptionPane`
- `DialogPane::GameSettingDialog`

## Body

```text
packet CUserSetting {
    u8 opcode                 // 0x1B
    u8 setting_id
}
```

# User Setting (`CUserSetting`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x1B` (27) |
| Common transform | derived |
| Representative builder | `net_send_user_setting` at `0x00542E60` |
| Name provenance | Project-owner protocol name, confirmed by the Game Settings and Options dialog call sites |

## Current evidence

The builder sends a two-byte body. The Game Settings dialog calls it when a setting changes, while the Options path also sends value `0` during its request or initialization flow. Individual setting identifiers remain to be mapped.

The prior `CUserStatus` reconstruction came from related vocabulary and was not supported by local RTTI. The client has no derived packet RTTI for this name.

## Known send sites

- `0x00542AD6` in `sub_542370`, reachable from `DialogPane::OptionPane`.
- `0x00542CB7` in `sub_542C60`, reachable from `DialogPane::GameSettingDialog`.

## Plaintext body

```text
opcode:u8                 // 0x1B
setting_id:u8
```

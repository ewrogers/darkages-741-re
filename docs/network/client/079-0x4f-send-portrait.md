# Send Portrait (`CSendPortrait`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4F` (79) |
| Encoding | session key |
| Name provenance | Verified project protocol name, matched to the local portrait builder. |

## Purpose

The client sends this message for **send portrait**.

`net_send_c_portrait?` submits a global packet buffer initialized with command `0x4F`.

## Sent by

Known static callers lead to:

- `UserInfoPane::UserInfoPane_ForUser`

## Body

```text
packet CSendPortrait {
    u8 opcode                 // 0x4F
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.

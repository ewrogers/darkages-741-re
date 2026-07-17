# Change User State (`CChangeUserState`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x79` (121) |
| Encoding | session key |
| Name provenance | Project protocol vocabulary, confirmed against the local builder and the shared world-list state domain. |

## Purpose

The client sends `CChangeUserState` when the player chooses a new presence or group-seeking state in the UI.

## Body

```text
packet CChangeUserState {
    u8 opcode                    // 0x79
    u8 user_state               // UserState
}
```

The values are defined under [`UserState`](../protocol-types.md#userstate). The same byte appears on each row of [`SShowUsers`](../server/054-0x36-show-users.md).

## Validation and local state

`net_send_change_user_state` accepts only values `0` through `7`. A negative value or a value of `8` or greater is replaced with `0` before the packet is sent. The normalized value is also stored as the local character's current state.

# Quit (`SQuit`)

`SQuit` approves the safe-quit request started by the in-game options UI. A value of `1` advances the alert and causes the client to acknowledge with `CQuit 00`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x4C` (76) |
| Transform | derived |
| Runtime owner | `SafeQuitAlert` |
| Paired packet | [`CQuit`](../client/011-0x0b-quit.md) |
| Name provenance | Microsoft C++ RTTI in the target |

## Plaintext body

```text
packet SQuit {
    u8      opcode                    // 0x4C
    u8      approved                  // value 1 advances SafeQuitAlert
    bytes   trailing[2]               // observed as 00 00; not consumed by the client
}
```

`net_deserialize_quit_server_packet` performs exactly one `u8` read after the opcode and stores it in the `SQuit` object. It does not read, skip, or combine the following two bytes. The `trailing` field records the observed capture shape without claiming that the client treats the bytes as a `u16` value.

## Client handling

`ui_safe_quit_alert_handle_network_event` accepts opcode `0x4C` only while a `SafeQuitAlert` owns the event. It passes the typed `SQuit` object to `ui_safe_quit_alert_apply_quit_response`.

When `approved == 1`, the alert:

1. Marks its local safe-quit state as approved.
2. Sends `CQuit` as `0B 00`.
3. Replaces the alert text with localized string `0x19`.
4. Refreshes the affected alert control.

Other values are consumed by this handler but cause none of those state changes. No client range check or additional value table was found.

The matching observed exchange is:

```text
C> 0B 01
S> 4C 01 00 00
C> 0B 00
```

## What it does not control

The consumed `SQuit` byte is not used as a lobby or reconnect selector. The handler checks only for value `1` and advances the safe-quit handshake.

The separate opcode-only `CQuit` path performs its own connection teardown and uses local configuration to choose a new `TerminalPane2` startup path or process closure. That decision does not read an `SQuit` field.

## Unknown trailing bytes

The two trailing bytes are confirmed as `00 00` in the supplied capture, but the version 741 client leaves them unread. They may be server-owned padding, reserved fields, or data for another client version. Their purpose cannot be recovered from this client's typed `SQuit` path.

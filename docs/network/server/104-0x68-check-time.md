# Check Time (`SCheckTime`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x68` (104) |
| Transform | derived |
| Class name | `SCheckTime` |
| Name provenance | Microsoft C++ RTTI in the target |
| Owner | Main world packet dispatcher |

## Purpose

`SCheckTime` asks the client for its current Windows multimedia tick count. The client immediately answers with [`CCheckTime`](../client/117-0x75-check-time.md), echoes the server's value, and appends `timeGetTime()`.

This exchange can let a server compare client-clock progress with server-observed elapsed time. Speed-hack or tick-rate validation is therefore a plausible server-side use, but the trigger policy is not present in the client. The server could send the request periodically, after suspicious movement, or for another timing purpose. The client cannot distinguish those cases.

Separately, the application main loop compares several local clock sources and can send a [`CException`](../client/066-0x42-exception.md) report beginning with `SpeedHack`. That local detector does not depend on this packet. It is not evidence that a particular server-side `SCheckTime` policy exists.

## Body

```text
packet SCheckTime {
    u8  opcode                    // 0x68
    u32 server_value
}
```

`net_deserialize_check_time_server_packet` reads the big-endian value into the packet object at `+0x10`. The client gives it no local interpretation. It behaves as a correlation value, challenge, or server timestamp only from the client's point of view.

## Handling

The main world packet dispatcher recognizes typed opcode `0x68` and calls `net_send_check_time` directly. That function:

1. Copies `server_value` from the packet.
2. Calls `timeGetTime()` once.
3. Builds the nine-byte plaintext `CCheckTime` body.
4. Submits it immediately through the normal client packet sender.

There is no timer, deliberate delay, UI change, character-state write, comparison, tolerance check, or local enforcement action in this packet handler.

This handler belongs to the gameplay `WorldPane`. Test the packet after the character has entered the world and that pane is registered. During login or another screen without the world handler, the decoded packet has no confirmed responder.

## Testing

After entering the world, send this decoded body with the normal derived server transform:

```text
68 12 34 56 78
```

The expected decoded response is:

```text
75 12 34 56 78 TT TT TT TT
```

The final four bytes are the client's big-endian `timeGetTime()` value. Sending two requests at a known interval lets the server compare the unsigned tick difference with its own elapsed time. The 32-bit count wraps naturally after about 49.7 days, so a robust comparison must use modulo-`2^32` subtraction.

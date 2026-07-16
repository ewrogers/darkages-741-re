# Unhandled Control (0x58)

The live server sends this small control during login, but the 7.41 client does not assign it a packet class or act on it.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x58` (88) |
| Transform | `derived` |
| Name provenance | Behavioral description only; no RTTI packet name was recovered |

## Observed body

```text
struct ServerControl58 {
    u8 opcode                  // 0x58
    u8 zero                    // observed 0x00; meaning unknown
}
```

The supplied runtime observation places it after the initial [`SStatus`](008-0x08-status.md) and before [`SDrawHumanObjects`](051-0x33-draw-human-objects.md) during login. It appears to be sent on every login.

The zero byte cannot establish a field meaning. No client handler reads it, and the inbound decryptor also writes a separate local zero after every decoded body as a buffer terminator.

## What the client does

Opcode `0x58` is not in the raw or static-key inbound sets, so the transport decodes it with the derived session key and posts the opcode-first body to the event system.

There is no `0x58` entry in `server_packet_factory`. Packet-object construction therefore returns null, while the raw decoded body remains available to pane event handlers. None of the target's RTTI-backed pane handlers checks for `0x58`, including the world dispatcher. The event falls through unconsumed and changes no known client state.

In particular, it does not show or hide `MapLoadingPane`. Actual map-transfer progress is driven by [`SMapPart`](060-0x3c-map-part.md).

The server-side purpose may be a compatibility or historical marker, but this binary provides no evidence for a more specific name.

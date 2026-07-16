# Unhandled Map-Transfer Control (0x67)

The live server sends this small control when a map is transferred, but the 7.41 client does not assign it a packet class or act on it.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x67` (103) |
| Transform | `derived` |
| Name provenance | Behavioral description from runtime ordering; no RTTI packet name was recovered |

## Observed body

```text
struct ServerControl67 {
    u8 opcode                  // 0x67
    u8 zero                    // observed 0x00; meaning unknown
}
```

Runtime observation associates this control with map transfer rather than every login. Its exact position in the wider transfer sequence is useful behavioral evidence, but it does not prove whether the server intended it as a start marker, completion marker, or compatibility notice.

The zero byte is likewise unresolved. No client handler reads it, and the inbound decryptor appends its own local buffer terminator after the decoded length.

## What the client does

Opcode `0x67` uses the derived session-key transform. It has no entry in `server_packet_factory`, so no RTTI packet object is constructed. The decoded body still enters the pane event path, but none of the target's RTTI-backed pane handlers checks for `0x67`. The world dispatcher returns it unconsumed.

It therefore has no confirmed state, rendering, map, or loading-pane effect in this client. [`SMapPart`](060-0x3c-map-part.md) opcode `0x3C` is what creates `MapLoadingPane`, advances its percentage, and closes it after the final part.

The server may retain `0x67` for another client generation or an older protocol path. That remains a possibility rather than a conclusion from this binary.

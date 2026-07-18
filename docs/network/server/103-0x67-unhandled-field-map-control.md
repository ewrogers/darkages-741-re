# Unhandled Field/Map Control (0x67)

The live server sends this small control around field-map presentation and map transfer, but the 7.41 client does not assign it a packet class or act on it.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x67` (103) |
| Transform | `derived` |
| Name provenance | Behavioral description from runtime ordering; no RTTI packet name was recovered |

## Observed bodies

The bytes after the opcode remain opaque because no client code reads them:

```text
packet ServerControl67 {
    u8      opcode                    // 0x67
    bytes   payload[decoded_length - 1]
}
```

Two captures now show different payload shapes:

```text
67 00
67 03 00 00 00 00 00
```

The longer form appears once after `SFieldMap` creates the navigation pane and again immediately after `CFieldMap`, before the destination map begins loading. That ordering does not establish a subtype or integer layout, so the `03` and zero bytes remain unnamed.

## What the client does

Opcode `0x67` uses the derived session-key transform. It has no entry in `server_packet_factory`, so no RTTI packet object is constructed. The decoded body still enters the pane event path, but none of the target's RTTI-backed pane handlers checks for `0x67`. The world dispatcher returns it unconsumed.

It therefore has no confirmed state, rendering, field-map, map, or loading-pane effect in this client. [`SFieldMap`](046-0x2e-field-map.md) creates the navigation pane. [`SMapPart`](060-0x3c-map-part.md) creates `MapLoadingPane`, advances its percentage, and closes it after the final part.

The server may retain `0x67` for another client generation, server bookkeeping, or an older protocol path. Those remain possibilities rather than conclusions from this binary.

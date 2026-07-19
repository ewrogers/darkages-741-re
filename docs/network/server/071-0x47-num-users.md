# Num Users (`SNumUsers`)

`SNumUsers` carries one server-supplied user count, but this client never uses it. The receive factory constructs and parses the packet, then normal event delivery finds no world, manager, or UI handler for opcode `0x47`.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x47` (71) |
| Transform | `derived` |
| Name provenance | Microsoft C++ RTTI in the target |

## Body

```text
packet SNumUsers {
    u8 opcode                 // 0x47
    u16 user_count
}
```

The concrete deserializer reads exactly one big-endian `u16` after the opcode and stores it in the packet object. It does not consume any other fields.

## What the client does with it

The client has no handler for this packet. The central world dispatcher does not check opcode `0x47`, and none of the pane or manager functions that inspect typed server packet opcodes checks it either. A separate scan of literal `0x47` comparisons found no raw-buffer network handler.

If a server sends this packet, the normal receive path can decrypt it, construct `SNumUsers`, and parse `user_count`. Event propagation then finishes without copying the value into client state, opening a pane, drawing text, or sending a reply. The temporary packet object is eventually released with the event.

Factory registration proves that the client recognizes the packet layout. It does not prove that a version 7.41 server still sends the packet.

## No confirmed request or response pair

No client action or outgoing request was found that expects `SNumUsers`. In particular:

- [`CWho`](../client/024-0x18-who.md) requests the visible user list and is answered by [`SShowUsers`](054-0x36-show-users.md), not `SNumUsers`.
- Client opcode `0x47` is [`CAddStat`](../client/071-0x47-add-stat.md). Packet numbers are direction-specific, so it is unrelated. The stat UI waits for `SLevelPoint` or `SStatus` updates instead.

The exact server-side trigger or send time cannot be recovered from this client because it neither requests nor consumes the value. `derived` is the only timing constraint visible here: this is a normal transformed server packet, not part of the initial raw greeting.

Static addresses, names, and evidence are kept in the [function reference](../../appendix/functions.md) and `analysis/exports/packets.yaml`.

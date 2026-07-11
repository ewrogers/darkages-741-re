# 003 / 0x03: Transfer Server (`STransferServer`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x03` |
| RTTI class | `STransferServer` |
| Factory | `0x59C990` |
| Constructor | `0x59CA10` |
| Vtable | `0x68818C` |
| Deserializer | `0x59CA40` |

## Preliminary payload model

```text
1. u32be destination IPv4/address value
2. u16be destination port
3. transfer_token[u8 length]
```

## Raw reader-call trace

`u32be -> u16be -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Lobby role: the lobby server is known to send this packet to hand the client to a game server; this explains why `0x03` is present even though lobby-only `0x00-0x02` are absent from the game registry.
- Primitive widths and byte order: confirmed from reader implementations.
- The client reconnects to the supplied address/port and echoes the transfer token verbatim as the payload of raw `CTransferServerPacket 0x10`.
- This packet does **not** directly install the packet salt selector or replacement primary key. Those are read by raw `SVersionCheckPacket 0x00`, subtype `0`. In a capture this setup may occur immediately after transfer on the new connection, making it appear to be part of `STransferServer`.

# 010 / 0x0A: Message (`SMessage`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x0A` |
| RTTI class | `SMessage` |
| Factory | `0x59A050` |
| Constructor | `0x59A0D0` |
| Vtable | `0x687F70` |
| Deserializer | `0x59A100` |

## Preliminary payload model

```text
u8 message_type
if message_type == 0x11: u8, u8, string[u8 length]
u16be data_length
bytes[data_length]
```

## Raw reader-call trace

`u8 -> u8 -> u8 -> string[u8 length] -> u16be -> view(n)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

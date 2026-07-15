# 066 / 0x42: Exchange (`SExchange`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x42` |
| RTTI class | `SExchange` |
| Factory | `0x598ED0` |
| Constructor | `0x598F50` |
| Vtable | `0x687E98` |
| Deserializer | `0x598F80` |

## Preliminary payload model

```text
u8 variant
variant 0: u32be, string[u8 length]
variant 1: u8
variant 2: u8, u8, u16be, u8, string[u8 length]
variant 3: u8, u32be
variant 4: u8, string[u8 length]
variant 5: u8, string[u8 length]
```

## Raw reader-call trace

`u8 -> u32be -> string[u8 length] -> u8 -> u8 -> u8 -> u16be -> u8 -> string[u8 length] -> u8 -> u32be -> u8 -> string[u8 length] -> u8 -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

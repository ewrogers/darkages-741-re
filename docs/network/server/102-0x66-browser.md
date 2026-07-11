# 102 / 0x66: Browser (`SBrowser`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x66` |
| RTTI class | `SBrowser` |
| Factory | `0x597DA0` |
| Constructor | `0x597E20` |
| Vtable | `0x687D60` |
| Deserializer | `0x597E50` |

## Preliminary payload model

```text
u8 variant
variant 1 or 2:
  u16be length_1, bytes[length_1]
  u16be length_2, bytes[length_2]
variant 3: string[u8 length]
```

## Raw reader-call trace

`u8 -> u16be -> view(n) -> u16be -> view(n) -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

# 098 / 0x62: Web Board (`SWebBoard`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x62` |
| RTTI class | `SWebBoard` |
| Factory | `0x59CD40` |
| Constructor | `0x59CDC0` |
| Vtable | `0x6881CC` |
| Deserializer | `0x59CDF0` |

## Preliminary payload model

```text
u8 variant
if variant == 3:
  string[u8 length] URL
else:
  string[u8 length]
  string[u8 length]
string[u8 length] common trailing field
```

## Raw reader-call trace

`u8 -> string[u8 length] -> string[u8 length] -> string[u8 length] -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

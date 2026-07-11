# 057 / 0x39: Self Look (`SSelfLook`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x39` |
| RTTI class | `SSelfLook` |
| Factory | `0x59B9C0` |
| Constructor | `0x59BA40` |
| Vtable | `0x6880EC` |
| Deserializer | `0x59BA70` |

## Preliminary payload model

```text
u8, string[u8 length], string[u8 length], string[u8 length], u8
u8 optional_block_present
if optional_block_present == 1:
  string[u8 length] x 3
  u8, u8
  repeat 5 times: {u8, u8}
u8, u8, u8
string[u8 length], string[u8 length]
u8 record_count
repeat record_count times:
  u8, u8
  string[u8 length]
  string[u8 length]
```

## Raw reader-call trace

`u8 -> string[u8 length] -> string[u8 length] -> string[u8 length] -> u8 -> u8 -> string[u8 length] -> string[u8 length] -> string[u8 length] -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> u8 -> string[u8 length] -> string[u8 length] -> u8 -> u8 -> u8 -> string[u8 length] -> string[u8 length]`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

# 048 / 0x30: Pursuit Message (`SPursuitMessage`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x30` |
| RTTI class | `SPursuitMessage` |
| Factory | `0x59A980` |
| Constructor | `0x59AA00` |
| Vtable | `0x687FFC` |
| Deserializer | `0x59AA70` |

## Preliminary payload model

```text
u8 message_type
if message_type != 0x0A:
  u8, u32be
  skip/view 1 byte
  u16be, u8
  skip/view 4 bytes
  u16be, u16be, u8, u8, u8
  string[u8 length]
  if message_type in {0,2,4,6,9}:
    u16be data_length
    bytes[data_length]
  subreader over remaining payload
```

## Raw reader-call trace

`u8 -> u8 -> u32be -> view(n) -> u16be -> u8 -> view(n) -> u16be -> u16be -> u8 -> u8 -> u8 -> string[u8 length] -> u16be -> view(n) -> subreader(remaining)`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

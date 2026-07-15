# 100 / 0x64: Mini Game (`SMiniGame`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x64` |
| RTTI class | `SMiniGame` |
| Factory | `0x59A1C0` |
| Constructor | `0x59A240` |
| Vtable | `0x687F84` |
| Deserializer | `0x59A270` |

## Preliminary payload model

```text
u8 variant
variant 3: u8
variant 4: u8
variant 7: u32be, u32be
variant 8: u8
other observed variants consume no additional fields here
```

## Raw reader-call trace

`u8 -> u8 -> u8 -> u32be -> u32be -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

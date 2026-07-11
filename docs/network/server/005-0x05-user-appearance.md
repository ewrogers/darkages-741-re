# 005 / 0x05: User Appearance (`SUserAppearance`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x05` |
| RTTI class | `SUserAppearance` |
| Factory | `0x59CAC0` |
| Constructor | `0x59CB40` |
| Vtable | `0x6881A0` |
| Deserializer | `0x59CB70` |

## Preliminary payload model

```text
1. u32be
2. u8
3. u8
4. u8
5. u8
6. u8
```

## Raw reader-call trace

`u32be -> u8 -> u8 -> u8 -> u8 -> u8`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

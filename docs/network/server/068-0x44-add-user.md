# 068 / 0x44: Add User (`SAddUser`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x44` |
| RTTI class | `SAddUser` |
| Factory | `0x5977B0` |
| Constructor | `0x597830` |
| Vtable | `0x687CFC` |
| Deserializer | `0x597860` |

## Preliminary payload model

```text
No payload fields are consumed by this packet deserializer.
```

## Raw reader-call trace

`no packet-reader calls`

The raw trace lists static reader call sites. Conditional variants and counted records are represented more accurately in the preliminary model above and must not be interpreted as one unconditional flat structure.

## Verification status

- Opcode registration: confirmed from the client registry.
- Packet class name: confirmed from Visual C++ RTTI.
- Primitive widths and byte order: confirmed from reader implementations.
- Semantic field names: pending server-source or capture verification.

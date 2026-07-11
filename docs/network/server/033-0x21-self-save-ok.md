# 033 / 0x21: Self Save OK (`SSelfSaveOK`)

## Identification

| Property | Value |
|---|---|
| Direction | Server to client |
| Opcode | `0x21` |
| RTTI class | `SSelfSaveOK` |
| Factory | `0x59BD80` |
| Constructor | `0x59BE00` |
| Vtable | `0x688100` |
| Deserializer | `0x59BE30` |

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
- `net_dispatch_game_server_message` at `0x5ED990` does not dispatch opcode `0x21` to a handler in this build.
- There is no local evidence that this packet completes `CRefresh` processing.

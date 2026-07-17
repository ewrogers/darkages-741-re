# User Change State (`CUserChangeState`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x79` (121) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **user change state**.

## Sent by

Known static callers lead to:

- `MapUserInterface::WorldPane_Impl`

## Body

```text
packet CUserChangeState {
    u8      opcode                    // 0x79
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.

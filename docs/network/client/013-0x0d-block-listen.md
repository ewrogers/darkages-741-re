# Block Listen (`CBlockListen`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0D` (13) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **block listen**.

## Sent by

Known static callers lead to:

- `CharInputPane::BlockListenInputPane`

## Body

```text
packet CBlockListen {
    u8 opcode                 // 0x0D
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.

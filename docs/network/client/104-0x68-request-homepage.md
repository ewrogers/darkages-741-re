# Request Homepage (`CRequestHomepage`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x68` (104) |
| Encoding | startup key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **request homepage**.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CRequestHomepage {
    u8 opcode                 // 0x68
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.

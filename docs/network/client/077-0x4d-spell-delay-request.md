# Spell Delay Request (`CSpellDelayRequest`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x4D` (77) |
| Encoding | session key |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

The client sends this message for **spell delay request**.

## Sent by

Known static callers lead to:

- `LineInputPane::StringSpellInputPane, ArgsLineInputPane::NumberArgsSpellInputPane`

## Body

```text
packet CSpellDelayRequest {
    u8 opcode                 // 0x4D
    ...                         // fields pending
}
```

Field order, variants, state effects, and paired packets remain to be traced.

# Send Portrait (`CSendPortrait?`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x4F` (79) |
| Common transform | derived |
| Representative builder | `0x005B1160` |
| Name provenance | The class spelling is reconstructed from the locally confirmed portrait builder and related terminology. |

## Current evidence

`net_send_c_portrait?` at `0x005B1160` submits a global packet buffer. `0x0054CE10` initializes that buffer with opcode `0x4F`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x5AD23E` in `sub_5ad160`, reachable from `UserInfoPane::UserInfoPane_ForUser`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.

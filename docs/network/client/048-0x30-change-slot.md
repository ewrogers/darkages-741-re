# Change Slot (`CChangeSlot`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x30` (48) |
| Common transform | derived |
| Representative builder | `0x00490F40` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x00490F40` writes opcode `0x30` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x48FBBD` in `sub_48fa50`, reachable from `Pane::InventoryPane_A`, `InventoryPane_A::ItemInventoryPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.

# Add Stat (`CAddStat`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x47` (71) |
| Encoding | derived |
| Name provenance | Verified project protocol name; the command and local builder are confirmed. |

## Purpose

`StatusInfoPane` sends this packet when the player activates one of its five stat-increase controls. The client identifies the chosen control with one selector byte.

## Body

```text
packet CAddStat {
    u8      opcode                    // 0x47
    u8      stat_selector
}
```

The selector names are project-owner protocol vocabulary. The client directly confirms all five nonzero values and their control mapping:

| Name | Selector | Control index |
| --- | ---: | ---: |
| `None` | `0x00` | none |
| `Strength` | `0x01` | `0` |
| `Dexterity` | `0x02` | `4` |
| `Intelligence` | `0x04` | `1` |
| `Wisdom` | `0x08` | `2` |
| `Constitution` | `0x10` | `3` |

The client only sends when the selected index is between `0` and `4`; there is no other payload. In visible control order, the constructor's selector table is therefore `01 04 08 10 02`.

`net_send_add_stat` does not decrement the local point count or hide the controls. The visible state changes only after the server sends a later [`SLevelPoint`](../server/061-0x3d-level-point.md) or [`SStatus`](../server/008-0x08-status.md) update.

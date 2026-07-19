# Request Family Name (`CRequestFamilyName`)

`CRequestFamilyName` asks for the local character's family name when the player opens the family-list dialog.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x7A` |
| Transform | `derived` |
| Name provenance | Project-owner protocol name, paired with exact RTTI server response `SFamilyName` |
| UI owner | Exact RTTI `FamilyListDialogPane` |

## Body

```text
packet CRequestFamilyName {
    u8 opcode                    // 0x7A
}
```

## Where it is sent

`EquipPane` action `0x19` allocates `FamilyListDialogPane`. The dialog loads `lfamily.txt`, creates its local family-member rows, registers for events, and immediately sends this opcode-only packet from its constructor.

The request is therefore not periodic and is not sent during login. It is sent each time this family-list construction path runs.

The paired response is [`SFamilyName`](../server/109-0x6d-family-name.md).

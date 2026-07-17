# Request Family Name (`CRequestFamilyName`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x7A` (122) |
| Encoding | session key |
| Related protocol name | `CRequestLoverName` |
| Name provenance | Project-owner protocol name normalized to the exact server RTTI term `SFamilyName` |

## Purpose

The client sends this message for **request family name**.

The builder submits an opcode-only request. Project vocabulary calls it `CRequestLoverName`; this book uses `CRequestFamilyName` to match the exact RTTI-backed server response [`SFamilyName`](../server/109-0x6d-family-name.md). This is a documented naming choice, not recovered client RTTI.

## Sent by

Known static callers lead to:

- `DialogPane::EquipPane`

## Body

```text
packet CRequestFamilyName {
    u8      opcode                    // 0x7A
}
```

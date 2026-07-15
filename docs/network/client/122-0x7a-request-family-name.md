# Request Family Name (`CRequestFamilyName`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x7A` (122) |
| Common transform | derived |
| Representative builder | `net_request_family_name` at `0x004719B0` |
| Related protocol name | `CRequestLoverName` |
| Name provenance | Project-owner protocol name normalized to the exact server RTTI term `SFamilyName` |

## Current evidence

The builder submits an opcode-only request. Project vocabulary calls it `CRequestLoverName`; this book uses `CRequestFamilyName` to match the exact RTTI-backed server response [`SFamilyName`](../server/109-0x6d-family-name.md). This is a documented naming choice, not recovered client RTTI.

## Known send sites

- `0x004716C7` in `sub_471320`, reachable from `DialogPane::EquipPane`.

## Plaintext body

```text
opcode:u8                 // 0x7A
```

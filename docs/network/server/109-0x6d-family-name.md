# Family Name (`SFamilyName`)

`SFamilyName` returns the text drawn in the open family-list dialog.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x6D` |
| Concrete class | Exact RTTI `SFamilyName` |
| Transform | `derived` |
| UI owner | Exact RTTI `FamilyListDialogPane` |

## Body

```text
packet SFamilyName {
    u8 opcode                    // 0x6D
    string8 family_name
}
```

`FamilyListDialogPane` copies `family_name` verbatim into a 256-byte local buffer and redraws. It performs no comparison with `"NoName"` or `"Noname"` and supplies no fallback for an empty response.

The executable does contain the literal `"Noname"`, but the family-list constructor uses it for local member-row placeholders when a row is unavailable. It is not an `SFamilyName` default. If a server returns `"NoName"`, that policy belongs to the server and the client simply displays those bytes.

The paired request is [`CRequestFamilyName`](../client/122-0x7a-request-family-name.md).

# Change Password (`CChangePassword`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x26` (38) |
| Common transform | static |
| Representative builder | `0x004BC050` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x004BC050` writes opcode `0x26` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x4BBC8A` in `sub_4bba50`, reachable from `DialogPane::ChangePasswordDialogPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Field order, variants, state effects, and paired packets remain to be traced.

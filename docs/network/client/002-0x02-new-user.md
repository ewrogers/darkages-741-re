# New User (`CNewUser`)

| Field | Value |
| --- | --- |
| Direction | Client to server |
| Opcode | `0x02` (2) |
| Common transform | static |
| Representative builder | `0x0043D820` |
| Name provenance | The class name comes from related class vocabulary matched to the locally confirmed builder behavior. |

## Current evidence

The representative builder at `0x0043D820` writes opcode `0x02` as body byte 0 and reaches `net_submit_client_packet`.

No concrete derived client packet RTTI class exists in this binary. The display name is therefore kept separate from the locally verified opcode evidence.

## Known send sites

- `0x43F751` in `sub_43f410`, reachable from `TimerHandler::CreateUserDialogPane`.

## Plaintext body

```text
opcode:u8
... fields pending
```

Remaining fields, variants, and state effects remain to be traced.

The paired response is [New User Check (`SNewUserCheck`)](../server/001-0x01-new-user-check.md).

# New User (`CNewUser`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x02` (2) |
| Transform | `static` |
| Name provenance | Related class vocabulary matched to the locally confirmed builder and live creation flow |

## Purpose

This packet asks the lobby server to validate the account fields for a new character. It is the first half of the [character-creation flow](../../systems/character-creation.md).

`CreateUserDialogPane` reads the form, checks that the two password controls match, and schedules a short timer. `net_send_new_user_request` then builds and submits the request. The confirmation password is never transmitted.

The client has no derived packet RTTI for this name.

## Body

```text
packet CNewUser {
    u8      opcode                    // 0x02
    string8 name
    string8 password
    string8 account_text

    // Japan distribution mode 13 only
    u16     isp_selector
}
```

The active USA path sends `none` as `account_text`. A dormant NexonClub branch can assemble other account text, while Japan mode 13 exposes an email field and adds the ISP selector. See [Distribution markers](../../application/distribution-markers.md) for why those regional paths are dormant in this executable.

The ordinary submission path adds a final plaintext zero after this logical body before applying the static transform. The supplied decoded traces stop at the final field and do not show that common submission byte.

The live paired response uses server opcode `0x02`, documented on [Login or New User Check](../server/002-0x02-login-check.md). The creation pane also accepts server opcode `0x01` as a compiled alias.

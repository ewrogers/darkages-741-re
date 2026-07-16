# New User Appearance (`CNewUserAppearance`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x04` (4) |
| Encoding | startup key |
| Name provenance | Project-owner protocol name, confirmed against the accepted character-creation path |

## Purpose

The client sends this message for **new user appearance**.

After `SNewUserCheck` accepts command `0x02`, `net_handle_new_user_check` calls this builder. The four-byte body finalizes character creation with three appearance-related bytes from the create-user dialog.

The client has no derived packet RTTI for this name.

## Sent by

Known static callers lead to:

- UI or subsystem owner not known yet

## Body

```text
packet CNewUserAppearance {
    u8 opcode                 // 0x04
    u8 appearance_value_0
    u8 appearance_value_1
    u8 appearance_value_2
}
```

The exact meaning of the three appearance values remains to be named.

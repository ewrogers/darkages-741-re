# Group Toggle (`CGroupToggle`)

`CGroupToggle` switches whether the local character is open to group invitations. The packet contains no requested state. It tells the server to invert the current setting, then the client requests a fresh profile before changing the group icon.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2F` (47) |
| Encoding | derived |
| UI owner | RTTI class `BtmButtonsPane_A` |
| Builder | `net_send_group_toggle` |
| Name provenance | Project-owner protocol name, checked against the matching client builder and UI flow |

The client has no derived packet RTTI for this name.

## Body

```text
packet CGroupToggle {
    u8      opcode                    // 0x2F
}
```

The complete plaintext body is one byte. There is no boolean for open or closed.

## Client flow

The group-button action follows this order:

1. Mark the button action as pending without changing its displayed state.
2. Send `CGroupToggle`.
3. Send the empty [`CSelfLook`](045-0x2d-self-look.md) request.
4. Wait for [`SSelfLook`](../server/057-0x39-self-look.md).

`ui_bottom_buttons_apply_self_look` reads `SSelfLook.is_group_open`. Zero selects the closed icon state and a nonzero value selects the open state. `ui_bottom_buttons_set_group_invitation_state` then clears the pending action and redraws the pane.

This makes the icon server-authoritative. The click does not update it optimistically.

The one-second `CSelfLook` retry belongs to the initial profile load. Once that load has completed, this post-toggle refresh does not restart the retry state. If no new `SSelfLook` arrives, the existing icon remains until a later profile update.

## Supplied runtime trace

Both captured toggle cycles begin with the same two client packets:

```text
> 2F
> 2D
```

The captured server traffic that follows contains an [`SStatus`](../server/008-0x08-status.md) modifiers update, an [`SMessage`](../server/010-0x0a-message.md), and `SSelfLook`. The changing values are:

| Result | `SMessage` replacement row | `SSelfLook.is_group_open` |
| --- | --- | ---: |
| Invitations closed | `Join a group     :OFF` | `0` |
| Invitations open | `Join a group     :ON ` | `1` |

The `SMessage` has type `0x07`, a length of `0x0016`, and begins with ASCII `2`. That selector updates server-owned row 2 in `GameSettingDialog`; the remaining 21 bytes are the replacement row shown above. It does not update the bottom-button icon.

The `SStatus` body was identical in both cycles:

```text
08 04 00 00 00 00 00 00 00 06 06 01 25 00 00
```

Its `fields == 0x04` body is the ordinary combat-modifier block. It does not carry the invitation state and does not drive the group icon. The reason the server refreshes those modifiers after this action is not visible in the client.

One captured close cycle also contained `SMotion` before `SStatus`. It was not present in the open cycle, so it is not treated as a required response to `CGroupToggle`.

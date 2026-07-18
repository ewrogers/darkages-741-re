# Self Look (`CSelfLook`)

`CSelfLook` asks the server for the local character's profile. The request has no fields after its opcode. The server answers with [`SSelfLook`](../server/057-0x39-self-look.md), which carries the profile text, group state, class details, and legend marks.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2D` (45) |
| Transform | static |
| Runtime owner | `BtmButtonsPane_A` |
| Response | [`SSelfLook`](../server/057-0x39-self-look.md) |
| Name provenance | Project-owner protocol name, confirmed against the local builder and paired response handler |

## Plaintext body

```text
packet CSelfLook {
    u8      opcode                    // 0x2D
}
```

The complete plaintext body is one byte. `net_send_self_look` writes a zero immediately after the opcode in its temporary buffer, but submits a body length of one. That zero belongs to the common send-buffer sentinel handling and is not a `CSelfLook` field.

## Request flow

`BtmButtonsPane_A` sends `CSelfLook` as soon as it is constructed. While the initial profile request is pending, the pane schedules a one-second retry. `ui_bottom_buttons_handle_timer` sends the same empty request again when that timer fires.

One bottom-button action also sends [`CGroupToggle`](047-0x2f-group-toggle.md) and then requests a fresh profile. This lets the server return the updated group state in the next `SSelfLook`.

The button does not change its group icon optimistically. It keeps the action pending until `SSelfLook.is_group_open` supplies the server-authoritative state.

## Response

`ui_bottom_buttons_handle_network_event` recognizes server opcode `0x39` as `SSelfLook`. `ui_bottom_buttons_apply_self_look` updates the group-button state, cancels the retry timer, and clears the pending-profile flag.

The same response is consumed by `EquipPane`, `UserInfoPane`, `GroupAdPane`, and the legend panes to rebuild the visible character profile. No character ID or request option is needed because this request always refers to the local character.

The one-byte body, startup request, retry behavior, and direct `SSelfLook` pairing are confirmed in the version 741 binary.

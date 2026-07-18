# Show Paper (`SShowPaper`)

`SShowPaper` opens a paper window for reading only. It uses the same paper pane and visual backgrounds as `SEnterEditingMode`, but it carries no inventory slot and never returns edited content.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x35` (53) |
| Transform | `derived` |
| Name provenance | Project-owner protocol vocabulary, confirmed by the raw client handler and read-only paper flow |

## Body

```text
packet SShowPaper {
    u8              opcode                    // 0x35
    PaperBackground paper_background
    u8              width_blocks
    u8              height_blocks
    u8              center_text
    string16         content
}
```

All multibyte values are big-endian. `string16` is a `u16` byte count followed by exactly that many text bytes.

The block geometry matches [`SEnterEditingMode`](027-0x1b-enter-editing-mode.md):

```text
pane_width  = (width_blocks  + 2) * 16
pane_height = (height_blocks + 3) * 16
```

The pane is centered within the native `640×480` screen. [`PaperBackground`](../protocol-types.md#paperbackground) chooses only the visual skin.

## Read-only behavior

Opcode `0x35` has no server-packet factory entry. `net_dispatch_server_packet` recognizes the decoded opcode directly and calls `net_handle_show_paper_server_data`, which constructs the exact RTTI class `EditablePaperPane` with its local mode set to read-only.

That local mode disables the text editor and suppresses [`CExitEditingMode`](../client/035-0x23-exit-editing-mode.md). Its confirmed close action dismisses the pane without sending a client packet.

`center_text` is a boolean-style display field:

| Value | Layout |
| ---: | --- |
| `0` | Normal inset text area spanning the paper |
| Nonzero | Compact text area centered within the paper |

For the centered form, the client estimates text width as `content_byte_length * 6` pixels and centers that rectangle. This is a layout switch, not the flag that makes the pane read-only.

As with editable paper, incoming `0x09` bytes become carriage returns inside the text control, so tabs represent line breaks on the wire.

## What triggers it

The immediate client trigger is receipt of server opcode `0x35`. There is no client builder that requests `SShowPaper`, and the receive handler is not statically paired with a particular outgoing packet.

A server can therefore use it after an inventory action, dialog, script, or any other server-owned interaction. Receiving it after [`CUse`](../client/028-0x1c-use.md) is a plausible normal flow for readable items, but that item-policy decision cannot be confirmed from this client alone.

## Known limits

The client does not validate the background selector, block dimensions, or `center_text` value. To keep the centered pane within `640×480`, use at most 38 width blocks and 27 height blocks. The initial content passes through the same 1,024-byte bounded field as editable paper, so longer text is not reliably displayable.

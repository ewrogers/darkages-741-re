# Enter Editing Mode (`SEnterEditingMode`)

`SEnterEditingMode` opens an editable paper window for an inventory item. The server supplies its initial text, paper background, block dimensions, and the slot that the client must return when editing finishes.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x1B` (27) |
| Transform | `derived` |
| Name provenance | Project-owner protocol vocabulary, confirmed by the raw client handler and paired `CExitEditingMode` builder |

## Body

```text
packet SEnterEditingMode {
    u8       opcode                    // 0x1B
    u8       slot
    u8       paper_background          // PaperBackground
    u8       width_blocks
    u8       height_blocks
    string16 content
}
```

All multibyte values are big-endian. `string16` is a `u16` byte count followed by exactly that many text bytes.

The tentative `height` and `width` field names were reversed. The first dimension controls horizontal size and the second controls vertical size:

```text
pane_width  = (width_blocks  + 2) * 16
pane_height = (height_blocks + 3) * 16
```

The pane is centered within the client's native `640×480` screen. The extra two columns and three rows provide room for the paper border and controls.

[`PaperBackground`](../protocol-types.md#paperbackground) describes only the visual skin. Editing behavior is selected by the packet's handler, not by this byte.

## Opening the editor

Opcode `0x1B` has no server-packet factory entry or RTTI packet object. `net_dispatch_server_packet` recognizes the decoded opcode directly and gives the raw body to `net_handle_enter_editing_mode_server_data`.

The handler constructs the exact RTTI class `EditablePaperPane` in editable mode. The pane parses the fields, builds a text-edit control, lays out the paper, registers itself with the screen and event systems, and focuses the editor.

The background renderer uses `paper_background` as an asset-group selector for `Line001.epf`. Each group contains nine frames for the corners, edges, and interior of a stretchable paper skin. The selector does not affect the pane dimensions or whether its text is editable.

## Text representation and limits

Paper text is byte-oriented rather than Unicode. On receipt, the pane converts byte `0x09` to carriage return `0x0D` for the editor. [`CExitEditingMode`](../client/035-0x23-exit-editing-mode.md) converts carriage returns back to `0x09`, so tab bytes act as the wire representation of line breaks.

The packet parser first copies the declared content into an approximately 8,000-byte temporary buffer without checking the declared length. The text control then passes the initial value through its own 1,024-byte bounded field. Only 1,023 content bytes plus a terminator fit there, so longer initial content is not reliably displayable. A server should keep editable paper contents within that visible limit even though the wire length is `u16`.

## Closing and saving

The pane's close action sends `CExitEditingMode` with the retained slot and current text, then dismisses the pane immediately. It does not wait for a save acknowledgement.

The same RTTI pane is also used by [`SShowPaper`](053-0x35-show-paper.md) in read-only mode. Closing that form only dismisses it; it does not send `CExitEditingMode`.

## Known limits

The client does not range-check `paper_background` or the two block dimensions before using them for asset selection and geometry. The documented background values are the known supported skins. To keep the centered pane within `640×480`, use at most 38 width blocks and 27 height blocks.

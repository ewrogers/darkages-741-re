# Exit Editing Mode (`CExitEditingMode`)

`CExitEditingMode` submits the current contents of an editable paper item. The client sends it when the editable paper pane's close action runs, then closes the pane without waiting for a server acknowledgement.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x23` (35) |
| Transform | `derived` |
| Name provenance | Project-owner protocol vocabulary; the local builder and editable-paper UI flow are confirmed |

## Body

```text
packet CExitEditingMode {
    u8      opcode                    // 0x23
    u8      slot
    string16 content
}
```

All multibyte values are big-endian. The `slot` is copied from the [`SEnterEditingMode`](../server/027-0x1b-enter-editing-mode.md) request. The client does not return the paper background or its dimensions.

## Building the content

The builder reads the current text from the pane's text-edit control. It copies at most 8,000 bytes, writes that byte count as the `u16` string length, and appends the bytes.

Before sending, every carriage return byte `0x0D` is converted to `0x09`. The incoming editor performs the inverse conversion, so `0x09` is the paper protocol's line-break byte. The length counts encoded bytes, not characters or lines.

## Close behavior

`EditablePaperPane` action ID 0 is the confirmed submit-and-close path:

```text
close action
    -> copy and normalize edited text
    -> send CExitEditingMode
    -> unregister and dismiss the pane
```

The pane has a separate read-only mode used by [`SShowPaper`](../server/053-0x35-show-paper.md). Its close action skips the packet builder and dismisses the pane locally. Forced destruction also does not independently submit text; saving belongs to the editable pane's normal close action.

No response is required for the client to close the editor. The server remains responsible for validating the slot, content length, permissions, and persistence.

# Confirm (`CConfirm`)

`CConfirm` answers a two-button prompt created entirely by the server. The client sends it only from the exact RTTI class `UserConfirmPane`, after receiving `SMessage` type `0x11`.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x31` (49) |
| Transform | derived |
| UI owner | `UserConfirmPane` |
| Builder | `net_send_confirm` |
| Name provenance | Project-owner protocol name, confirmed against `UserConfirmPane` |

## Body

```text
packet CConfirm {
    u8      opcode                 // 0x31
    u8      dialog_value_0
    u8      choice
    u8      dialog_value_1
    string8 value
}
```

`choice` is `1` for OK and `0` for Cancel. Project-owner runtime testing confirms both values against the visible button labels. The client does not calculate the other fields. It echoes `dialog_value_0`, `dialog_value_1`, and `value` from the server prompt.

The roles of those three server-supplied values are not established. They may identify the prompt or carry operation-specific context, but the client treats them as opaque reply data.

## How the pane opens

Every typed server packet passes through `PacketPreprocessor` before normal pane-tree delivery. Its active path is:

```text
SMessage type 0x11
        |
        v
PacketPreprocessor consumes it
        |
        v
UserConfirmPane displays the main message
        |
        +-- OK     --> CConfirm choice 1
        `-- Cancel --> CConfirm choice 0
```

The `SMessage` prefix supplies the reply fields in this order:

```text
u8      dialog_value_0
u8      dialog_value_1
string8 value
```

Its later `u16`-counted main message becomes the visible alert text. That displayed text is not included in `CConfirm`.

The pane inherits `AlertPane`, which inherits `DialogPane`. It is constructed with two button assets and has one direct builder callback for each choice. There are no other static callers of `net_send_confirm` and no local menu or keyboard path that opens this pane without the server prompt.

## Why it may be absent from captures

The client path is live and has no distribution or configuration gate. It runs only when the server sends [`SMessage`](../server/010-0x0a-message.md) with `message_type = 0x11`. If the matching server does not use that message type, the pane never exists and opcode `0x31` cannot be produced through ordinary UI behavior.

The client has no derived packet RTTI for the name `CConfirm`. The exact `UserConfirmPane` name and opcode builder confirm the behavior, while the concrete packet name remains project-owner protocol vocabulary.

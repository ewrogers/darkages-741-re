# Event system

Events are the client's common message format. Mouse input, keyboard input, text, timers, decoded server packets, and app state changes all meet here.

An event is like a small envelope. Its type says which handler family should open it, and the remaining fields carry the details.

## Event shape

The shared event object is `0xA8` bytes. Only part of it is understood:

```text
struct Event {
    unknown header[0x0C]
    u32 type                    // +0x0C
    type-specific data[...]     // starts at +0x10
}
```

For a decoded server packet, the useful fields are:

```text
struct ServerEventData {
    bytes *body                 // event +0x14, starts with opcode
    u32 body_length             // event +0x18
    ServerPacket *parsed        // event +0x1C, null if no class exists
}
```

These layouts describe object-relative fields, not fixed runtime addresses.

## Event families

`event_dispatch` groups event types by purpose:

| Types | Family |
| --- | --- |
| `0x00` to `0x07` | Pointer and mouse input |
| `0x08` to `0x0C` | Keyboard and text input |
| `0x0D` to `0x12` | Window, focus, and IME input |
| `0x13` | Decoded server packet |
| `0x14` | Intro state change |

The first four families can travel through the pane tree. Intro state events go straight to `event_handle_intro_state`.

## Dispatch flow

```text
producer
  |
  +-- main thread? -- yes --> event_dispatch
  |                    no --> copy to queue
  |                              |
  +------------------------------+
                                 v
                       next dispatcher tick
                                 |
                    captured pane or pane tree
```

`event_dispatch_pane_subtree` visits children before their parent. Returning true means the event was handled, so traversal stops. This is similar to offering input to the topmost child node before its container.

Mouse capture is a shortcut. While a pane owns capture, pointer events go directly to it instead of searching the whole tree.

Capture also sends keyboard and application events to that pane. Network events continue through the normal pane tree.

## Network events

`net_post_decoded_server_packet_event` creates type `0x13` after transport decryption. During dispatch, the client may build a typed server packet object. Packets without a registered class can still be handled directly by a pane or manager.

This keeps network code and gameplay code loosely joined. The socket only delivers a decoded message. The event system decides which game screen or manager sees it.

## Timers

Timers use the same main-thread tick but are stored separately from normal events. A due timer calls its `TimerHandler` callback. `event_dispatcher_tick` handles at most 40 due timers per pass.

A `Pane` contains a secondary `TimerHandler` base at offset `0x11C`. Because of that inheritance layout, a timer callback may receive a pointer adjusted to that base. This detail matters when naming callbacks or building hooks.

The complete event type table, pane handler slots, timer entry, and tree-entry layout are in [Pane and event layouts](../appendix/runtime/panes.md).

## Known limits

- Some event fields are still unnamed.
- Pointer-bearing event variants should not be copied across process boundaries until their ownership rules are known.
- Registration, visibility, focus, and mouse capture are separate states. A hidden pane may still be registered.

Addresses and confidence notes are in the [function reference](../appendix/functions.md).

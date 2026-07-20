# Event system

Events are the client's common message format. Mouse input, keyboard input, text, timers, decoded server packets, and app state changes all meet here.

An event is like a small envelope. Its type says which handler family should open it, and the remaining fields carry the details.

## Event shape

The shared event object is `0xA8` bytes. Its common header is now mostly understood:

```text
struct Event {
    void *vtable                // +0x00, Event methods inherited from LObject
    u32 live_cookie             // +0x04, raw bytes "bosy" while live
    u32 unobserved_08           // +0x08, purpose not established
    s8 type                     // +0x0C, starts as -1
    u8 reserved_0d[3]           // +0x0D, not read in the traced paths
    u8 data[0x98]               // +0x10, family-specific payload
}                               // total size 0xA8
```

The vtable is the object's method lookup table. Both it and the cookie come from the shared `LObject` base. `lobject_ctor` writes the cookie as the four bytes `62 6F 73 79`, which read as `bosy`, and `lobject_dtor` clears it to zero. `event_dispatch_immediate` checks the cookie through `lobject_is_live` and refuses to dispatch an object that is no longer live.

The type is one signed byte, not a four-byte integer. The constructor writes `-1` as its unset value, and producers replace that byte with a type from the table below. The three bytes after it only carry the layout forward to the four-byte-aligned payload at `+0x10` in every traced path.

The word at `+0x08` remains deliberately named `unobserved_08`. The event constructor and destructor do not initialize it. None of the 25 stack-based construction sites, family checks, or central dispatch paths read or write it. Queueing still copies it because the queue copies the entire `0xA8`-byte object. A stack event can therefore carry an indeterminate value there, so code should not expect zero or attach meaning to it yet.

For a decoded server packet, the useful fields are:

```text
struct ServerEventData {
    bytes *body                 // event +0x14, starts with opcode
    u32 body_length             // event +0x18
    ServerPacket *parsed        // event +0x1C, null if no class exists
}
```

These layouts describe object-relative fields, not fixed runtime addresses.

## Construction and queueing

Most producers construct an `Event` on the stack, set its signed type byte, fill the matching payload fields, and call `event_dispatch_or_queue`.

Main-thread events are dispatched immediately. Events from another thread are copied into a synchronized queue. The dispatcher keeps a separate pool of reusable `Event` objects for that queue, but the pool stores pointers outside the objects. Neither allocation nor recycling uses `Event +0x08` as a link.

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

## Server-controlled input blocking

[`SBlockInput`](../network/server/081-0x51-block-input.md) opens the RTTI-backed `ClockPane` as a modal wait cursor. The pane follows pointer movement and returns true for pointer plus keyboard/text events, so those events stop before reaching ordinary UI and world handlers.

The block is represented by the live `ClockPane` singleton rather than a player or world-state flag. Beginning a block also emits button-up events for any held left or right mouse buttons. Ending it removes the pane and restores the normal cursor. Timers and network events continue throughout the block.

## Network events

`net_post_decoded_server_packet_event` creates type `0x13` after transport decryption. During dispatch, the client may build a typed server packet object. Packets without a registered class can still be handled directly by a pane or manager.

This keeps network code and gameplay code loosely joined. The socket only delivers a decoded message. The event system decides which game screen or manager sees it.

## Timers

Timers use the same main-thread tick but are stored separately from normal events. A due timer calls its `TimerHandler` callback. `event_dispatcher_tick` handles at most 40 due timers per pass.

A `Pane` contains a secondary `TimerHandler` base at offset `0x11C`. Because of that inheritance layout, a timer callback may receive a pointer adjusted to that base. This detail matters when naming callbacks or building hooks.

The complete event type table, pane handler slots, timer entry, and tree-entry layout are in [Pane and event layouts](../appendix/runtime/panes.md).

## Known limits

- The purpose of `unobserved_08` is not established. It is preserved by whole-object copies but unused by the confirmed event lifecycle.
- Many fields inside the family-specific payload union are still unnamed.
- Pointer-bearing event variants should not be copied across process boundaries until their ownership rules are known.
- Registration, visibility, focus, and mouse capture are separate states. A hidden pane may still be registered.

Addresses and confidence notes are in the [function reference](../appendix/functions.md).

# Hooks and injection

The safest hook points expose logical data before the client transfers ownership or applies transport transforms. This page records the version-741 contracts needed for monitoring, blocking, replacement, and injection.

## Hook matrix

| Hook | Address | ABI | Block result | Replacement lifetime |
|---|---:|---|---|---|
| `input_dispatch_event` | `0x4647C0` | `u8 __thiscall(void *app, void *event)` | Skip original, return `1` | Event is client-owned; copy anything retained |
| `net_queue_received_packet_bytes` | `0x467060` | `void __stdcall(const void *body, int length)` | Skip original | Original copies synchronously |
| `net_submit_client_packet` | `0x563E00` | `void __thiscall(void *communications, const u8 *body, s16 length)` | Skip original | Original copies synchronously |
| `net_poll_receive` | `0x564300` | `void __thiscall(void *communications)` | Not a policy hook | Proxy queue owns commands until drained |
| `input_client_window_proc` | `0x4A9C30` | Win32 `WNDPROC` | Return a result for the private proxy message only | Proxy queue owns commands until drained |
| `app_shutdown` | `0x4AC060` | `void __cdecl(void)` | Call original after proxy teardown | No new work after entry |

`input_dispatch_event_through_pane_tree` at `0x464D50` is useful for pane diagnostics, but it is recursive and may observe one logical event more than once. It is not the primary event hook.

## Central logical event hook

Every final logical event reaches `input_dispatch_event` on the main thread. The event object is `0xA8` bytes and begins with this confirmed common header:

```c
struct InputEventHeader {
    void *vtable;       /* +0x00, normally 0x674018 */
    u8 unknown_04[8];
    s8 type;            /* +0x0C */
};
```

Confirmed families are:

| Types | Family | Pane vtable slot |
|---|---|---:|
| `0..7` | Pointer | `+0x48` |
| `8..0x0C` | Keyboard, text, and IME | `+0x4C` |
| `0x13` | Decoded network receive | `+0x50` |
| `0x0D..0x12` | Other application events | `+0x54` |

Important layouts are:

| Family | Offset | Field |
|---|---:|---|
| Pointer | `+0x10` | Logical X |
| Pointer | `+0x14` | Logical Y |
| Pointer | `+0x18` | Modifier and held-button mask |
| Pointer | `+0x20` | Win32 message time |
| Pointer | `+0x24`, `+0x28` | Original coordinate copies |
| Keyboard | `+0x10` | Mapped key byte |
| Keyboard | `+0x11` | Modifier byte |
| Keyboard | `+0x14` | Win32 message time |
| Character `0x0B` | `+0x14` | Win32 message time |
| Character `0x0B` | `+0x1C` | Character byte followed by NUL |
| Network `0x13` | `+0x14` | Decoded body pointer beginning with opcode |
| Network `0x13` | `+0x18` | Decoded body length |
| Network `0x13` | `+0x1C` | Optional deserialized packet object |

The central dispatcher may translate pointer coordinates and may create and release the optional server-packet object. Observe before the original call when policy needs the untouched event.

### Blocking and cleanup

Returning `1` means consumed. The caller, `input_dispatch_event_on_main_thread` at `0x463F70`, still performs payload cleanup after the central dispatcher returns.

For network event type `0x13`, the caller frees the raw buffer at `+0x14` with the communications object's allocator. The central dispatcher owns only the temporary packet object at `+0x1C`. A hook that blocks the event must not free either field.

Use decoded ingress for network-body replacement. Replacing a network pointer inside the central event risks mixing allocation domains and cleanup rules.

## Decoded SPacket ingress

`net_queue_received_packet_bytes` is called after a complete frame has been transformed. Its input is:

```text
[u8 opcode] [payload...]
```

The supplied length includes the opcode and excludes the local trailing zero. The function rejects nonpositive lengths, allocates `length + 1`, copies the body, appends zero, and constructs event type `0x13`.

The binary frame parser calls it at `0x5673D5` and `0x56767A`. The legacy parser calls it at `0x566E69` and `0x566FB1`.

This is the preferred SPacket policy hook:

- Monitoring sees plaintext logical packet bytes.
- Blocking skips event construction after the frame has already been consumed.
- Replacement may use proxy-owned memory for the duration of the original call because the original makes its own copy.
- Length and opcode checks can run before client allocation.

Equivalent hook logic:

```c
void hook_server_body(const u8 *body, int length)
{
    RuleResult result;

    if (proxy_reentrant()) {
        original_server_body(body, length);
        return;
    }

    result = evaluate_server_rules(body, length);
    publish_server_event(body, length, &result);

    if (result.action == RULE_BLOCK)
        return;

    if (result.action == RULE_REPLACE)
        original_server_body(result.body, result.length);
    else
        original_server_body(body, length);
}
```

### SPacket injection

Execute this adapter through the communications command pump:

```c
net_queue_received_packet_bytes(body, length);
```

The adapter uses the client's allocator, creates the correct event, and queues a full `0xA8` copy to the main thread because the call originates on the communications worker. Normal event cleanup later releases the raw body.

Do not fabricate a network event with a proxy-heap pointer at `+0x14`. The client will free that field through its own allocator.

## Logical CPacket egress

`net_submit_client_packet` receives the untransformed logical body:

```text
[u8 opcode] [payload...]
```

The signed 16-bit length includes the opcode and excludes the local zero sentinel. The function:

1. Applies the transfer gate at communications offset `+0x780DE`. When set, only opcode `0x10` is accepted.
2. Adds the seven-byte dialog wrapper for opcodes `0x39` and `0x3A`.
3. Appends a zero sentinel.
4. Queues communications event 6.

The normal practical maximum input length is 32766 because the queued length includes the sentinel. For `0x39` and `0x3A`, it is 32760 because the queued representation grows by seven bytes. Native callers are assumed to provide positive lengths.

This is the preferred CPacket policy hook. The original copies before returning, so a replacement body only needs to remain valid during the call.

### CPacket injection

The simplest compatible adapter is:

```c
communications = *(void **)((u8 *)module_base + 0x0033D958);
net_submit_client_packet(communications, body, (s16)length);
```

Run it on a dedicated bounded proxy producer, not the controller I/O thread. The native queue is synchronized but can wait when full.

Do not invoke this adapter on the communications worker. A full native queue can make the worker wait for itself.

A later worker-affine adapter may call `net_send_client_packet` at `0x5648A0` directly, but only after reproducing the exact submission normalization. Passing a raw logical body directly is wrong because the sender expects the sentinel-appended representation and the special dialog wrapper where applicable.

## Input injection

There are two useful input fidelity levels.

### Win32-faithful input

Post normal window messages to the HWND at `0x73D938`:

- `WM_KEYDOWN`, `WM_KEYUP`, `WM_SYSKEYDOWN`, and `WM_SYSKEYUP`
- `WM_CHAR`
- `WM_MOUSEMOVE`, button transitions, and `WM_MOUSEWHEEL`

This path preserves the client's scan-code translation, held-key state, modifier state, double-click detection, coordinate scaling, and IME behavior. Construct `lParam` fields as Windows would, including scan code and transition bits for keyboard events.

### Internal logical input

For deterministic logical events, post a proxy command to the main-thread pump and call an existing emitter there:

| Address | Emitter |
|---:|---|
| `0x4672F0` | `input_emit_mouse_move_event` |
| `0x4673F0` | `input_emit_left_button_down_event` |
| `0x467680` | `input_emit_left_button_up_event` |
| `0x467790` | `input_emit_right_button_down_event` |
| `0x467A20` | `input_emit_right_button_up_event` |
| `0x467B30` | `input_emit_mouse_wheel_event` |
| `0x467C10` | `input_emit_key_down_event` |
| `0x467E30` | `input_emit_key_up_event` |
| `0x467FE0` | `input_emit_char_event` |

These functions update input-manager state as well as dispatching. Their complete argument types are not yet proven, so validate each call signature from native callers before exposing it as a controller command.

## Raw socket telemetry

Raw Winsock hooks are useful for byte-for-byte capture and connection lifecycle monitoring. The target imports Winsock 1.1 by ordinal.

| Operation | IAT slot | Thunk | Known call sites |
|---|---:|---:|---|
| `connect`, ordinal 4 | `0x669480` | `0x6042A2` | Transport initialization |
| `closesocket`, ordinal 3 | `0x669488` | `0x604296` | Disconnect paths |
| `recv`, ordinal 16 | `0x669484` | `0x60429C` | `0x5670D5`, `0x567430`, `0x567910`, plus startup probing |
| `send`, ordinal 19 | `0x669490` | `0x60428A` | Binary send at `0x564A67`, legacy sends, and startup probing |

Prefer IAT replacement when complete process-local raw telemetry is required. Preserve Winsock return values, short reads or writes, `SOCKET_ERROR`, and `WSAGetLastError` behavior.

Do not inject fabricated ciphertext through `recv` or call `send` with a plaintext body. The logical adapters preserve framing, transform state, sequence state, and client ownership.

## Reentrancy and provenance

Mark injected commands with proxy-owned metadata outside client buffers. Use a thread-local guard to prevent an injected packet from being re-evaluated indefinitely by the same hook. Telemetry should still record whether an event was native, injected, replaced, or replayed.

Never place proxy metadata inside the packet body unless it is part of the actual protocol.

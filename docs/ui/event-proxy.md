# Injected event proxy design

The verified event and network boundaries are sufficient for an injected proxy that observes or blocks events locally and accepts commands over IPC. The proxy should reuse native client producers instead of fabricating pointer-bearing `Event` variants.

The example implementation is under [`examples/event-proxy/`](../../examples/event-proxy/README.md). It is an architecture skeleton, not a finished injector or detour library.

## Hook and execution boundaries

| Boundary | Static address | RVA | Proxy role |
| --- | ---: | ---: | --- |
| `event_dispatch` | `0x004647C0` | `0x000647C0` | Observe or consume logical events before pane propagation |
| `event_dispatcher_tick` | `0x00464180` | `0x00064180` | Drain bounded IPC commands on the client main thread |
| `net_submit_client_packet` | `0x00563E00` | `0x00163E00` | Observe, block, or submit opcode-first client plaintext |
| `net_post_decoded_server_packet_event` | `0x00467060` | `0x00067060` | Copy opcode-first server plaintext into an owned type `0x13` event |

These are 32-bit MSVC-style functions. An `event_dispatch` detour uses an x86 `__fastcall` bridge for the original `__thiscall`, with the dispatcher in `ECX`, an unused bridge value in `EDX`, and `Event *` on the stack. The same bridge pattern applies to the tick and client-send hooks.

All addresses must be resolved as `module base + RVA`. The launcher should verify the complete executable fingerprint. The DLL should also validate the expected hook prologues before attaching.

## IPC architecture

The pipe thread validates fixed binary messages and copies accepted commands into a bounded queue. It never invokes client code. The tick hook drains that queue after the normal dispatcher tick, preserving the client main-thread requirement.

Rules remain inside the injected DLL as atomic allow, observe, or block values indexed by event type or packet opcode. Hooks consult the current rule without waiting for the controller. Telemetry goes through a separate bounded queue and is dropped on contention or overflow.

Persistent rules use YAML. The controller parses [`rules.example.yaml`](../../examples/event-proxy/rules.example.yaml) and sends compact rule updates. The DLL does not parse YAML from a hook.

## Native event construction

`input_get_event_manager` at `0x00427380` returns the live `EventMan`. The following public wrapper layer preserves input blocking, held-button state, modifier tables, double-click synthesis, and IME state:

| Event | Native entry | Construction |
| --- | ---: | --- |
| Pointer move | `input_post_pointer_move`, `0x00466C80` | `EventMan *`, x, y, message time |
| Left button down/up | `0x00466D10` / `0x00466D50` | `EventMan *`, message time; coordinates come from stored pointer state |
| Right button down/up | `0x00466D80` / `0x00466DC0` | Same stored-coordinate behavior |
| Mouse wheel | `input_post_mouse_wheel`, `0x00466DF0` | `EventMan *`, raw Win32 wheel delta, message time |
| Key down/up | `0x00466E20` / `0x00466E60` | `EventMan *`, scan code, composition-active state, message time, virtual key |
| Character | `input_post_character`, `0x00466E90` | One byte and message time |
| Committed text | `input_post_committed_text`, `0x00466ED0` | NUL-terminated bytes, copied to a maximum of `0x7F` |
| IME open state | `input_post_ime_open_status_change`, `0x00466EB0` | Open value and message time |
| IME start/end | `0x00466EF0` / `0x00466F30` | Message time |
| IME candidate close | `0x00466F80` | Message time |

A click command should normally be preceded by a pointer-move command. Button producers use `EventMan` coordinates already stored at `+0x10` and `+0x14`.

The corresponding event constructors populate the `0xA8` tagged `Event` and call `event_dispatch_or_queue`. For example, pointer events fill type at `+0x0C`, x and y at `+0x10` and `+0x14`, input flags at `+0x18`, wheel units at `+0x1C`, and message time at `+0x20`. Text producers copy their bytes into the inline region beginning at `+0x1C`.

Candidate-list data type `0x10` is intentionally excluded from generic IPC construction. It contains pointer-bearing data with specialized cleanup. The real Win32 IME producer remains the safe construction route.

## Packet construction

A client command carries the exact opcode-first plaintext body documented on the matching client packet page. The tick hook calls `net_submit_client_packet` with the live pointer stored at static address `0x0073D958`. The normal queue, framing, sequence, and transform stages remain downstream.

A server command also carries an opcode-first decoded body. `net_post_decoded_server_packet_event` allocates from the client's packet pool, copies the body, appends a zero byte, and posts a normal type `0x13` event. The packet factory and pane handlers therefore see the same owned representation as a decoded socket packet.

This server path does not advance receive encryption, sequence state, or handshake state. It is appropriate for handler and UI testing, not for replacing stateful transport traffic.

## Blocking and cleanup

Returning true from the `event_dispatch` hook marks an event consumed and prevents normal pane traversal. The caller still returns through `event_dispatch_immediate`, which releases an owned server body and the known IME allocations. Blocking should occur before the proxy invokes any parser or partially mutates the event.

Client-packet blocking returns without entering `net_submit_client_packet`. Defaults should remain fail-open. Synthetic commands should pass through the same rules unless explicitly marked to bypass them. High-impact authentication, key-transition, world-transition, and `SBadGuy` traffic should be denied for synthetic server injection by default.

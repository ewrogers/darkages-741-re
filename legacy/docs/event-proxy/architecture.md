# Event proxy architecture

An event proxy for this client should observe at logical boundaries and execute client calls on their owning threads. The minimum reliable design has a controller transport, a policy engine, a main-thread command queue, and a communications-side command path.

The client remains the owner of its native queues, packet transforms, allocators, event objects, and socket state.

## Required hook layers

| Layer | Primary hook | Thread | Purpose |
|---|---|---|---|
| Logical event | `event_dispatch` at `0x4647C0` | Main | Observe or consume all input, network, and application events |
| Decoded ingress | `event_post_socket_bytes` at `0x467060` | Communications during native receive | Observe, block, replace, or inject decoded SPacket bodies |
| Logical egress | `net_submit_client_packet` at `0x563E00` | Producer thread | Observe, block, or replace untransformed CPacket bodies |
| Main execution | `input_client_window_proc` at `0x4A9C30` | Main | Drain commands posted with a private registered window message |
| Communications execution | `net_poll_receive` at `0x564300` | Communications | Drain bounded commands after a worker wake |
| Lifecycle | `app_shutdown` at `0x4AC060` | Main | Stop acceptance, drain work, and remove hooks before object destruction |

The logical event, decoded ingress, and logical egress hooks provide the useful policy boundaries. Raw Winsock hooks are optional diagnostics, not substitutes for them.

## Thread model

```text
controller I/O
    |
    +--> bounded main-command queue
    |       |
    |       +--> PostMessageA(private_message)
    |               |
    |               +--> input_client_window_proc detour
    |
    +--> bounded communications-command queue
            |
            +--> ReleaseSemaphore(communications + 0x14)
                    |
                    +--> worker vslot +0x10
                            |
                            +--> net_poll_receive detour
```

The controller transport must not call client functions directly. It only validates and copies commands into bounded proxy-owned queues.

### Main-thread wake

Register a process-unique message with `RegisterWindowMessageA`. Post that message to the window stored at `0x73D938`. The window-procedure detour handles it before calling the original procedure and drains a bounded number of commands.

Standard `WM_KEY*`, `WM_CHAR`, and `WM_MOUSE*` messages may also be posted directly when Win32-faithful input is desired.

`event_dispatcher_tick` at `0x464180` is a viable fallback pump, but a private window message gives an explicit wake and avoids adding work to every idle tick.

### Communications-thread wake

The worker's primary semaphore handle is at communications offset `+0x14`. `util_worker_thread_loop` checks the native ring after a wake. If the ring is empty, it skips the native pop and still calls vtable slot `+0x10`, which is `net_poll_receive`.

The proxy can therefore enqueue its own command, release that semaphore once, and drain the proxy queue in a `net_poll_receive` detour. Drain a fixed number per call so native receive cannot starve.

Do not insert synthetic records into the client's native ring. Its record layout is only partly understood, and its queue has its own blocking and ownership rules.

## Queue and backpressure rules

Use separate, bounded queues for commands and telemetry. Hooks must never wait for the controller.

- Monitoring records may be dropped when their telemetry queue is full. Count and report drops.
- Policy commands must receive an explicit busy or timeout result instead of silently disappearing.
- Copy packet and event data before leaving the hook. Client-owned pointers have short lifetimes.
- Do not hold a client lock while serializing or sending controller data.
- Use a thread-local reentrancy guard around hooks that can be reached by injected work.

The native communications queue is synchronized and safe for normal foreign producers, but it waits when all 128 records are occupied. A dedicated proxy producer may call `net_submit_client_packet`, but the controller I/O thread and game-owned threads must not be exposed to that wait.

Calling `net_submit_client_packet` from the communications worker is not robust. If the native queue fills concurrently, the worker can wait for itself. A communications-thread adapter that calls `net_send_client_packet` directly must first reproduce all `net_submit_client_packet` normalization, including the `0x39` and `0x3A` wrapper and the trailing zero sentinel.

## Policy ordering

For each hook, use this order:

1. Check the reentrancy guard and pass through internal proxy calls when required.
2. Validate the observed length and copy the minimum data needed by policy.
3. Evaluate local, already-published rules only.
4. Emit telemetry without waiting.
5. Pass, replace, or consume.

Rules must be local to the injected component. A synchronous round trip to an external controller from a hook can freeze input, rendering, or socket progress.

## Failure behavior

Failure should preserve the native client whenever possible.

- If target validation fails, install no hooks.
- If a nonessential hook cannot be installed, disable only its capability and report it.
- If the controller disconnects, use a configured fail-open or fail-closed policy. Fail-open is safer for early development.
- If a replacement packet is invalid, reject the controller command and leave the native event unchanged.
- If shutdown begins, stop accepting commands before draining and unhooking.

## Shutdown sequence

The `app_shutdown` detour should perform this sequence once:

1. Mark the proxy as stopping.
2. Stop accepting new controller commands.
3. Wake both proxy execution paths.
4. Cancel or drain queued commands with explicit results.
5. Stop controller and telemetry workers.
6. Wait until active hook counters reach zero.
7. Restore detours and IAT entries.
8. Call the original `app_shutdown`.

`event_manager_dtor` at `0x466A80` is the last object-level boundary before the communications object is deleted. It is useful as a defensive assertion or last-chance gate, but process shutdown should begin at `app_shutdown`.

## Recommended implementation phases

1. Validate the target and install monitoring-only hooks.
2. Add local blocking at the three logical boundaries.
3. Add main-thread input commands.
4. Add decoded SPacket injection through the communications pump.
5. Add CPacket injection through a dedicated producer.
6. Add an optional direct communications-thread sender only after the normalization adapter is tested against native output.
7. Add optional raw Winsock telemetry.

Exact contracts and injection adapters are in [Hooks and injection](hooks-and-injection.md). Target constants are in [Version profiles](version-profiles.md).

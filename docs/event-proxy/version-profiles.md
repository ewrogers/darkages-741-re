# Version profiles

Addresses in an injected component must be selected by an exact executable profile. Reported version text is not enough.

## Version 741 identity

```text
File: Darkages.exe
Size: 3,112,960 bytes
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
Machine: 32-bit x86
Preferred image base: 0x400000
Reported client version: 741
```

The installed executable used for this analysis matched this size and hash on 2026-07-13.

For relocation-safe code, store relative virtual addresses and resolve them from the loaded module base:

```c
void *resolve_rva(void *module_base, u32 rva)
{
    return (u8 *)module_base + rva;
}
```

## Core hook profile

| Capability | Static VA | RVA | Whole-instruction prefix | Bytes |
|---|---:|---:|---:|---|
| Central logical event | `0x4647C0` | `0x000647C0` | 5 | `55 8B EC 6A FF` |
| Decoded SPacket ingress | `0x467060` | `0x00067060` | 6 | `55 8B EC 83 EC 08` |
| Logical CPacket egress | `0x563E00` | `0x00163E00` | 6 | `55 8B EC 83 EC 38` |
| Communications pump | `0x564300` | `0x00164300` | 9 | `55 8B EC 81 EC 1C 01 00 00` |
| Main window procedure | `0x4A9C30` | `0x000A9C30` | 6 | `55 8B EC 83 EC 34` |
| Main idle/event pump | `0x464180` | `0x00064180` | 5 | `55 8B EC 6A FF` |
| Process shutdown | `0x4AC060` | `0x000AC060` | 9 | `55 8B EC 81 EC E0 00 00 00` |
| EventMan destructor | `0x466A80` | `0x00066A80` | 5 | `55 8B EC 6A FF` |

The prefix length is the shortest verified sequence of complete x86 instructions large enough for a five-byte relative jump. A detour implementation must relocate those instructions into its trampoline and must not assume that the byte count is portable to another build.

## Supporting functions

| Name | Static VA | RVA | Role |
|---|---:|---:|---|
| `event_dispatcher_queue_event_copy` | `0x463D10` | `0x00063D10` | Copy a complete `0xA8` event into the synchronized queue |
| `event_dispatcher_process_event` | `0x463F70` | `0x00063F70` | Central call plus payload cleanup |
| `event_dispatch_or_queue` | `0x4670F0` | `0x000670F0` | Direct on main thread, copy from other threads |
| `event_queue_socket_packet` | `0x468220` | `0x00068220` | Build network event type `0x13` |
| `input_run_message_pump` | `0x4AC750` | `0x000AC750` | Main `PeekMessageA` loop |
| `net_dispatch_communications_event` | `0x5643D0` | `0x001643D0` | Native communications-event switch |
| `net_send_client_packet` | `0x5648A0` | `0x001648A0` | Transform, frame, and physically send |
| `net_receive_binary_framed_data` | `0x567070` | `0x00167070` | Binary receive and frame parser |
| `net_enqueue_communications_event` | `0x586210` | `0x00186210` | Native ring push plus semaphore release |
| `util_worker_thread_loop` | `0x586350` | `0x00186350` | Generic wait, dispatch, and periodic callback loop |

## Globals and vtables

| Symbol | Static VA | RVA | Validation |
|---|---:|---:|---|
| Main HWND, `hWndParent` | `0x73D938` | `0x0033D938` | Null before window creation, then a valid HWND |
| `event_dispatcher_instance` | `0x73D944` | `0x0033D944` | Object vtable is `0x673F68` |
| `event_dispatcher_singleton` | `0x6D9220` | `0x002D9220` | Mirrors the EventDispatcher object after construction |
| `event_manager_instance` | `0x6D9260` | `0x002D9260` | Object vtable is `0x674024` |
| `net_communications_instance` | `0x73D958` | `0x0033D958` | Object vtable is `0x684CC0` |
| `app_main_thread_id` | `0x740400` | `0x00340400` | Set by the main message loop |
| `event_dispatcher_vtable` | `0x673F68` | `0x00273F68` | Slot `+0x08` is `event_dispatcher_tick` |
| `event_vtable` | `0x674018` | `0x00274018` | Used by `event_ctor` |
| `event_manager_vtable` | `0x674024` | `0x00274024` | Used by `event_manager_ctor` |
| `net_communications_vtable` | `0x684CC0` | `0x00284CC0` | Slot `+0x10` is `0x564300` |

Compare vtable pointers after adding the module relocation delta. Static values are only valid at the preferred base.

## Communications layout

| Offset | Type | Meaning |
|---:|---|---|
| `+0x14` | `HANDLE` | Primary queue semaphore, suitable for a proxy wake |
| `+0x54` | pointer | Native synchronized ring |
| `+0x60` | `HANDLE` | Worker thread handle |
| `+0x64` | `u32` | Worker thread ID |
| `+0x74` | pointer | Event sink, EventMan |
| `+0x480CC` | `SOCKET` | Active TCP socket or `INVALID_SOCKET` |
| `+0x780DE` | `u8` | Transfer gate for outbound packets |
| `+0x780E0` | pointer | Client allocator used for packet buffers |

The object size passed during construction is `0x780E4`. The native ring is configured for `0x80` records of `0x18` bytes.

## Winsock import profile

The executable imports `WSOCK32` functions by Winsock 1.1 ordinal.

| Operation | Ordinal | IAT static VA | IAT RVA | Thunk static VA |
|---|---:|---:|---:|---:|
| `closesocket` | 3 | `0x669488` | `0x00269488` | `0x604296` |
| `connect` | 4 | `0x669480` | `0x00269480` | `0x6042A2` |
| `recv` | 16 | `0x669484` | `0x00269484` | `0x60429C` |
| `send` | 19 | `0x669490` | `0x00269490` | `0x60428A` |
| `WSAAsyncSelect` | 101 | `0x669494` | `0x00269494` | `0x604284` |

## Semantic validation

Hash validation is primary. Before enabling each capability, also validate the structure it depends on:

1. Confirm the PE is x86 and its loaded image covers every required RVA.
2. Compare the complete hook prefix, not only the first opcode.
3. Confirm core globals point into readable memory after startup.
4. Confirm the EventDispatcher, EventMan, and communications vtables match this profile after relocation.
5. Confirm communications vtable slot `+0x10` resolves to `net_poll_receive`.
6. Confirm the WndProc address registered during startup resolves to `input_client_window_proc`.
7. Confirm WSOCK32 IAT slots still name the expected ordinals before replacing them.

If any core identity check fails, install no hooks. If an optional capability such as raw socket telemetry fails its local checks, leave that capability disabled while keeping independently validated logical hooks available.

Do not scan for a nearby prologue and assume it is equivalent. Semantic checks prevent a partial match from turning into a call-convention or ownership error.

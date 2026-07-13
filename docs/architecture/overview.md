# Client architecture overview

The version-741 client has two important execution domains: the main Win32 thread and one communications worker. Input, UI routing, timers, and final logical-event dispatch run on the main thread. Socket receive, frame decoding, packet transforms, and physical send run on the communications worker.

This split determines where monitoring and injection code may safely run.

## Object graph

`startup_initialize_client` at `0x4A9F80` constructs the application dispatcher first, then the input manager and communications object.

| Static address or offset | Meaning |
|---:|---|
| `0x73D938` | Main window handle, currently named `hWndParent` in IDA |
| `0x73D944` | Published application dispatcher pointer, `app_instance` |
| `0x6D9220` | Second published application pointer, `app_singleton` |
| `0x6D9260` | Input manager pointer, `input_manager_instance` |
| `0x73D958` | Communications object pointer, `net_communications_instance` |
| `0x740400` | Main thread ID, `app_main_thread_id` |
| input manager `+0x0C` | Owned communications object |
| communications `+0x480CC` | TCP socket |

The application object is `0x1BC` bytes. The input manager is `0x45C` bytes. The communications object is `0x780E4` bytes.

## Main thread

`input_run_message_pump` at `0x4AC750` uses `PeekMessageA`. A Win32 message is translated by `input_client_window_proc` at `0x4A9C30` and `input_translate_win32_message` at `0x48E980`. Mouse, keyboard, character, and IME messages become the client's own `0xA8`-byte event objects.

When the Win32 queue is empty, application vtable slot `+0x08` calls `input_process_main_thread_events_and_timers` at `0x464180`. That function:

1. Drains copied events from the synchronized application queue.
2. Dispatches each event on the main thread.
3. Processes up to 40 due timers.

The final common routing point is `input_dispatch_event` at `0x4647C0`. It routes focused or modal panes first, then the visible pane hierarchy. Network receive is event type `0x13`, so decoded packets join the same main-thread event system as input.

## Communications worker

`net_socket_ctor` at `0x563910` builds the communications object on top of a reusable worker base. The base owns a synchronized native queue and a semaphore. Its worker loop is `util_worker_thread_loop` at `0x586350`.

The queue has 128 records of `0x18` bytes each. A producer calls `net_enqueue_communications_event` at `0x586210`, which pushes a record and releases the semaphore. A full queue makes the producer wait.

The communications vtable maps these worker callbacks:

| Vtable offset | Address | Role |
|---:|---:|---|
| `+0x0C` | `0x586350` | Generic worker loop |
| `+0x10` | `0x564300` | `net_poll_receive` periodic callback |
| `+0x14` | `0x5643D0` | Dispatch a queued communications event |
| `+0x18` | `0x564550` | Synchronous query handler |
| `+0x1C` | `0x5645B0` | Additional wait-handle callback |

After every wait cycle, including a semaphore wake with no native queue record, the worker calls vtable slot `+0x10`. This makes `net_poll_receive` a useful communications-thread execution pump.

## Receive flow

```text
WSOCK32 recv
  -> net_receive_binary_framed_data (0x567070)
  -> net_decrypt_server_packet_body (0x567DE0)
  -> net_queue_received_packet_bytes (0x467060)
  -> net_wrap_received_packet_message (0x468220)
  -> input_dispatch_or_queue_event (0x4670F0)
  -> synchronized 0xA8 event copy
  -> input_process_main_thread_events_and_timers (0x464180)
  -> input_dispatch_event (0x4647C0)
```

`net_queue_received_packet_bytes` receives a decoded logical body beginning with the opcode. It allocates `length + 1` bytes from the client allocator, copies the body, and appends a zero byte. The wrapper places that buffer at event offset `+0x14`, the logical length at `+0x18`, and an initially null packet object at `+0x1C`.

`input_dispatch_or_queue_event` compares the current thread ID with `app_main_thread_id`. Events produced by the communications worker are copied into the synchronized queue. Main-thread producers dispatch directly.

## Send flow

```text
packet builder
  -> net_submit_client_packet (0x563E00)
  -> communications event 6
  -> net_dispatch_communications_event (0x5643D0)
  -> net_send_client_packet (0x5648A0)
  -> transform and 0xAA framing
  -> WSOCK32 send
```

`net_submit_client_packet` is the last common logical CPacket boundary. It applies the transfer gate, adds the special wrappers for opcodes `0x39` and `0x3A`, appends the local zero sentinel, and queues a client-owned copy. The communications worker later transforms and sends that copy.

## Shutdown order

`app_shutdown` at `0x4AC060` is the process-level shutdown boundary. At `0x4AC2B3` it deletes the input manager, which destroys the communications object and worker before the application dispatcher is deleted.

The worker base destructor at `0x585DA0` can use `TerminateThread`. Any injected work, hooks, or controller queues must therefore stop and drain before the original shutdown path destroys the input manager.

See [Event proxy architecture](../event-proxy/architecture.md) for the implementation consequences and [version profiles](../event-proxy/version-profiles.md) for exact addresses and validation bytes.

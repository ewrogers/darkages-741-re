# Event proxy design

An injected event proxy could act like a small adapter between the client and another local process. It would observe selected events, apply fast local rules, and queue new work for the next game tick.

The design does not need to replace packet encryption. Client packets enter before encryption, and server packets enter after decryption.

```text
controller process
      |
      | local IPC
      v
injected proxy queues
      |
      +-- commands --> main-thread tick --> native client functions
      |
      +-- telemetry <-------------------- observed events
```

## Hook points

Three functions cover the first useful version:

- `event_dispatch` observes common client events and decoded server packets.
- `net_submit_client_packet` observes or blocks client sends before framing and encryption.
- `event_dispatcher_tick` drains proxy commands on the main thread.

The proxy should call the original function unless a local rule explicitly blocks the item.

## Main-thread command queue

The IPC thread must not call pane or game functions directly. It only validates a command and puts it in a bounded queue.

```text
on IPC command
    validate type and size
    copy command into bounded queue

on event_dispatcher_tick
    drain a small command budget
    call the matching native producer
    run the original tick
```

Native producers such as `input_post_pointer_event`, `input_post_keyboard_event`, and `input_post_text_event` preserve the client's normal event construction and ownership rules.

## Packet commands

For a client send, the controller supplies an opcode-first plaintext body. The proxy passes it to `net_submit_client_packet`; the normal client adds its sequence, transform, and TCP frame.

For a simulated server message, the controller supplies a decoded opcode-first body. The proxy uses `net_post_decoded_server_packet_event`, which sends it through the normal event and pane path.

Simulated server messages do not advance the real receive cipher or network session. They are best used for UI experiments and controlled tests, not as a replacement transport.

## Local rules

Blocking must be decided inside the injected process. Waiting for the controller would stall the game loop.

```yaml
rules:
  - channel: client_packet
    opcode: 0x71
    action: observe
  - channel: keyboard
    key: F12
    action: block
```

If rule loading fails, the proxy should fail open and keep the client working. Command and telemetry queues need fixed limits. When telemetry is full, drop observations instead of blocking the game.

## Safe first scope

The first version only needs:

- pointer, keyboard, and text events
- common application events
- decoded server packets
- plaintext client sends

Events that contain borrowed pointers should stay out of generic IPC until their copy and cleanup behavior is known.

Exact hook addresses are kept in the [function reference](../appendix/functions.md). This page is a design guide, not a ready-to-load DLL.

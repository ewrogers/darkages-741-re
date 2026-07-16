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

## Default and live rules

The proxy loads its default rules from YAML when the DLL starts. Every rule needs a stable ID so a controller can refer to it later.

```yaml
rules:
  - id: observe_alive
    enabled: true
    priority: 100
    channel: client_packet
    opcode: 0x71
    action: observe

  - id: block_f12
    enabled: false
    priority: 200
    channel: keyboard
    key: F12
    action: block
```

The loaded rules become the first live rule set. Runtime changes affect memory only. They do not rewrite the YAML file. If a user wants to keep a change, the controller should save a new YAML file outside the injected DLL.

Resetting the rules discards runtime changes and reloads the defaults.

## Rule control over IPC

The controller can manage the live rule set with these commands:

| Command | Result |
| --- | --- |
| `rule.list` | Return the active rules and current revision. |
| `rule.add` | Add a rule with a new ID. |
| `rule.edit` | Replace one rule while keeping its ID. |
| `rule.remove` | Remove a rule from the live set. |
| `rule.enable` | Enable a rule. |
| `rule.disable` | Disable a rule. |
| `rule.reset_defaults` | Reload the default YAML rules. |

An edit should send the complete replacement rule. This is easier to validate than a list of small field changes.

```yaml
command: rule.edit
request_id: 42
expected_revision: 7
rule:
  id: block_f12
  enabled: true
  priority: 200
  channel: keyboard
  key: F12
  action: block
```

The controller includes the revision it last read. The proxy rejects a stale edit instead of overwriting a newer change.

```yaml
request_id: 42
ok: true
revision: 8
```

The wire format may be a small fixed binary message even though the saved rules use YAML. The command names and behavior should stay the same.

## Publishing rule changes

IPC parsing still happens outside the hooks. A control command follows this path:

```text
controller
   |
   v
IPC thread: parse and check message shape
   |
   v
bounded control queue
   |
   v
main-thread tick: clone, validate, and apply
   |
   v
publish new rule snapshot and send reply
```

Hooks read one immutable snapshot. They never edit the rule table, take an IPC lock, or wait for the controller. After a change, the proxy publishes the new snapshot in one swap and keeps the old snapshot alive until existing readers are finished.

Each accepted change increments the revision. A rejected change leaves both the active rules and revision untouched. Validation should check the rule ID, channel, action, match fields, opcode range, and total rule limit.

## Rule order and failure behavior

Only enabled rules run. Higher priority rules run first. `observe` records the event and continues. `allow` and `block` stop evaluation, so the first matching terminal action wins. If no terminal rule matches, the event is allowed.

If default loading, IPC parsing, or a runtime edit fails, the proxy keeps the last valid snapshot and fails open. Command and telemetry queues need fixed limits. When telemetry is full, drop observations instead of blocking the game.

## Safe first scope

The first version only needs:

- pointer, keyboard, and text events
- common application events
- decoded server packets
- plaintext client sends

Events that contain borrowed pointers should stay out of generic IPC until their copy and cleanup behavior is known.

Exact hook addresses are kept in the [function reference](../appendix/functions.md). This page is a design guide, not a ready-to-load DLL.

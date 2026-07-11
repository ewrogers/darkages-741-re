# Input subsystem

The client converts Win32 window messages into its own event objects before UI or game code sees them. The same dispatcher also carries network and other application messages, which is why input routing shares infrastructure with packet delivery.

The main path is:

```text
input_run_message_pump (0x4AC750)
  -> input_client_window_proc (0x4A9C30)
     -> input_translate_win32_message (0x48E980)
        -> input_emit_*_event (0x4672F0 and nearby)
           -> net_dispatch_or_queue_received_message (0x4670F0)
              -> net_dispatch_received_message (0x4647C0)
                 -> focused or modal pane
                 -> visible pane tree
                 -> world handlers when not consumed
```

The two `net_` names in this diagram are older project names. The functions submit and dispatch generic client messages, not only network packets.

## Pages

- [Win32 message routing](win32-message-routing.md)
- [Internal events, focus, and modals](internal-events-and-focus.md)
- [Keyboard behavior and outgoing packets](keyboard-and-packets.md)
- [Mouse behavior and world interaction](mouse-and-world.md)

## Address convention

Addresses are static virtual addresses for the preferred image base `0x400000`. See the project [address convention](../README.md#address-convention) before using them as runtime addresses.

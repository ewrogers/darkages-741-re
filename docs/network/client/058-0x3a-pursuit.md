# Pursuit (`CPursuit`)

`CPursuit` moves an NPC conversation backward, forward, or through an answered step. It returns the target, pursuit, and destination step from the active [`SPursuitMessage`](../server/048-0x30-pursuit-message.md), followed by an optional typed argument.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x3A` (58) |
| Transform | Dialog-response inner wrapper, then `static` |
| Name provenance | Project-owner protocol vocabulary; behavior confirmed by local dialog RTTI and builders |

The client has no derived packet RTTI class for `CPursuit`.

## Body

```text
packet CPursuit {
    u8  opcode                         // 0x3A
    u8  target_type
    u32 target_id
    u16 pursuit_id
    u16 step_id

    if bytes_remaining > 0 {
        u8 argument_type
        if argument_type == 1 {
            u8 choice_number
        }
        if argument_type == 2 {
            string8 text
        }
    }
}
```

All multibyte values are big-endian. The no-argument body is exactly ten bytes before the inner wrapper. `argument_type` is absent for navigation and close, not zero on the wire.

| Argument type | Meaning |
| ---: | --- |
| `1` | Menu choice, followed by a one-based choice number |
| `2` | Text answer, followed by `string8` bytes |

## Step rules

The client calculates `step_id` from the current server message:

| UI action | Sent step | Argument |
| --- | ---: | --- |
| Previous | Current minus 1 | None |
| Next | Current plus 1 | None |
| Close | Current | None |
| Select menu row | Current plus 1 | Type 1 and row index plus 1 |
| Submit text | Current plus 1 | Type 2 and entered text |
| Submit protected form | Current plus 1 | Type 2 manager-result text after local approval |

The server's `has_previous` and `has_next` bytes only enable the two buttons. They do not carry explicit destination steps. Arithmetic on the `u16` is performed by the client.

Every confirmed navigation and answer builder asks `NPCSession` to enter response-pending after queuing `CPursuit`. The client deactivates the nested answer pane, disables Previous and Next, and clears the default action while leaving Close available. The server continues the conversation by sending the requested `SPursuitMessage` step.

The outer pursuit pane registers Close as both attachment-order action 6 and its Escape cancel action. Either input sends the no-argument current-step body, then closes the NPC session locally. Nested menu and input panes return false for Escape so the outer pane can handle it.

## Simple-dialog speech echo

Two pursuit types send another packet immediately before `CPursuit`:

- Type 3 sends [`CSay`](014-0x0e-say.md) with the selected menu text.
- Type 5 sends `CSay` with `input_prolog + " " + text + " " + input_epilog`.

The subsequent `CPursuit` remains the ordinary type-1 or type-2 response. Servers that reproduce the simple-dialog flow should expect both packets in that order.

## UI producers

The current `NPC_Pursuit_MessageDialog` owns Previous, Next, and Close. Its question and input subtypes build answer packets through the common header helper. The older compiled `MessageDialogBase` family independently emits the same previous, current, next, menu, and text forms. Exact RTTI classes include:

- `QuestionMessageDialog`
- `QuestionMessageFaceDialog`
- `SimpleQuestionMessageDialog`
- `TextMessageDialog`
- `SimpleTextMessageDialog`

This second implementation confirms the argument values and step rules. See [NPC dialogs](../../systems/npc-dialogs.md) for the active pane construction and input path.

## Inner wrapper

`CPursuit` and `CMerchant` are the only opcodes selected by the special branch in `net_submit_client_packet`. The client first builds the [dialog-response inner wrapper](../packet-transforms.md#dialog-response-inner-wrapper), then applies the ordinary startup-key transform selected for opcode `0x3A`.

```text
CPursuit body
    -> dialog-response inner wrapper
    -> normal static transform for opcode 0x3A
    -> frame
```

This is not evidence that `CMerchant` and `CPursuit` use the same outer key. They share the inner wrapper but retain their different command-selected outer transforms.

## Paired packet

[`SPursuitMessage`](../server/048-0x30-pursuit-message.md) supplies every field used by the confirmed builders and selects whether navigation, menu, text, speech echo, or protected input is available.

## Known limits

Argument values other than 1 and 2 are not emitted by any recovered client builder. The protected ID/password controls are handed to a regional account manager. Only its successful state reaches `net_send_pursuit_protected_text_result`, which sends the manager-produced nonempty string rather than directly concatenating the two edit fields. That account policy is separate from the packet layout.

The `target_id` is always a `u32`. Observed reactor IDs may fit in three bytes, but an injected sender must preserve and write all four bytes. A type-10 `SPursuitMessage` body is only `30 0A`; any additional byte shown by a transport or logging layer is not part of the deserialized packet body.

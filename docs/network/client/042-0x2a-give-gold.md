# Give Gold (`CGiveGold`)

`CGiveGold` asks the server to transfer a chosen amount of gold to another living object. The client opens an amount dialog when the player drags the gold inventory entry onto another player, an NPC, or a monster.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x2A` (42) |
| Transform | derived |
| Runtime owners | `InvItemPane`, `GiveGoldDialogPane`, and `WorldPane` |
| Name provenance | Project-owner protocol name, confirmed against the local builder |

## Plaintext body

```text
packet CGiveGold {
    u8      opcode                    // 0x2A
    u32     amount
    u32     object_id
}
```

The body is 9 bytes including the opcode. Both fields after the opcode are big-endian 32-bit integers.

## Choosing the target

The target follows the same living-object drag path as [`CGive`](041-0x29-give.md). The client rejects the local character's own object ID, then returns the selected living object's ID to the source `InvItemPane` through TimerHandler event `1`.

Inventory slot `60` selects gold. Instead of sending immediately, `ui_inventory_item_handle_timer` constructs `GiveGoldDialogPane` and gives it the selected `object_id`.

## Dialog flow

`GiveGoldDialogPane` uses the `_nmoney.txt` controls and focuses the amount input. Action `0` parses and submits the amount. Action `1` closes the dialog without sending.

A parsed amount of zero also closes the dialog without sending. For a nonzero amount, `net_send_give_gold` writes `amount` first and the retained `object_id` second.

The client-side path does not compare the requested amount with the character's current gold before building the packet. Any insufficient-gold rejection is therefore a server decision.

## Server outcome

The matching success and rejection responses have not yet been traced. The body, living-object target path, self-target rejection, dialog actions, zero-amount behavior, and field order are confirmed in the version 741 binary.

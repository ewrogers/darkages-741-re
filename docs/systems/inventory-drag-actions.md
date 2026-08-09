# Inventory drag actions

Dragging an inventory entry into the world can produce four different client packets. The choice depends on whether the source is an ordinary item or the gold entry in slot 60, and whether the release target is a map tile or a living object.

The drag itself does not send a packet. It identifies a target, queues a small event back to the source inventory item, and lets that item choose the packet or amount prompt.

## Flow

```text
InvItemPane pointer drag
        |
        v
DraggedInvItemPane release
        |
        +-- map tile ------> TimerHandler event 0: packed X/Y
        |                         |
        |                         +-- slot 1..59 --> CDrop
        |                         +-- slot 60 ----> DropGoldDialogPane --> CDropGold
        |
        +-- living object -> TimerHandler event 1: object ID
                                  |
                                  +-- slot 1..59 --> CGive
                                  +-- slot 60 ----> GiveGoldDialogPane --> CGiveGold
```

`ui_inventory_item_handle_pointer_event` starts the drag after the pointer leaves the small drag threshold around the press point. It creates exact RTTI `DraggedInvItemPane`, which retains the source `InvItemPane` and displays a temporary copy of its icon.

On release, `ui_dragged_inventory_item_dispatch_drop` sends the drag record and pointer position through the pane tree. The temporary drag pane is then removed independently of whether a target consumed the release.

## Dropping on a map tile

`ui_world_pane_handle_inventory_drop` accepts the release only when the pointer is inside the world pane and `ui_world_pane_screen_to_tile` produces coordinates inside the current map. It does not check distance from the local character.

The handler queues TimerHandler event `0` to the source item. The event payload packs target X in the high 16 bits and target Y in the low 16 bits. The inventory callback unpacks the coordinates on the main thread.

For ordinary items, `ui_inventory_item_handle_timer` sends quantity `1` immediately unless the entry is stackable and its stored quantity exceeds one. A stack opens the numeric input pane with the range `0` through the stored quantity. A nonzero answer reaches `ui_inventory_item_submit_drop_quantity`; zero cancels.

Slot `60` is the synthetic gold entry. It opens exact RTTI `DropGoldDialogPane`, retains the selected X and Y, and reads a nonzero amount from the shared `_nmoney.txt` controls before sending [`CDropGold`](../network/client/036-0x24-drop-gold.md).

## Dropping on a living object

The living-object route covers the human and monster branches used by other players, NPCs, and monsters. `ui_world_pane_handle_living_object_message` rejects the local character's own object ID, then queues TimerHandler event `1` to the source item with the selected object ID.

For an ordinary item, the live drag path sends [`CGive`](../network/client/041-0x29-give.md) with quantity `1`. The packet supports a full `u32` quantity, and `ui_inventory_item_submit_give_quantity` can forward another nonzero value, but no static reference connects that callback to the live drag path. The version 741 UI therefore does not confirm a stack-quantity prompt for giving items.

For slot `60`, the callback opens exact RTTI `GiveGoldDialogPane`. The dialog retains the object ID and sends [`CGiveGold`](../network/client/042-0x2a-give-gold.md) only when its parsed amount is nonzero.

## Packet submission queue

All four paths end at `net_submit_client_packet`. Ordinary packet bodies are copied into client-owned memory, gain the common transmitted zero byte, and are queued as communications command `6`. `net_queue_communications_command` copies the command record into the socket FIFO and releases the network-worker semaphore. The worker later selects the opcode's transform, adds the frame, and writes it to the connection.

This means the UI and the network worker do not share a temporary stack buffer. Submission is asynchronous, but the builders and the shared transport still touch game-owned state and must be entered from the main game thread.

## Calling the actions without dragging

Use the narrow native packet builder when it already accepts the desired values. This keeps the client's packet construction, local guards, and queue handoff while avoiding pointer hit testing and temporary drag panes. Direct body submission is the fallback for a builder whose inputs are trapped in UI state, not the default for every action.

The ordinary item builders are usable when the caller resolves the live `InvItemPane` for the requested slot:

- `net_send_drop(item, target_y, target_x, quantity)` builds [`CDrop`](../network/client/008-0x08-drop.md). Its native X and Y argument order is reversed from the wire order.
- `net_send_give(item, object_id, quantity)` builds [`CGive`](../network/client/041-0x29-give.md).

The two gold builders are poor supplied-value entry points. They require live dialog objects and parse their attached text controls. A controller that already has an amount and target should validate the amount, build the nine-byte opcode-first `CDropGold` or `CGiveGold` body, and pass it to `net_submit_client_packet`.

The exact x86 calling contracts, RVAs, slot checks, packet bodies, and main-thread rules are in [Manual native actions](../appendix/runtime/manual-actions.md).

## Known limits

The client-side branches, field order, queue handoff, and quantity behavior are statically confirmed in the version 741 executable. The direct-call contracts have not yet been exercised by an in-game injected dispatcher. The server can still reject a locally valid slot, quantity, coordinate, or object ID.

# Mouse behavior and world interaction

## Pointer flags

World pointer events carry the current modifiers plus button-state bits:

| Bit | Meaning |
|---:|---|
| `0x01` | Alt |
| `0x02` | Ctrl |
| `0x04` | Shift |
| `0x10` | Left button held |
| `0x20` | Right button held |

`input_world_pane_handle_pointer_event` at `0x5CE4E0` is the WorldPane pointer vtable method. It forwards into the world layer, where hit testing separates object actions from ground actions.

## Ground actions

`input_handle_world_ground_pointer_event` at `0x5EFBE0` converts the logical screen point to a map tile.

| Input | Exact condition in this handler | Result |
|---|---|---|
| Right-button down | Neither Ctrl nor Shift is held | Reset movement sync and start click-to-move pathfinding to the tile |
| Shift+right-button down | Flags equal `0x24` | Choose a direction from the cursor quadrant and use the normal turn-or-move routine |
| Ctrl+right-button down | Flags include `0x22` | No recovered ground action |
| Ctrl+Shift+right-button down | Flags include `0x26` | No recovered ground action |

The Shift+right path divides the world pane around its center to choose one of the four direction IDs. It does not send a unique packet. It reaches `CChangeDir` or `CMove` through the same direction routine used by the keyboard.

## Object actions

`input_handle_world_object_action` at `0x5EF120` handles a hit-tested object:

| Input path | Target condition | Result | Immediate packet |
|---|---|---|---|
| Ctrl+left-click | Another category-1 user | Open local `PopupMenuPane` | None |
| Left-click | Self | Run the self-object local action | Not established |
| Left-click | Another object | Request its bubble or object information | `CObjectInfoRequest` `0x43`, subtype `1` |
| Object action type `6` | Another object | Move toward an adjacent tile, turn, or attack when already adjacent | Movement, turn, or attack packets as needed |

The Ctrl branch only tests the Ctrl bit. Shift+left-click therefore follows the ordinary object-info path unless a child pane consumes it earlier.

`input_open_object_popup_menu` at `0x54BDB0` constructs the pane. Visual C++ RTTI confirms the class name `PopupMenuPane`; its constructor is `ui_popup_menu_pane_ctor` at `0x54C010`. Packet effects from each popup-menu choice still need to be traced separately.

`net_send_c_object_info_request` at `0x5F4730` builds this plaintext body:

```text
43 01 object_id:u32be
```

## Move toward an object

`input_move_to_world_object` at `0x5F4A70` finds the target and its four adjacent tiles. If the self player is already adjacent, the client turns toward the target or attacks when already facing it. Otherwise it computes a path to an adjacent tile and records the target ID and position for continued processing.

This is a client-side convenience path. The server still receives ordinary `CMove`, `CChangeDir`, and `CAttack` packets rather than a special click-to-object packet.

## Double-click and wheel

EventMan generates separate left and right double-click event types. Whether they cause an action depends on the pane under the pointer. The mouse wheel is similarly converted into internal type `7` and routed to the focused or hit-tested pane before the world.

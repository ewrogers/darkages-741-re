# Manufacturing manuals

The manufacturing window is a server-fed recipe browser. The server opens it with a recipe count, the client requests one recipe at a time, and crafting sends the displayed recipe name back to the server.

## Packet flow

```text
SManual RecipeCount
        |
        v
ManufactureDialogPane opens
        |
        +---- CManual RequestRecipe(index 0)
        |                 |
        |                 v
        |           SManual Recipe
        |                 |
        |                 v
        |        recipe is drawn in pane
        |                 |
        +---- NEXT/PREV --+
        |
        +---- OK --> CManual CraftRecipe(name, optional slot)
```

[`SManual`](../network/server/080-0x50-manual.md) is opcode `0x50`. [`CManual`](../network/client/085-0x55-manual.md) is opcode `0x55`. Both use the derived packet transform.

## Pane and layout

The exact RTTI class `ManufactureDialogPane` derives from `DialogPane` and `Singleton<ManufactureDialogPane>`. Its active constructor loads `lmanu.txt` and registers the pane as a modal dialog.

The constructor attaches controls in this order:

| Action ID | Named control | Role |
| --- | --- | --- |
| `0` | `OK` | Send `CraftRecipe` |
| `1` | `CANCEL` | Close locally |
| `2` | `NEXT` | Request the next recipe |
| `3` | `PREV` | Request the previous recipe |
| `4` | `NUM` | Show one-based position and count |
| `5` | `TILE` | Draw the recipe icon |
| `6` | `NAME` | Show the recipe name |
| `7` | `DESC` | Show the description |
| `8` | `INGREDIENT` | Show the ingredient text |
| `9` | `ADDITIONAL` | Optional inventory-item drop target |

The numeric action IDs come from attachment order, not the order of definitions in `lmanu.txt`. Only IDs `0` through `3` are buttons handled by the pane.

The local `setoa.dat` entry contains 11 layout blocks. `Noname` is the 288 by 259 dialog background and uses frame 0 of `manufac.spf`; it is not attached as a control. `PREV` and `NEXT` use the two states in `manuprev.spf` and `manunext.spf`. The recipe icon and additional-item target are 32 by 32 canvases on the left, while the name, description, and ingredient text occupy the right side.

## Opening a manual

The global packet owner creates the pane only for `SManual RecipeCount` and only when the manufacture singleton is absent. A recipe detail sent before the count message does not create a window.

The two-byte `manufacture_id` is session context, but its low byte has concrete inventory behavior. It is the one-based slot of the item that owns or opened the manual. The pane requires that item to exist and closes if the server removes it. Both ID bytes are echoed unchanged in every `CManual`.

For a nonzero count, the pane immediately requests recipe index `0`. The pane keeps only the current recipe; it requests another record whenever the player navigates.

## Recipe display and navigation

Each recipe supplies a zero-based index, a tagged sprite, a name, a description, ingredients, and an additional-item mode. The pane displays the position as `index + 1` over the server count and enables `PREV` or `NEXT` only when an adjacent index exists.

The button actions move one recipe at a time. Four keyboard event values provide the same navigation with deltas `-1`, `+1`, `-10`, and `+10`. The larger jumps clamp to the first or last valid index. The recovered event values are `0x80`, `0x82`, `0x93`, and `0x94`; their user-facing key labels have not yet been verified.

## Additional item slot

The final byte of `SManual Recipe` was missing from the supplied dummy-session model. Value `1` enables inventory-item drops onto `ADDITIONAL`.

When an item is dropped, the pane copies its image into the target and records the source item's one-based inventory slot. Clicking the target clears the selection. `SAddInventory` and `SRemoveInventory` updates also clear a selected slot when its item changes or disappears, preventing a stale slot from being sent.

`CManual CraftRecipe` ends with that selected slot. Zero means that no additional item was supplied. The client does not enforce that an item is present; the server remains responsible for validating the recipe and inventory.

## Crafting and closing

`OK` sends the current recipe name as `string8`, followed by the additional slot. The recipe index is not part of the craft request. The pane stays open and does not predict success, consume ingredients, or show a manufacture-specific result.

`CANCEL` destroys the pane without sending a packet. Removing the source manual item also closes it. These rules mean a server implementation should report craft success or failure through inventory updates and ordinary message packets rather than expecting a separate `SManual` completion variant.

## Known limits

- The high byte of `manufacture_id` is preserved but not interpreted by this pane.
- Only additional-item mode `1` has confirmed behavior.
- The exact game actions that cause the server to send the first `RecipeCount` are server-owned and are not recoverable from the client packet flow alone.
- A duplicate raw-body manufacture constructor exists in the binary, but no live static caller was recovered. The documented path uses the typed `SManual` object.

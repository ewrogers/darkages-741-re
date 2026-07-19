# Manual (`SManual`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x50` (80) |
| Transform | derived |
| Internal name | Exact RTTI class `SManual` |
| UI owner | Exact RTTI class `ManufactureDialogPane` |

## Purpose

The server uses this packet to open and feed the manufacturing recipe window. A `RecipeCount` message starts a session. The client then asks for one recipe at a time with [`CManual`](../client/085-0x55-manual.md), and a `Recipe` message fills the window.

The `SManual` deserializer and the manufacture pane both branch on the same values:

| `message_type` | Name | Meaning |
| --- | --- | --- |
| `0x00` | `RecipeCount` | Start or reset the manual and supply its recipe count |
| `0x01` | `Recipe` | Supply one recipe for display |

## Body

```text
packet SManual {
    u8       opcode                    // 0x50
    u16      manufacture_id
    u8       message_type
    if message_type == 0x00 {
        u8   recipe_count
    }
    if message_type == 0x01 {
        u8       recipe_index
        u16      sprite
        string8  recipe_name
        string16 recipe_description
        string16 ingredients
        u8       additional_item_mode
    }
}
```

The supplied dummy-session shape was correct through `ingredients`, but the version 741 client reads one more byte. `additional_item_mode == 1` enables the `ADDITIONAL` inventory-item drop target. No other value has a confirmed meaning.

`sprite` is the tagged wire value. The pane converts it to an icon-bank index when drawing. A server library that exposes `SpriteFlags.ClearFlags(...)` is applying a post-parse normalization and should not confuse that normalized value with the literal two bytes sent on the wire.

## Manufacture identifier

The client preserves `manufacture_id` as two bytes and echoes both bytes in every `CManual`. The pane treats the low byte as a one-based inventory slot:

- The opening packet is accepted only while that slot contains an item.
- Removing the source item closes the window.
- The high byte is preserved and echoed, but this pane does not otherwise interpret it.

This is stronger than treating the field as an arbitrary dialog ID, but the high byte's server-side meaning remains unknown.

## Client behavior

Only `RecipeCount` can create `ManufactureDialogPane`. If the singleton is already open, later `SManual` packets reach its network-event handler instead.

For a valid source slot, the pane stores `recipe_count`. When the count is nonzero, it immediately sends `CManual RequestRecipe` for zero-based index `0`. A zero count leaves the pane open with its empty `0/0` display.

A `Recipe` response replaces the current display with:

- `recipe_index + 1` over `recipe_count`
- the recipe icon
- name, description, and ingredients
- the optional additional-item mode

The description and ingredient displays retain at most 1024 text bytes each. The packet reader still advances over the full declared `string16` length when a value is longer.

Unknown `message_type` values have no recognized variant body. The deserializer reads only the common header and the pane does not apply the message.

## Paired packet

[`CManual`](../client/085-0x55-manual.md) requests a recipe by index or asks the server to craft the displayed recipe by name. The full UI flow is documented in [Manufacturing manuals](../../systems/manufacturing.md).

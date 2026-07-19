# Manual (`CManual`)

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x55` (85) |
| Transform | derived |
| Name provenance | Project-owner protocol name, confirmed by `ManufactureDialogPane` and `SManual` |
| UI owner | Exact RTTI class `ManufactureDialogPane` |

## Purpose

The manufacturing window sends this packet for two actions. It requests one recipe by zero-based index, or it asks the server to craft the recipe currently displayed.

| `action` | Name | Meaning |
| --- | --- | --- |
| `0x00` | `RequestRecipe` | Request one recipe record by index |
| `0x01` | `CraftRecipe` | Craft by recipe name and optional inventory slot |

The client has no derived packet RTTI for `CManual`. The name is project-owner protocol vocabulary; the two builders independently confirm the action values and bodies.

## Body

```text
packet CManual {
    u8       opcode                    // 0x55
    u16      manufacture_id
    u8       action
    if action == 0x00 {
        u8   recipe_index
    }
    if action == 0x01 {
        string8 recipe_name
        u8      additional_inventory_slot
    }
}
```

The supplied dummy-session shape omitted one meaningful trailing byte from `CraftRecipe`. `additional_inventory_slot` is the one-based slot of the item dropped into the `ADDITIONAL` control, or zero when no item is selected.

`manufacture_id` is copied byte-for-byte from [`SManual`](../server/080-0x50-manual.md). Its low byte is the source inventory slot used by the client. The high byte remains opaque to this pane.

## Request flow

After `SManual RecipeCount` supplies a nonzero count, the client sends `RequestRecipe(0)`. The `NEXT` and `PREV` controls request adjacent indexes. Keyboard paths also request indexes one or ten positions away, clamped to the valid range.

Recipes are not cached by the pane. Navigation asks the server for each selected record again.

## Craft flow

Pressing `OK` sends `CraftRecipe` with the displayed `recipe_name`. It does not send `recipe_index`. If the recipe enabled the additional-item target, the user may drag an inventory item into that control and the request includes its slot.

The client does not close the pane after sending a craft request and performs no local success calculation. Inventory changes and ordinary server messages provide the outcome. Pressing `CANCEL` closes the pane locally and sends no `CManual` close action.

The complete pane and control behavior is documented in [Manufacturing manuals](../../systems/manufacturing.md).

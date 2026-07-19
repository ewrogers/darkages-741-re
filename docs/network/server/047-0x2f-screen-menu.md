# Screen Menu (`SScreenMenu`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x2F` (47) |
| Encoding | session key |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet to open several menu-shaped dialogs. A subtype selects the dialog family, and the remaining fields provide its prompt, choices, or inventory-slot references.

The constructor calls `net_server_packet_base_ctor` with opcode `0x2F` and installs the `SScreenMenu` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

## Body

```text
packet SScreenMenu {
    u8      opcode                    // 0x2F
    ...                         // fields pending
}
```

The complete shared body and every subtype still need to be traced.

## NPC illustration owner

`NPCSession` consumes this packet and reads a speaker name plus an illustration index from the subtype-specific body. It resolves those fields through `NPCIllustFileMan`; failure falls back to the NPC tile. See [NPC dialog illustrations](../../systems/npc-dialog-illustrations.md). The complete field order still needs to be traced before it can be added to the body schema above.

## Client inventory menus

The screen-menu dispatcher accepts subtypes 0 through 11. Subtypes 5 and 11 both construct the exact RTTI class `ClientItemMenuDialog`.

This dialog reads a one-based inventory slot for each row. It resolves that slot against the live client inventory, ignores inactive item records, and passes the live item name to `ItemListPane` separately from the slot used as the selection value. In the unmodified client, it does not add the live stack quantity to that name.

The dispatcher, dialog constructor, and row builder run when the response constructs the list. They are not repaint callbacks. Runtime probes must be armed before a fresh response is triggered; installing them after the dialog is already visible can leave every counter at zero.

The [show inventory quantities in screen menus](../../appendix/runtime-patches/show-inventory-quantities-in-screen-menus.md) runtime patch intercepts only that row-builder call. Server item menus, skill menus, spell menus, and NPC menu classes are not changed.

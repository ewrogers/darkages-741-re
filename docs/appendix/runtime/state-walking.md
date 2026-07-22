# Runtime state walking

Client state can be read reliably from a small set of lifetime-owned roots. The safest model is to walk those roots on the game thread, copy the useful values into an owned snapshot, and let other code read only that snapshot. Do not retain client object pointers after the walk.

This page is the entry point for character, map, entity, and UI state. The linked layout pages remain the source of truth for complete field definitions.

## Address rules

These addresses apply only to the documented version 741 executable. Verify its fingerprint before using them.

```text
preferred image base: 0x00400000
SHA-256: 054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6
```

The table gives static Binary Ninja addresses and module-relative RVAs. At runtime, resolve a static address as `loaded_module_base + RVA`. Object offsets are then relative to the resolved object pointer.

| Root | Static address | RVA | Stored value |
| --- | ---: | ---: | --- |
| Event dispatcher | `0x006D9220` | `0x002D9220` | `EventDispatcher *` |
| Equipment pane | `0x006FC8EC` | `0x002FC8EC` | complete `EquipPane *` |
| Character name | `0x0073D910` | `0x0033D910` | 16-byte NUL-terminated buffer |
| Application window | `0x0073D938` | `0x0033D938` | `HWND` |
| Screen hierarchy | `0x0073D948` | `0x0033D948` | `HierList<Screen> *` |
| Screen root pane | `0x0073D94C` | `0x0033D94C` | root `Pane *` |
| World map interface | `0x0073D960` | `0x0033D960` | `WorldPane + 0x2E8` |
| World implementation interface | `0x0073D964` | `0x0033D964` | `WorldPane + 0x2EC` |
| Main menu pane | `0x0073D968` | `0x0033D968` | complete `MainMenuPane *` |
| Main thread ID | `0x00740400` | `0x00340400` | Win32 thread ID |
| GUI back pane interface | `0x0082B768` | `0x0042B768` | `GUIBackPane + 0x190` |
| Map-loading pane | `0x00851598` | `0x00451598` | complete `MapLoadingPane *` |

The two adjusted roots can be recovered without calling client code:

```c
WorldPane *get_world_pane(void) {
    void *impl = *reloc_ptr(0x0033D964);
    return impl ? (WorldPane *)((u8 *)impl - 0x2EC) : NULL;
}

GUIBackPane *get_gui_back_pane(void) {
    void *singleton_base = *reloc_ptr(0x0042B768);
    return singleton_base ? (GUIBackPane *)((u8 *)singleton_base - 0x190) : NULL;
}
```

`ui_get_gui_back_pane` at static address `0x005A9C40`, RVA `0x001A9C40`, is the client's native null-safe accessor. Calling it is appropriate only on the game thread.

Constructors publish these roots and destructors clear them. Treat the root pointer value as a generation token. When it changes, discard every child pointer and rebuild the corresponding part of the snapshot.

## Safe snapshot pass

The client mutates panes, arrays, trees, and reference-counted objects on its main thread. A 32-bit aligned pointer load may be atomic, but a whole object walk is not. Another thread can observe a valid parent followed by a destroyed child.

A safe pass is:

1. Require `GetCurrentThreadId() == *app_main_thread_id`.
2. Resolve and capture each root once.
3. Decide the session and map lifecycle states from those captured roots.
4. Copy scalar fields and bounded strings into owned storage.
5. Traverse pointer arrays and trees while still on the same thread.
6. Publish one immutable snapshot after the walk completes.

Never expose a client pointer in the published result. Never wait inside an event handler or snapshot callback. If a packet event is used to request a refresh, take the snapshot after normal handling has finished or on the next dispatcher tick so the client-owned state already reflects the packet.

Packet tracking is useful for invalidation and for values the client does not retain. It should not replace a complete rebuild after login, logout, map transfer, or a root-generation change.

## Lifecycle state

Login state is not one permanent boolean. Pane construction and destruction create short transition windows.

| State | Useful test |
| --- | --- |
| Title | `MainMenuPane != NULL` and `WorldPane == NULL` |
| Entering or leaving | roots are changing, neither principal root is present, or both are briefly present |
| In game | `WorldPane != NULL` and `WorldPane->world_user_func != NULL` |

Use an enum with an unknown or transition value instead of forcing ambiguous frames into title or in-game.

A map is ready for structure walking when all of these are true:

```c
world != NULL
world->width > 0 && world->height > 0
world->map_cell_storage != NULL
world->map_transfer_active == 0
map_loading_pane == NULL
```

The relevant `WorldPane` fields are `width +0x1C4`, `height +0x1C8`, `current_map_id +0x26C`, `map_transfer_active +0x275`, `map_cell_storage +0x27C`, and `world_user_func +0x2CC`.

## Character snapshot

`WorldPane + 0x2CC` points to `WorldUserFunc`, the compact session owner documented in [Session and character state](session.md). The richer status panes fill the fields that this compact copy omits.

| Requested value | Preferred live source |
| --- | --- |
| Name | bounded string at static `0x0073D910`, valid only during an in-game generation |
| Class | `WorldUserFunc + 0x1089`, raw [`CharacterClass`](../../network/protocol-types.md#characterclass) byte |
| Level, ability level | `WorldUserFunc + 0x1058`, `+0x1059` |
| Total experience | `WorldUserFunc + 0x1060` |
| Total ability and game points | `StatusInfoPane + 0x1E0`, `+0x1D4` |
| Experience to next level | `StatusInfoPane + 0x1D0` |
| Ability to next level | `StatusInfoPane + 0x1D8` |
| Strength | `WorldUserFunc + 0x1064` |
| Dexterity, wisdom, constitution, intelligence | `WorldUserFunc + 0x1068`, `+0x106A`, `+0x106C`, `+0x106E` |
| Health and mana totals | `WorldUserFunc + 0x1078` through `+0x1084` |
| Weight and maximum weight | `WorldUserFunc + 0x15C84`, `+0x15C80` |
| Armor class | `ExtraStatusInfoPane + 0x4F8`, signed byte |
| Damage and hit modifiers | `ExtraStatusInfoPane + 0x4F9`, `+0x4FA`, unsigned bytes |
| Attack and defense elements | `ExtraStatusInfoPane + 0x4FC`, `+0x4FE`, `u16` |
| Magic resistance units | `ExtraStatusInfoPane + 0x500`, `u16` |
| Action locked | `(WorldUserFunc[0x15C88] & 0x01) != 0` |

The pane sources are reached through these `GUIBackPane` children:

```c
ItemInventoryPane       *items;        // GUIBackPane +0x4F88
SkillSpellInventoryPane *skill_spells; // GUIBackPane +0x4F8C
SpelledViewPane         *effects;      // GUIBackPane +0x4F94
NewStatusInfoPane       *status;       // GUIBackPane +0x4FA0
NewExtraStatusInfoPane  *extra_status; // GUIBackPane +0x4FA4
```

The status objects are session models even when their page is not selected. They are created with `GUIBackPane`, updated from `SStatus`, and remain useful while another lower-tray page is active. Their complete layouts are in [Status and mail panes](inventory-ui.md#status-and-mail-panes).

### Hidden and translucent appearance

There is no confirmed authoritative `self_is_hidden` field. Find the local world object by looking up `WorldUserFunc + 0x1050` in the world object's ID tree. A `WorldObject_Human` stores `is_translucent` at `+0xD5`.

Expose that value as `appearance_is_translucent`, not as a guaranteed hidden status. The renderer uses it for an observable translucent appearance, but some unseen remote players can instead arrive with an all-zero appearance record. The action-lock byte is independent of this appearance state.

## Inventory and equipment

The compact session inventory is useful for gameplay identity, but the pane model is the authoritative client copy for quantities and durability.

```c
ItemInventoryPane *inventory = gui_back->items;       // +0x4F88
InvItemPane *item = inventory->items[slot - 1];       // pane +0x1A0
```

There are 60 pointers for one-based slots 1 through 60. For each non-null `InvItemPane`, copy:

| Field | Offset |
| --- | ---: |
| Sprite | `+0x190`, `u16` |
| Display name | `+0x192`, bounded 128-byte buffer |
| Dye color | `+0x212`, `u8` |
| Slot | `+0x214`, `u8` |
| Maximum durability | `+0x238`, `u32` |
| Current durability | `+0x23C`, `u32` |
| Quantity | `+0x240`, `u32` |
| Stackable | `+0x244`, `u8` |

The display name can contain the rendered stack quantity. Keep the quantity field separately instead of parsing the string.

Equipment uses the direct `EquipPane` singleton root. It owns 18 entries:

```c
u16 sprites[18];                  // +0x111C
u8 dyes[18];                      // +0x1140
char names[18][128];              // +0x1152
struct { u32 max; u32 current; }
    durability[18];               // +0x1A54
```

The index is `equipment_slot - 1`. The singleton exists for the in-game session even when the equipment UI is not visible. See [Inventory and character panes](inventory-ui.md) for construction and replacement behavior.

## Skills, spells, and cooldowns

`GUIBackPane + 0x4F8C` points to `SkillSpellInventoryPane`:

```c
NewSkillInventoryPane *skills; // +0x224
NewSpellInventoryPane *spells; // +0x228
```

Each child has `capacity +0x190`, normally 90, and an item-pointer array at `+0x194`. Null pointers are empty slots.

Useful spell entry fields are:

| Field | Offset |
| --- | ---: |
| Slot | `+0x190`, `u8` |
| Icon | `+0x192`, `u16` |
| Argument type | `+0x194`, `u8` |
| Name | `+0x195`, 128 bytes |
| Prompt | `+0x215`, 128 bytes |
| Cast lines | `+0x295`, `u8` |
| Action delay active | `+0x297`, `u8` |

Useful skill entry fields are:

| Field | Offset |
| --- | ---: |
| Icon | `+0x190`, `u16` |
| Name | `+0x192`, 128 bytes |
| Slot | `+0x312`, `u8` |
| Cooldown progress | `+0x314`, `u32`, 0 through 30 |
| Cooldown start | `+0x318`, `timeGetTime` milliseconds |
| Cooldown end | `+0x31C`, `timeGetTime` milliseconds |
| Cooldown visual active | `+0x320`, `u8` |
| Action delay active | `+0x322`, `u8` |

Skill remaining time can be calculated from the start and end timestamps with wrap-safe 32-bit tick arithmetic while the visual-active byte is set. Spell entries retain only the active action-delay flag. Recovering an exact remaining spell delay requires observing the corresponding `SActionDelay` update or walking the owner's timer records; the entry alone does not hold an expiry timestamp.

## Buffs and debuffs

`GUIBackPane + 0x4F94` points to `GUIBackPane::_SpelledViewPane`. Its ten display slots are parallel arrays:

```c
s16 icon[10];   // +0x190, -1 means empty
s8 stage[10];   // +0x1A4, 0 means absent
```

Copy each entry whose icon is not `-1` and stage is nonzero. Stage values 1 through 6 are server-supplied remaining-duration display bands. The exact palette and bar behavior are documented with [`SSpelled`](../../network/server/058-0x3a-spelled.md).

The client stores no seconds, expiry timestamp, or last-update time, and it never decrements the stage itself. Therefore a runtime snapshot can expose the icon and duration stage, but not an exact remaining duration. Capture packet arrival time only if time within the current server stage is useful; it still does not reveal the server's threshold or expiry.

## Map and world entities

The durable map values are:

| Value | Source |
| --- | --- |
| Map ID | `WorldPane + 0x26C`, `u32` |
| Width, height | `WorldPane + 0x1C4`, `+0x1C8`, signed 32-bit |
| Camera or view Y, X | `WorldPane + 0x238`, `+0x23C` |
| Map flags | `WorldPane + 0x260` |
| Weather | `WorldPane + 0x264` |

The [`SMapSize`](../../network/server/021-0x15-map-size.md) handler parses the map name but does not copy it into a durable `WorldPane` field. Keep the name from the latest accepted `SMapSize` packet and clear it when the world generation ends. This is the main packet-tracked exception to direct state walking.

`WorldPane + 0x194` points to the shared `WorldObjectList`. Its ordered ID tree contains the client's current humans, creatures, NPC-style objects, and ground items. The exact node and object layouts are in [World objects](world.md#dynamic-object-index).

For a full walk:

1. Capture `WorldObjectList *` once.
2. Read its head sentinel from `list + 0x20`.
3. Begin at `head->parent`, the root node.
4. Perform a bounded in-order traversal, skipping the head sentinel.
5. Copy each object's fields immediately. Do not retain the node or object pointer.
6. Abort the collection on an invalid pointer, repeated node, or reader-defined count limit.

Every common object supplies `entity_id +0x24`, `draw_layer +0x28`, `broad_category +0x2C`, `collision_level +0x31`, `tile_y +0x40`, `tile_x +0x44`, `inserted +0x48`, and optional `name_pane +0x58`.

Classify the complete object by RTTI before reading derived fields:

| Exact class | Useful fields |
| --- | --- |
| `WorldObject_Item` | sprite `+0x7C`, dye `+0xB4` |
| `WorldObject_Monster` | image session `+0x90`, living name `+0x112`, direction `+0x192`, creature type `+0x1EC` |
| `WorldObject_Human` and `WorldObject_User` | image session `+0x90`, appearance record `+0xA4`, translucent byte `+0xD5`, name `+0x112`, direction `+0x192` |

Mundanes and monsters share `WorldObject_Monster`. Creature type, collision behavior, appearance, and an attached name pane are better distinctions than the class alone. Ground-item objects retain sprite and dye, but not a display name or quantity.

This tree is the authoritative collection of objects currently known to the client. It is not a durable list of objects drawn in the last frame. The renderer can still cull by map position and view geometry. Call this collection `known_entities` unless an additional viewport test establishes strict on-screen visibility.

## Lower-tray UI state

`GUIBackPane` retains its current layout and selected page independently of the child models.

```c
s32 layout_index;          // +0x4DF0: 0 small, 1 large
s32 current_page;          // +0x4FA8
Pane *active_page;         // +0x4FAC
bool page_is_expanded;     // +0x4FB0
```

Normal `SWindowChange` selections map to these internal page values:

| Internal value | Page |
| ---: | --- |
| `0` | Items |
| `3` | Skills |
| `1` | Spells |
| `5` | Chat |
| `7` | Status |

Internal values `2`, `4`, and `9` are alternate paired modes. Preserve the raw value if one appears instead of silently labeling it as a normal page.

The UI questions are separate:

| Question | Test |
| --- | --- |
| Is the lower tray compact? | `layout_index == 0` |
| Is the current inventory-style page expanded? | `page_is_expanded != 0` |
| Is the game window minimized by Windows? | `IsIconic(*app_hwnd) != FALSE` |
| Which lower page is active? | map `current_page`, then verify `active_page` is visible |
| Is the chat page selected? | `current_page == 5` and the active page is visible |

Do not call all three compact, expanded, and OS-minimized states "minimized." They have different owners and behavior.

## Discovering panes and dialogs

The event dispatcher owns an `EventHandlerList` subobject at `EventDispatcher + 0x60`. It is a flat preorder representation of the live pane tree:

```c
struct EventHandlerList {
    void *vtable;                    // +0x00
    EventHandlerEntry *entries;      // +0x04
    s32 count;                       // +0x08
    s32 capacity;                    // +0x0C
    // mutation-aware iterator records follow
};

struct EventHandlerEntry {
    Pane *pane;                      // +0x00
    u32 depth;                       // +0x04
    u32 identity_or_generation;      // +0x08, exact purpose uncertain
};                                  // size 0x0C
```

Walk the entry array only on the main thread. Copy `count` once, require `0 <= count <= capacity`, and apply a reader-defined upper bound. The depth values reconstruct parent and ancestor relationships.

A registered pane is not necessarily presented. `Pane + 0x130` is its visible byte. A useful presented test requires the pane and every pane ancestor in the flattened tree to be visible. Input priority, pointer capture, keyboard focus, and object validity are separate states described in [Pane and event layouts](panes.md).

### RTTI class names

On this 32-bit MSVC build, a polymorphic object's primary vtable points into the module's read-only data. The word immediately before that vtable points to its Complete Object Locator. The locator's `+0x0C` pointer names a `TypeDescriptor`, whose decorated class name begins at `TypeDescriptor + 0x08`.

Validate every pointer against the loaded module, bound the class-name read, and use the class hierarchy descriptor when testing inheritance. Exact-name comparison alone does not prove that a class derives from `DialogPane`.

Useful presented class families include:

| UI state | RTTI classes or base family |
| --- | --- |
| Exchange | `ExchangeDialog` |
| Bulletin and mail | `BulletinSession`, `BoardListDialog`, `ArticleListDialog`, `ArticleDialog`, `MailListDialog`, `MailDialog`, `NewArticleDialog`, `NewMailDialog` |
| Who list | `GUIBackPane::_ShowUsersPane`, `ShowUsersPane` |
| Merchant | `MerchantSession` and classes derived from `MerchantDialogPane` |
| NPC pursuit | `NPCSession`, `NPC_Pursuit_MessageDialog`, `NPC_Pursuit_NexonIdDialog`, `NPC_Pursuit_TextInputMenuDialog`, and other `NPCMenuDialog` or `NPCMessageDialog` descendants |

For a generic dialog, `DialogPane` keeps its control list at `+0x594`, default and cancel control indexes at `+0x598` and `+0x59C`, and its focused control index at `+0x5AC`. These fields describe controls owned by that dialog, not every text input in the client.

The chat page test identifies an open chat pane, but exact keyboard ownership remains partly unresolved. A conservative query can report a visible, registered `ChatInputPane`, `TellInputPane`, `TellReceiverInputPane`, or `BlockListenInputPane` together with the selected page or modal context. Do not claim that a line input has focus from `DialogPane + 0x5AC` unless it is actually a control in that dialog.

## Known limits

| Requested result | Limit |
| --- | --- |
| Exact buff duration | Client retains only icon and server stage, not seconds or expiry |
| Exact spell-delay time remaining | Spell entry retains a boolean; packet or timer tracking is needed for an expiry |
| Authoritative hidden state | Only observable human translucency is mapped |
| Ground-item name and quantity | World item objects retain only sprite and dye |
| Strictly drawn entities | The object tree is current client knowledge, not the renderer's last-frame output |
| Exact active chat keyboard owner | Visible input classes can be found, but the universal focus owner is not yet mapped |

These limits should appear as nullable or explicitly qualified fields in a consumer-facing snapshot. Do not fill them with guesses from nearby display state.

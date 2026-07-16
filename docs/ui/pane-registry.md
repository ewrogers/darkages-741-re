# Pane registry and RTTI inventory

The term pane registry can mean three different things in this client. Keeping them separate avoids incorrect ownership and lifecycle conclusions.

| Mechanism | Purpose | Evidence |
| --- | --- | --- |
| `HierList<Screen>` | Runtime spatial pane hierarchy and absolute-coordinate lookup | RTTI name, startup root, insertion/removal, and parent walk |
| `EventHandlerList` | Runtime application pane tree and central event propagation | RTTI name, constructor, insertion/removal, and iterator code |
| `DialogPane + 0x594` | Pane-local ordered control collection | Dialog constructor and pointer/focus routing |
| `Singleton<T>` wrappers | Shared access to selected pane instances | Embedded Microsoft RTTI type names |

The singleton wrappers are not entries in another runtime pane registry. A singleton pane can still be screen-registered, event-registered, hidden, focused, or captured through the ordinary mechanisms.

## Screen hierarchy and root pane

Startup constructs a `HierList<Screen>` at `ui_screen_hierarchy_ptr` (`0x0073D948`) through `ui_screen_hierarchy_ctor` at `0x005522B0`. It then allocates an RTTI-confirmed `ScreenPane` root through `ui_screen_pane_ctor` at `0x00553350` and stores it in `ui_screen_root_pane_ptr` (`0x0073D94C`). The root is inserted into both the screen hierarchy and `EventHandlerList` with null parent and sibling arguments.

Pane primary vtable slots `+0x38` and `+0x3C` call `ui_pane_register_screen` (`0x0054A270`) and `ui_pane_unregister_screen` (`0x0054A2C0`). Insertion reaches `ui_screen_hierarchy_insert` at `0x00552370` and sets bit `0x01` in `Pane + 0x188`. Removal clears that bit and may be deferred while a hierarchy update is active.

`ui_screen_hierarchy_get_absolute_origin` at `0x005528C0` finds the pane's hierarchy node, follows its spatial parents, and adds `Pane + 0x128` and `Pane + 0x12C` until it reaches `ui_screen_root_pane_ptr`. Central pointer capture uses this absolute origin before calling a pane event virtual.

This hierarchy is the closest match to a conventional scene tree for spatial composition. It is still distinct from event propagation. A pane has separate registration bits at `+0x188`: bit `0x01` for `HierList<Screen>` and bit `0x02` for `EventHandlerList`.

## EventHandlerList layout

`EventDispatcher` is allocated as `0x1BC` bytes by startup code. Its `EventHandlerList` begins at dispatcher offset `+0x60` and is constructed by `event_handler_list_ctor` at `0x00465AF0`.

The list uses a heap array of `0x0C`-byte entries:

| Entry offset | Meaning | Confidence |
| --- | --- | --- |
| `+0x00` | Pane pointer | High |
| `+0x04` | Tree depth | High |
| `+0x08` | Entry identity/generation? | Medium |

The tree is stored as a flattened preorder list. An illustrative layout is:

```text
depth 0  root A
depth 1    child A.1
depth 2      child A.1.a
depth 1    child A.2
depth 0  root B
```

This is compact but requires depth-aware iteration:

- `event_handler_list_insert` at `0x00465C50` finds the requested parent and sibling position, then inserts a new entry at parent depth plus one.
- `event_handler_list_remove_subtree` at `0x00465D80` removes the pane and every immediately following entry with a greater depth.
- `event_handler_list_begin_children` at `0x00465E10` allocates one of 16 mutation-aware iterator slots.
- `event_handler_list_next` at `0x00466080` returns the current pane and advances the iterator.
- `event_handler_list_advance_sibling` at `0x00466190` skips descendants until it finds the next entry at the iterator's target depth.
- `event_handler_list_end_iterator` at `0x00466050` releases the iterator slot.

This structure explains the recursion in `event_dispatch_pane_subtree`. Each call iterates immediate siblings while recursive calls handle their children. A mutation during a handler does not rely on a raw array pointer remaining stable.

## Register and unregister

Pane primary vtable slots `+0x40` and `+0x44` call `ui_pane_register_event_handler` (`0x0054A310`) and `ui_pane_unregister_event_handler` (`0x0054A360`). Those reach `event_register_pane` at `0x00463E40` and `event_unregister_pane` at `0x00463E80`.

Registration sets bit `0x02` in `Pane + 0x188`. Unregistration clears it and removes the complete subtree. Showing or hiding the pane does not perform either operation.

The two registration arguments after the pane select its sibling position and parent. Their exact public names are not present in RTTI, so documentation should describe the observed relationship rather than inventing API names.

## DialogPane control collection

`ui_dialog_pane_ctor` at `0x00445260` initializes `DialogPane + 0x594` to null. `ui_dialog_add_control` at `0x00445670` creates the collection on first use and inserts a control pointer.

Important `DialogPane` fields are:

| Offset | Role |
| --- | --- |
| `+0x594` | Control collection pointer |
| `+0x598` | Configured control index used by dialog setup |
| `+0x59C` | Second configured control index used by dialog setup |
| `+0x5AC` | Focused control index |
| `+0x5BC` | Hovered control index |
| `+0x5C0` | Hover hit-zone code |
| `+0x5C4` | Secondary pointer-state control index |
| `+0x5C8` | Secondary pointer-state zone |

Some setup fields remain behaviorally named rather than fully identified. The focus and pointer-state fields are confirmed by the event handlers.

The login dialog shows how layout data becomes the local collection. Its constructor at `0x004BA180` repeatedly asks the layout manager for a named control through `0x004832E0`, then passes the returned object to `ui_dialog_add_control`. Later event callbacks use the attachment-order index, not the layout string, as the control ID.

## RTTI pane inventory

A Binary Ninja name search for local RTTI vtable types containing `Pane` returns 302 records. That is a useful search result, but it is not a complete inheritance query. Decoding the MSVC Complete Object Locator and Class Hierarchy Descriptor records produces 332 distinct classes whose base graph actually reaches `Pane`.

The two results differ for explainable reasons. The name search includes `WorldPane_user_object_message`, whose name contains `Pane` but whose RTTI does not inherit it. It also misses 31 real descendants whose displayed vtable name does not contain that substring. The complete alphabetical list and direct-base paths are in the [Pane type and inheritance appendix](../appendix/pane-types.md).

The largest recovered qualifier groups are:

| Recovered qualifier | Vtable types |
| --- | ---: |
| `Pane` | 80 |
| `DialogPane` | 59 |
| `AlertPane` | 15 |
| `ListPane` | 14 |
| `ControlPane` | 13 |
| `LineInputPane` | 10 |
| `BulletinDialogPane` | 7 |
| `DraggedPane` | 6 |
| `SessionLayeredTabPane` | 5 |
| `TextEditPane` | 4 |
| `ButtonControlPane` | 4 |

Names such as `Pane::DialogPane::VTable` and `DialogPane::LoginDialogPane::VTable` agree with constructor vtables and suggest those inheritance steps. Other qualifiers can represent a namespace or a specialized family. The appendix therefore derives each edge from the Base Class Array instead of treating the qualified vtable type name as proof.

Representative recovered families include:

- Dialogs: `LoginDialogPane`, `CreateUserDialogPane`, `AgreementDialogPane`, `ExchangeDialogPane`, `ManufactureDialogPane`, and `BrowserDialogPane`.
- Controls: `ControlPane`, `ButtonControlPane`, `ImageButtonControlPane`, `LineInputPane`, and `TextEditPane`.
- World and overlay panes: `WorldPane`, `FieldMapPane`, `GameMessagePane`, `ClockPane`, `ToolTipPane`, and `MapLoadingPane`.
- Lists and tabs: `ListPane`, `ArticleListPane`, `BoardListPane`, `LayeredTabPane`, and `SessionLayeredTabPane`.

## Singleton pane wrappers

The executable contains 86 RTTI strings for `Singleton<T>` specializations. Thirty-nine name a pane or dialog type by a simple name filter. Confirmed examples include:

```text
AgreementDialogPane          BrowserDialogPane          BrowserControlPane
CIPane                       ClockPane                  CreateUserDialogPane
EmployeeDialogPane           EquipPane                  GameMessagePane
IMECandidatePane             LogoPane                   MapLoadingPane
PopupMenuPane                StatusInfoPane             ToolTipPane
TownMapPane                  GUIBackPane                WorldPane
WorldPane_Impl               UserInfoPane_ForUser       UserInfoPane_ForOthers
```

These names prove that shared-instance wrappers were instantiated. They do not prove that every listed pane is always alive, visible, or registered. The wrapper may lazily create or merely expose the instance.

## Practical analysis workflow

For a pane or dialog under investigation:

1. Start from its exact RTTI vtable name and constructor writes.
2. Record both the primary pane vtable and the secondary `TimerHandler` vtable at `this + 0x11C`.
3. Compare event slots `+0x48`, `+0x4C`, `+0x50`, and `+0x54` with the nearest verified base.
4. Check `+0x64` for a dialog action override.
5. Find `ui_pane_register_screen` calls to establish spatial parentage.
6. Find `ui_pane_register_event_handler` calls to place it in the event tree.
7. Find `ui_dialog_add_control` calls to reconstruct its pane-local control order.
8. Track show/hide, capture, focus, and timer operations separately.
9. Use runtime observation to capture actual parentage, depth, visibility, priority, and focus state for each application phase.

This workflow produces a useful node-style view without flattening several independent client mechanisms into one invented registry.

# Item and ability descriptions

The client has two description surfaces that look related but use different data. Right-clicking a spell or skill opens a fixed detail pane. Hovering an item opens the shared `DescPane` tooltip. Both can show names and descriptive text, but the spell and skill `Lev:x/y` suffix is not copied into the detail pane's `LEV` line.

## Spell and skill level suffixes

`ui_parse_skill_spell_level_suffix` runs when a live `SkillInvItemPane` or `SpellInvItemPane` is constructed. It initializes both numeric outputs to `-1`, then scans backward for this shape near the end of the supplied name:

```text
<base name> (<label><left>/<right>)
           ^
           returned split position
```

The scan uses the rightmost closing parenthesis it encounters, then requires a preceding slash, an opening parenthesis, and an ASCII space immediately before that opening parenthesis. It does not require the closing parenthesis to be the final byte. It also does not check the literal text `Lev:`. Any label is accepted if the surrounding shape is usable.

The right substring is passed to `atoi` without digit validation. On the left, the parser skips characters after `(` until it finds the first ASCII digit, then passes that substring to `atoi`. A missing left digit or a nonnumeric right side can therefore become zero. A structurally valid suffix returns the position of the separating space. A suffix missing the required delimiters returns the original string length and leaves both outputs at `-1`.

The constructors retain three results:

- the left numeric value
- the right numeric value
- the split position used to recover the base name

`ui_skill_inventory_item_get_base_name` and `ui_spell_inventory_item_get_base_name` copy only the bytes before the split position. Name-based book searches therefore compare `Beag Cradh`, not `Beag Cradh (Lev:2/10)`.

The left value is confirmed as the learned level. `ui_skill_spell_book_find_current_level` scans the 89 live spell or skill slots by stripped base name and returns that value. Requirement checks compare it with prerequisite spell and skill levels. The client retains the right value, but its meaning and a later consumer have not been confirmed.

## Right-click detail pane

The information action resolves the selected spell or skill definition, builds `SkillSpellInfoDialogPane`, centers it over the owner, and opens it. The pane loads `_nui_ske.txt`, including `ICON`, `LEV`, five stat fields, `NAME`, two subtitle fields, and `DESC`.

The displayed fields come from the definition record:

- `ICON` selects the skill or spell icon bank and sprite.
- `NAME` uses the definition name.
- `LEV` is formatted independently from definition requirement fields by `ui_skill_spell_format_level_requirement`.
- The five stat requirements have individual pass or fail colors.
- The description joins at most 32 retained lines with newline characters.

The learned-name lookup contributes a learned/not-learned state, and the parsed left value can satisfy prerequisite checks. Its numeric output is not copied into `LEV`. This is the important separation between the name suffix and the visible detail line.

## Shared item hover tooltip

`DescPane` is a singleton shared by ordinary inventory items and merchant-style server item lists.

The exact RTTI class `ItemMetaDescMan` supplies the local item-description index. It subscribes to the `SItemDes` metadata table with internal event tag `0x1234`. Each accepted row contributes a numeric ID and text value under the row's group name. The compiled client also contains an unreferenced helper that writes this index to `IDDump.txt`; no live static call reaches that debug export.

```text
pointer enters a row
        |
        v
queue row update at 0 ms
        |
        v
resolve item name or item provider
        |
        v
load, position, and show DescPane
```

`ui_desc_pane_show` creates the pane on first use. A non-null item name reloads its description helper. A null name keeps the current content and only updates placement. The pane records whether it is active and may retain an owning inventory item so that one item cannot close another item's tooltip. `ui_close_desc_pane` hides and unregisters the active pane and clears that state.

An `InvItemPane` opens the tooltip directly from pointer movement. It adjusts the anchor to keep the tooltip inside the 640 by 480 client area. Leaving the item closes the pane only when that item is the recorded owner.

`NPCServerItemMenuDialog`, used by screen-menu types 4 and 10, takes a queued path. Its row control schedules timer subtype 2 with the row index and a delay of 0 ms. The dialog callback stores the pointer position, resolves a changed row, and opens `DescPane` near the pointer. A repeated update for the same row passes a null name and repositions the existing pane. Subtype 3 and movement outside the dialog close it and reset the hover row.

The compiled `MerchantDialogPane::ServerItemMenuDialog3` family contains the same name-based `DescPane` pattern, including a row-relative timer callback. This supports the reported shop and banking behavior, but its live construction path has not yet been recovered. The current local-inventory screen-menu types 5 and 11 use a different list family and have no direct `DescPane` call in the checked path. The exact mapping of buy, sell, deposit, and withdrawal screens to these compiled families therefore remains partly behavioral evidence.

`DescPane` also closes when it receives decoded `SExchange` or `SGroup` events. It checks only the opcode for that cleanup path.

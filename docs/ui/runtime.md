# UI loading, input, and rendering

Win32 messages, internal event values, focus and modal priority, keyboard shortcuts, mouse modifiers, and world actions are documented in the dedicated [input subsystem](../input/README.md). This page focuses on UI construction and runtime pane behavior.

The UI runtime combines archive layouts with compiled C++ pane behavior. A layout supplies named presentation data. A pane constructor selects those names and creates the runtime hierarchy.

## Construction pipeline

The common path is:

1. Obtain the shared layout manager through `ui_layout_manager_singleton` at `0x402AC0`.
2. Load and cache a text entry with `ui_layout_load_from_archive` at `0x482340`.
3. Select controls by `<NAME>` and retrieve their rectangles, images, values, and colors.
4. Construct concrete pane classes such as `ImageButtonControlPane` or `TextEditControlPane`.
5. Attach each child to its parent pane.
6. Let the parent virtual methods handle input and draw traversal.

The layout manager uses the default UI fastfile when no archive object is supplied. In this build the active layouts and their image entries are primarily in `setoa.dat`.

## Login dialog example

`ui_login_dialog_ctor` at `0x4BA180` is a complete example:

```c
void LoginDialogPane::construct(void)
{
    layout *ui;

    ui = load_layout("_nlogin.txt", 0);
    attach_background(ui, "Noname");

    attach_child(create_image_button(ui, "OK"));
    attach_child(create_image_button(ui, "Cancel"));
    attach_child(create_text_edit(ui, "Name"));
    attach_child(create_text_edit(ui, "Password"));
}
```

The simplified code shows intent, not recovered source syntax.

`ui_login_dialog_handle_control_action` at `0x4BA8C0` switches on the child ID:

```c
int LoginDialogPane::handle_action(int control_id, int event_code)
{
    switch (control_id) {
    case 0:
        send_login(name_text(), password_text());
        return 1;

    case 1:
        close_dialog();
        return 1;
    }

    return 0;
}
```

Control ID `0` is OK and ID `1` is Cancel. The constructor's child attachment order creates this mapping. `_nlogin.txt` contains the names and visual definitions, but no callback or packet opcode.

`ui_login_dialog_handle_key_event` at `0x4BA810` implements Enter and Escape behavior through the same pane logic.

## Image button states

`ImageButtonControlPane` is identified by RTTI at `0x6C5950`. Its constructor is `ui_image_button_ctor` at `0x439640`.

The object stores three image descriptors beginning at these offsets:

| Object offset | Use |
|---:|---|
| `this + 0x1A0` | Current visual state: 0, 1, or 2 |
| `this + 0x1AC` | State 0 image descriptor |
| `this + 0x1E0` | State 1 image descriptor |
| `this + 0x214` | State 2 image descriptor |

Each image descriptor is `0x34` bytes in this code path. These are object-relative offsets, not static addresses.

`ui_image_button_initialize_images` at `0x439700` supports two layout styles:

- `VALUE` from 1 through 14 selects a built-in button preset.
- Otherwise, up to three explicit `IMAGE` entries supply the state images.

`ui_image_button_draw` at `0x439860` chooses the descriptor by state, clips to the pane rectangle, and calls `render_blit_image` at `0x44FB80`. The blitter handles software clipping, palette conversion, transparency, and orientation modes.

Enter or Space activation reaches `ui_image_button_handle_key_event` at `0x438590`. That function invokes the parent action virtual with the button's numeric ID and event code `8`.

## EPF and SPF image loading

`render_load_image_frame` at `0x48BBC0` resolves an image filename and frame through the shared image library at `0x404A00`.

`render_decode_image_entry` at `0x48B530` recognizes `.epf` and `.spf` names case-insensitively and follows separate decode paths:

- SPF entries can be parsed directly from the fastfile entry buffer.
- EPF entries use header and frame metadata before the requested frame is made available to the blitter.
- Effect resources containing names such as `Efct` or `Mefc` have additional table handling.

The field layouts, palette behavior, and compression results are documented in [Graphics and animation files](../file-formats/graphics-and-animation-files.md).

## New in-game pane set

The root `_nui.txt` layout provides `CONTENT` and tab rectangles. Constructors then load more focused layouts:

| Internal class | Layout | Constructor |
|---|---|---:|
| `nui_AlbumPane` | `_nui_al.txt` | `0x5B2A70` |
| `nui_EventPaneImpl` | `_nui_ev.txt` | `0x5B3EE0` |
| `nui_FamilyPane` | `_nui_fm.txt` | `0x5B4FB0` |
| `nui_IntroPane` | `_nui_eq.txt`, `_nui_eqa.txt` | `0x5B59F0` |
| `nui_LegendPane` | `_nui_dr.txt` | `0x5B7AA0` |
| `nui_SkillSpellPane` | `_nui_sk.txt` | `0x5B80C0` |
| `PortraitTextInputDialogPane` | `_nui_pi.txt` | `0x5B11A0` |
| `SkillSpellInfoDialogPane` | `_nui_ske.txt` | `0x5AE090` |
| `EventInfoDialogPane` | `_nui_eve.txt` | `0x5AF460` |

These class associations were recovered from the constructor's assigned vtable, the vtable's complete object locator, and its RTTI type descriptor. They do not rely on filename guessing alone.

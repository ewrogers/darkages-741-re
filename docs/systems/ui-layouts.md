# UI layout files

The client keeps many window layouts as small text files inside `setoa.dat`. Their names usually begin with `_n`, such as `_nlogin.txt`, `_noptdlg.txt`, and `_nui_pi.txt`.

These files describe named rectangles and art. They do not create a pane tree by themselves. The C++ pane class loads a layout, asks for definitions by name, constructs the real controls, and attaches them to the dialog.

```text
setoa.dat
  |
  +-- _nui_pi.txt
        |
        +-- named definitions: TEXT, OK, CANCEL
                    |
PortraitTextInputDialogPane constructor
        |
        +-- TextEditControlPane
        +-- ImageButtonControlPane
        +-- ImageButtonControlPane
```

This is closer to a game UI skin than a complete scene file. The layout controls position and appearance. The compiled pane class supplies behavior.

## Load path

`ui_layout_load` finds the named entry through the normal DAT archive reader. It parses each `CONTROL` block and caches the result by layout filename.

The pane then uses helpers such as:

- `ui_layout_get_control_rect`
- `ui_layout_get_control_type`
- `ui_layout_get_control_image`
- `ui_layout_get_control_value`
- `ui_layout_get_control_color`
- `ui_layout_create_image_button`

A missing layout or a missing named control reaches a fatal invalid-layout error. Names are part of the contract between the asset and the pane class.

## Text format

```text
<CONTROL>
    <NAME> "OK"
    <TYPE> 7
    <RECT> 10 172 71 194
    <IMAGE>
        "_nbtn.spf" 3
        "_nbtn.spf" 4
        "_nbtn.spf" 5
    <VALUE>
        0
    <COLOR>
        20
        31
<ENDCONTROL>
```

`ui_layout_parse_control` recognizes these fields:

| Field | Meaning |
| --- | --- |
| `NAME` | Name used by the pane constructor to find this definition. |
| `TYPE` | Numeric layout category. It does not choose the final C++ control class by itself. |
| `RECT` | Left, top, right, and bottom in pane-local coordinates. |
| `IMAGE` | Ordered image entry name and frame index. Up to three entries are used by the image-button helper. |
| `VALUE` | Ordered integer options. A button may use the first value as a built-in skin selector. |
| `COLOR` | Ordered palette indexes used by the control constructor. |

The matching archive contains 46 underscore-prefixed text layouts with 525 control definitions. Only `TYPE` values 0, 3, and 7 appear in those files. Type 0 is normally the window background. Type 7 is the common named region. Type 3 appears on two agreement buttons. Use a nearby working control as the model instead of assigning a new type from its number alone.

## Names and action IDs

A layout's order is not the dialog's callback order. Numeric action IDs come from the order in which the pane constructor calls `ui_dialog_add_control`.

`_nui_pi.txt` stores its definitions as `Noname`, `OK`, `CANCEL`, then `TEXT`. `PortraitTextInputDialogPane` attaches them in a different order:

| Action ID | Attached control | Result |
| ---: | --- | --- |
| 0 | `TEXT` | Profile edit control |
| 1 | `OK` | Save and close |
| 2 | `CANCEL` | Close without saving |

The login dialog gives another example. `_nlogin.txt` lists the two edit areas before its buttons, but `LoginDialogPane` attaches `OK`, `Cancel`, `Name`, then `Password`. Its action IDs follow that attach order.

Pointer hit testing returns an attached-control index. `ui_dialog_handle_pointer_event` sends that index to the dialog's action virtual on release. Keyboard focus, Tab movement, Enter, Space, and Escape also work from the attached control collection. See [UI and panes](ui.md) and [Event system](events.md) for the wider routing flow.

## Building a custom UI

There are two useful levels of customization.

To reskin or rearrange an existing pane:

1. Start from the layout file already loaded by that pane class.
2. Keep every control name that the constructor requests.
3. Change rectangles, image entries, frame indexes, or supported color values.
4. Preserve image order for controls with several states.
5. Rebuild or extend `setoa.dat` with the changed text and referenced art.
6. Test every pointer and keyboard path because the compiled attach order still controls callbacks.

To add a new control with new behavior, a layout edit is not enough. Code must look up the new name, construct a suitable `Pane` or `ControlPane`, call `ui_dialog_add_control`, and handle the resulting action ID. An injected extension can do that after the original constructor runs, but it must also follow the normal lifetime, event registration, focus, and cleanup rules.

The client includes `ui_layout_serialize_control`, so the grammar has a built-in two-way representation. A custom tool can parse and write the same fields. DAT archive writing remains a generated inverse of the reader and should be round-trip tested as described in [DAT archives](../file-formats/dat-archives.md).

The complete file-to-class mapping is in [UI layout registry](../appendix/ui-layout-registry.md).

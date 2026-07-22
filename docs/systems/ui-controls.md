# Native UI controls

Dialogs attach small `ControlPane` objects for buttons, text fields, progress bars, and grouped choices. The layout file supplies rectangles and art indexes, while the constructor chooses the control class and attachment order.

## Shared state

Exact RTTI confirms this first reconstructed hierarchy:

```text
Pane
  +-- ControlPane
        +-- ProgressBarControlPane
        +-- ProgressBarControlPaneEx
        +-- ButtonControlPane
        |     +-- TextButtonControlPane
        |     +-- TextButtonExControlPane
        |     +-- ImageButtonControlPane
        |           +-- ImageButtonExControlPane
        +-- RadioGroupControlPane
        +-- ScrollableControlPane
        +-- TextEditControlPane
        |     +-- StaticTextControlPane
        |     +-- StaticTextControlPane2
        +-- ImageControlPane
```

`ControlPane` keeps these common states separate:

| Field | Purpose |
| --- | --- |
| control kind | Distinguishes constructor-selected control families |
| enabled | Allows normal interaction and selects enabled drawing |
| palette index | Supplies the current color or hit-zone state |
| focus outline allowed | Copies the owning dialog's policy when attached |
| rectangle | Defines the local control bounds |

Changing enabled state or palette index invalidates the rectangle so the next frame redraws it.

## Buttons and labels

`ButtonControlPane` adds a visual state, a toggle lock, and focus. Enter or Space sends dialog action `8` with the control's attachment-order ID.

Text buttons own a child text pane. Registration attaches that child in the parent's coordinate space, and unregistration detaches it first. The normal and extended classes center a 12-pixel-high label using the client's 6-pixel-per-byte text measurement.

Image buttons retain three pixmaps for the normal button states. A numbered source loads three consecutive frames from `butt001.epf`; the alternate constructor accepts three pixmaps supplied by its caller. `ImageButtonExControlPane` adds the same kind of owned, centered label used by text buttons.

The extended text button selects `buttonex.epf` or `btn220.epf` from its width and state. Focus feedback is drawn only when the control is enabled, focused, and its dialog permits focus outlines.

## Progress, radio, and scrolling

`ProgressBarControlPane` loads two pixmaps and draws a background segment count followed by the filled foreground count.

`RadioGroupControlPane` owns a collection of bounded labels and rectangles. Pointer hit testing returns the option index with bit `0x40` set, or `7` when no option is hit. Changing selection invalidates both the old and new option rectangles. Drawing chooses palette indexes independently from enabled, hovered, and selected state.

`ScrollableControlPane` owns another pane. Rectangle changes are converted to local coordinates and forwarded to that child. Screen registration attaches the child, unregistration detaches it, and destruction queues the child through the normal deferred-deletion owner.

Its scroll API selects one of the child pane's two scrollbars. Maximum values are clamped to `0..30000`, positions remain within that maximum, and absent scrollbars read as zero. Pointer, keyboard, network, and timer events are forwarded to the owned child.

## Text and image controls

`TextEditControlPane` builds a child text canvas, applies optional scrollbar margins and text flags, inserts initial text, and connects to the shared text-input service when it exists. It exposes separate byte and line limits. Applying a byte limit immediately uses the canvas's DBCS-safe truncation path.

Focus enters editing mode, resets caret state, and can select all text. Unfocus leaves editing mode and collapses the selection to the caret. Masked-input mode is enabled explicitly for sensitive form fields.

The two static-text variants reuse the text canvas without normal editing. `StaticTextControlPane` can optionally forward input events, while `StaticTextControlPane2` keeps editing disabled.

`ProgressBarControlPaneEx` draws a bordered proportional vertical fill from current and maximum values. `ImageControlPane` retains one pixmap, invalidates itself when that image changes, and blits it during the content draw.

The durable symbols and evidence are in [`ui-controls.yaml`](../../analysis/exports/ui-controls.yaml).

# Server message dialogs

The client can show server-driven message panes with wrapped text, optional character or item art, and up to four actions. These panes use the exact RTTI base class `MessageDialogBase` and the `lmsg.txt` layout.

## Flow

A shared dispatcher reads a one-byte message variant and constructs the matching derived dialog. The ordinary `MessageDialog` then:

1. parses the shared target, graphic, navigation, and text fields;
2. measures the text and optional art;
3. builds a variable-height pane from the top, middle, and bottom layout images;
4. attaches the text, action buttons, and optional image control.

The dispatcher has compiled branches for variants `0` through `6` and `9`. Their derived behavior is documented as each class is recovered.

## Text and art

The standard dialog treats text as byte strings. It lays out 40 character cells per row when art is present and 48 cells otherwise. Each cell and row is 12 pixels for this size calculation.

The graphic ID selects the image source:

| Graphic ID | Source |
| --- | --- |
| `0x4000` through `0x7FFE` | Monster image library |
| `0x8000` through `0xBFFE` | Item icon library |
| Other values | No measured art |

The client loads the selected image before construction to measure its visible pixel bounds. A simple message variant instead uses a fixed 240 by 52 pixel pane.

## Layout contract

`ui_load_message_dialog_layout` loads `lmsg.txt` once and retains:

- `TopImage`, `MidImage`, and `BotImage`;
- `Description`;
- `Btn1` through `Btn4`;
- the `SimpleMessage` art and `smBtn1` through `smBtn3`.

The ordinary builder repeats the middle image enough times to contain the wrapped text. Server flags control whether the navigation buttons begin enabled.

## Movement and closing

Dragging a message records its start and end positions. Selected message variants apply that delta to a matching pair of shared viewport offsets, so later panes of that family retain the adjusted position.

Closing runs the pane's detach callbacks and queues it for deferred destruction. The input handler consumes pointer events that report a nonzero action result.

## Known limits

The common message dispatcher and the ordinary variant are confirmed. The meanings and packet layouts of every derived variant are still being recovered, so this page does not assign names to their unknown fields yet.

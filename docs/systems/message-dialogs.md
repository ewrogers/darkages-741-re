# Server message dialogs

The client can show server-driven message panes with wrapped text, optional character or item art, and up to four actions. These panes use the exact RTTI base class `MessageDialogBase` and the `lmsg.txt` layout.

## Flow

A shared dispatcher reads a one-byte message variant and constructs the matching derived dialog. The ordinary `MessageDialog` then:

1. parses the shared target, graphic, navigation, and text fields;
2. measures the text and optional art;
3. builds a variable-height pane from the top, middle, and bottom layout images;
4. attaches the text, action buttons, and optional image control.

The dispatcher accepts variants `0` through `6` and `9`. Other values do not create a pane.

## Confirmed variants

| Variant | Exact class | Content and controls |
| --- | --- | --- |
| `0` | `MessageDialog` | A `string16` message, optional monster or item art, and up to four actions |
| `1` | `SimpleMessageDialog` | No message string; a fixed 240 by 52 pane with three actions |
| `2` | `QuestionMessageDialog` | A `string16` prompt followed by counted `string8` choices |
| `3` | `SimpleQuestionMessageDialog` | Counted `string8` choices without a prompt |
| `4` | `TextMessageDialog` | A `string16` message, prompt and trailing labels, optional art, and a bounded text editor |
| `5` | `SimpleTextMessageDialog` | Prompt and trailing labels plus a bounded text editor, without the main message |
| `6` | `QuestionMessageFaceDialog` | A prompt and choices with a `HumanImageControlPane` preview |
| `9` | `NexonclubDialog` | A message, optional art, ID and masked-password editors, submit, and account registration |

The question builders attach one text button per choice. Attachment order becomes the action number, so each handler converts it back to the one-based choice value expected by the packet.

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

## Responses

These dialogs answer with `CPursuit` command `0x3A`. The common response identifies the target, pursuit, and step. The response shape then follows the action:

| Action | Step | Argument |
| --- | --- | --- |
| Previous | Current step minus one | None |
| Stay on current step | Current step | None |
| Choose an answer | Current step plus one | Type `1`, followed by the one-byte choice |
| Submit text | Current step plus one | Type `2`, followed by a one-byte length and text bytes |

`SimpleQuestionMessageDialog` also sends the displayed choice through `CSay` command `0x0E` before its pursuit response. This is a real extra packet, not merely local UI feedback.

Variant `9` authenticates the entered NexonClub ID and password on a background worker. A one-second timer polls the result so the pane does not wait inside an input callback. A successful result sends the authenticated ID as the type-`2` pursuit text. Its fourth action opens the client's fixed Nexon account-registration URL through `ShellExecuteA`.

## Movement and closing

Dragging a message records its start and end positions. Selected message variants apply that delta to a matching pair of shared viewport offsets, so later panes of that family retain the adjusted position.

Closing runs the pane's detach callbacks and queues it for deferred destruction. The input handler consumes pointer events that report a nonzero action result.

## Known limits

The client skips one byte and one four-byte block in the common server header without interpreting them. Their server-side meanings are not established by this binary. Final text colors still resolve through the client's palette rather than fixed RGB values.

# Messages and history

The client has three different places that can show server text. A short notice can fade over the world, a longer-lived copy can enter the message history, and speech can appear above a character without being saved at all.

| UI path | Owner | Retention |
| --- | --- | --- |
| Floating notices | `GameMessagePane` | Four rendered rows, then automatic fading |
| Message history | `NewSystemMessagePane` and `NewSystemMessageTextPane` | Up to 30,000 text bytes |
| World speech | `World::BalloonPane` | Three-second balloon attached to one object |

## Floating notices

`GameMessagePane` is the small colored overlay used by several [`SMessage`](../network/server/010-0x0a-message.md) types. The live world layout gives it four rows with 49 character cells per row.

Long text wraps into another row. When a fifth row is needed, the oldest row is rotated out. Each append starts a 2,000 millisecond timer before its fade sequence begins. This pane is therefore a short display queue, not the persistent chat log.

## Persistent history

`NewSystemMessagePane` owns a `NewSystemMessageTextPane`, which is a specialized `TextEditPane`. It accepts `SMessage` types `0x00` through `0x06`, `0x0B`, and `0x0C` when the body is no longer than 70 bytes.

Each accepted message is prefixed with a newline and appended to the text buffer. Carriage returns are normalized to spaces, and the regular formatted-text parser handles inline color codes.

The buffer limits are:

```c
struct MessageHistoryLimits {
    s16 max_bytes = 30000;
    s16 max_lines = 30000;
};
```

This is not a fixed packet count. A full 70-byte message consumes 71 retained bytes after its added newline, so the byte limit holds roughly 422 such messages. Shorter messages allow more entries. The line limit is also 30,000, but the byte limit normally wins first.

When the byte limit is exceeded, `ui_text_enforce_max_bytes` removes the oldest text from the front. It checks Windows DBCS lead bytes so trimming does not leave half of a two-byte character behind.

## The orange history control

The orange control belongs to `NewSystemMessagePane`. Its drag handler changes how many history rows are visible, clamped from one through ten. It is a height control rather than the history buffer itself.

The embedded `NewSystemMessageTextPane` supplies the scrollable text behavior. Expanding the orange control reveals more rows at once, while the underlying text buffer can retain much more than ten lines.

## Saved and unsaved speech

[`SSay`](../network/server/013-0x0d-say.md) contains a speech mode, a world-object ID, and a `string8`. Its handler creates a balloon for 3,000 milliseconds. It does not call the persistent-history append path.

`SMessage` has no independent history flag either. Its type byte is the selector. This gives the server a simple way to choose the result:

```text
SSay only                 -> temporary object balloon
history SMessage only     -> saved message
SSay plus SMessage        -> balloon plus saved copy
```

The client code supports this explanation for NPC text that is saved only sometimes. A paired runtime capture is still needed to prove whether the live server sends both packets for the logged case.

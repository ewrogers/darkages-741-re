# Speech balloons and message routing

## Receive paths

`net_dispatch_game_server_message` at `0x5ED990` sends two registered packets into different handlers:

```text
SSay 0x0D
    net_handle_s_say 0x5F3E00
    chat_show_object_balloon 0x5CBF90
    World::BalloonPane

SMessage 0x0A
    net_handle_s_message 0x5F6D80
    GameMessagePane, WindowMessageDialogPane, or ScorePane
```

This distinction explains why ordinary speech can appear over a player or creature while channel and system text can appear in a screen overlay or panel.

## Object speech and shouts

The recovered `SSay` body is:

```text
u8     say_type
u32be  object_id
string[u8 length] text
```

`net_handle_s_say` at `0x5F3E00` looks up `object_id`. If the object is missing, it sends `CPutRequest` so the server can restore the missing object state. If the object exists, `chat_show_object_balloon` creates a `World::BalloonPane` and schedules removal after `3000` milliseconds.

The local input path confirms these values:

| `say_type` | Local behavior | Balloon palette |
|---:|---|---:|
| `0` | Public say, opened with Enter | `0xFF` |
| `1` | Shout, opened with `!` | `0x45` |
| `2` | No local input path confirmed | `0x58` |

The type `2` style is implemented by `chat_world_balloon_pane_ctor` at `0x5C4F00`, but its sender and semantic name remain open.

## General message routing

`net_s_message_deserialize` at `0x59A100` produces this packet object:

```text
u8 message_type

if message_type == 0x11:
    u8 unknown_1
    u8 unknown_2
    string[u8 length] unknown_text

u16be data_length
bytes[data_length] data
```

`net_handle_s_message` at `0x5F6D80` handles only a subset of the possible types:

| Type | Display target | Rendering behavior |
|---:|---|---|
| `0x00` | `GameMessagePane` | Palette `0x58`, RGB `127,167,243` (`#7FA7F3`), then newline |
| `0x03` | `GameMessagePane` | RGB `255,255,255`, then newline |
| `0x08` | `WindowMessageDialogPane` | Standard panel variant |
| `0x09` | `WindowMessageDialogPane` | Standard panel variant |
| `0x0A` | `WindowMessageDialogPane` | Alternate panel variant |
| `0x0B` | `GameMessagePane` | Palette `0x77`, RGB `143,151,55` (`#8F9737`), then newline |
| `0x0C` | `GameMessagePane` | Palette `0x54`, RGB `115,183,175` (`#73B7AF`), then newline |
| `0x12` | `ScorePane` | White text, maximum accepted length `70` |

Types `0x01`, `0x02`, `0x04` through `0x07`, and `0x0D` through `0x11` fall through without display in this handler. Type `0x11` has extra deserialized fields but is still ignored here.

The exact channel names for types `0x00`, `0x03`, `0x0B`, and `0x0C` are not statically encoded. Private tell or whisper, guild, and world messages are expected to use this family, but assigning those names to individual values requires a capture or owner confirmation.

## Colored floating overlay

The direct text types append to `GameMessagePane`, confirmed by RTTI at `0x6C6B10`. The world setup routine at `0x4B75A0` creates this pane with the raw internal rectangle tuple `{2, 3, 58, 300}`. Its placement and automatic visibility behavior make it the recovered on-screen floating message overlay.

`chat_append_game_message_palette` at `0x4803A0` resolves a palette index through `ui_palette_get_rgb` at `0x593D40`. The palette stores three bytes per entry:

```c
void palette_get_rgb(const u8 *palette, u8 index, u8 *r, u8 *g, u8 *b)
{
    const u8 *entry = palette + (index * 3);

    *r = entry[0];
    *g = entry[1];
    *b = entry[2];
}
```

The RGB values above were read directly from the untransformed 768-byte `legend.pal` entry in the local `Legend.dat`. Public-say balloon palette `0xFF` is RGB `27,127,127` (`#1B7F7F`), and shout palette `0x45` is RGB `255,231,59` (`#FFE73B`). These colors are evidence for runtime comparison, but are not enough by themselves to name the remaining channel subtypes.

`chat_game_message_pane_append_rgb` at `0x47C5C0` converts the text into per-character colored cells, handles inline palette tokens, wraps lines, and makes the pane visible.

## Look and panel messages

Look results use `SMessage 0x0A`, not the raw `0x34` other-user profile reply.

For types `0x08`, `0x09`, and `0x0A`, `net_handle_s_message` changes each tab byte (`0x09`) in the payload to carriage return (`0x0D`) and constructs a `WindowMessageDialogPane`. RTTI identifies the class at `0x6C5BFC`, and its constructor is `ui_window_message_dialog_ctor` at `0x4488C0`.

Types `0x08` and `0x09` pass mode `0`. This builds the standard wrapped text view and close-button form. Type `0x0A` passes mode `1` and builds an alternate text control. The static code confirms the structural variant, but does not identify which look request or content category selects each subtype.

## Score pane

Type `0x12` is not sent to `GameMessagePane`. `ui_score_pane_handle_s_message` at `0x5521B0` forwards it to `ScorePane`, confirmed by RTTI at `0x6CC600`. The helper at `0x552120` prepends a newline, accepts lengths from `0` through `70`, and appends the result in white.

This is a distinct overlay and should not be labeled as a normal chat channel without runtime evidence.

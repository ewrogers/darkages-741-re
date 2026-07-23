# Mini Game (`SMiniGame`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x64` (100) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

This packet can open one of the client's built-in mini games, including the separate fishing dialog. It also carries updates for games that are already open.

The path is live in this client. The server packet factory constructs `SMiniGame`, `net_deserialize_mini_game_server_packet` reads its action-dependent body, and the normal server packet dispatcher reaches `ui_world_handle_mini_game_server_packet`. Action `4` continues through `ui_apply_mini_game_server_packet` and calls `ui_launch_mini_game`. Action `8`, subtype `1`, instead takes the world pane's dedicated [fishing](../../systems/fishing.md) path.

## Actions

| Value | Parsed body | Client behavior |
| ---: | --- | --- |
| `3` | one `u8` | Parsed, but no consumer was found. |
| `4` | one `u8` game selector | Opens or switches to a built-in mini game. |
| `5` | none | No server-packet behavior was found. The same value is the client's close notification in `CMiniGame`. |
| `6` | none | No server-packet behavior was found. |
| `7` | two `u32` values | Updates an existing Find Farmpet or Puzzle play pane. It does not open a pane. |
| `8` | one `u8` subtype | Subtype `1` checks the player's fishing position and opens `FishingDialogPane` when valid. |

Other action values do not cause the deserializer to read more bytes.

## Opening a game

Action `4` accepts these selectors:

| Selector | Client class | Initial UI |
| ---: | --- | --- |
| `1` | `RopeSkipping::Game` | Builds a `MiniGame::GameDialogPane` using `lminig.txt`. |
| `2` | `Puzzle::Game` | Builds the Puzzle dialog from `lpz_dlg.txt` with mode `1`. |
| `3` | `FindFarmpet::FindFarmpetPane` | Opens the dedicated Find Farmpet pane and loads its `fp_*.spf` art. |
| `4` | `Puzzle::Game` | Builds the Puzzle dialog from `lpz_dlg.txt` with mode `0`. |

Selectors outside `1` through `4` do nothing. If another mini game is active, the launcher closes it before constructing the requested one. Requesting the already active selector keeps the existing game.

The smallest useful plaintext bodies are therefore:

| Plaintext body | Expected result |
| --- | --- |
| `64 04 01` | Open Rope Skipping. |
| `64 04 02` | Open Puzzle mode `1`. |
| `64 04 03` | Open Find Farmpet. |
| `64 04 04` | Open Puzzle mode `0`. |

These are plaintext packet bodies, not complete socket frames. A server must still apply the normal server-to-client framing, derived transform, sequence, and trailer for opcode `0x64`.

## Opening fishing

The plaintext body `64 08 01` requests the fishing dialog. `ui_world_handle_mini_game_server_packet` requires a loaded map and local user, then checks the current ground tile and the next two tiles in the character's facing direction. The current tile's `gndattr.tbl` height-1 marker must be clear, and at least one of the next two tiles must have the height-2 marker. This behaves like a local shore-and-water eligibility check.

When the check succeeds, `ui_fishing_dialog_create` constructs the dialog. The world pane centers it on the game canvas, registers it, and supplies timer selector `0x0B` as its completion callback. The fish, hook, collision tests, and timing gauge then run locally on client timers.

When the check fails, the client displays localized message slot `0x80` and reports a failed fishing result without opening the dialog. See the paired `CMiniGame` action `8` body below.

### Asset archive requirement

The local installation keeps all 167 mini-game entries in `cious.dat`. This includes `lminig.txt`, `lpz_dlg.txt`, the other Puzzle layouts, Rope Skipping art, and the Find Farmpet `fp_*.spf` files. None of those entry names collide case-insensitively with entries in any of the other 20 legacy DAT archives in the installation.

The client does not open `cious.dat` during normal startup. These constructors pass no archive override to `ui_layout_load`, so the lookup falls back to the already-open `setoa.dat`. Sending `64 04 01` in this state reaches `RopeSkipping::Game`, fails to find `lminig.txt`, raises the client's fatal invalid-layout error, and terminates the process. Puzzle selectors `2` and `4` have the same problem with `lpz_dlg.txt`. Find Farmpet avoids that first text-layout lookup but still expects its art in the same unavailable archive.

This installation therefore needs its mini-game archive integrated before any selector is safe to test. The [Minigame support patch](../../appendix/runtime-patches/minigame-assets.md) opens `cious.dat` in a dormant client archive object and adds it as a lookup fallback while preserving `misc.dat`, `setoa.dat`, and every other original archive. It does not merge or rewrite the DAT files and does not use a DLL.

## Body

```text
packet SMiniGame {
    u8      opcode                    // 0x64
    u8      action

    if action == 3 {
        u8      value
    }

    if action == 4 {
        u8      game_selector
    }

    if action == 7 {
        u32     entry_id
        u32     value
    }

    if action == 8 {
        u8      subtype
    }
}
```

For action `7`, `FindFarmpet::FindFarmpetPane` applies `value` only when `entry_id` matches one of its two tracked IDs. `Puzzle::PlayPane` forwards both values to its active game state.

## Paired client packet

Closing `MiniGame::AbstractGame` or `FindFarmpet::FindFarmpetPane` sends [`CMiniGame`](../client/106-0x6a-mini-game.md) action `5`. Other game controls send actions `6` and `7`. Fishing completion returns action `8`, subtype `2`, with a client-calculated success flag.

## Known limits

The action-4 open path and selector mapping are confirmed both statically and by a runtime `64 04 01` test that reached the expected missing-`lminig.txt` failure. The runtime archive patch has not yet been tested in game. Fishing action `8`, subtype `1`, is statically confirmed but has not yet been observed in a live packet trace. The meanings of server action `3` and other action-8 subtypes remain unresolved.

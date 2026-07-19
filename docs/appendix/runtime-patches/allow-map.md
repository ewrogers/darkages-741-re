# Allow map

This patch lets the Tab map remain available when `SMapSize.flags` contains `NoMap`.

It applies only to the version 741 target with SHA-256 `054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6`.

## Target

At static data address `0x0068A5F1` (RVA `0x0028A5F1`, file offset `0x002891F1` for reference), replace:

```diff
- 000: 40 | db 0x40 ; NoMap mask used by map setup and the Tab handler
+ 000: 00 | db 0x00 ; make both client-side NoMap tests ignore the flag
```

The client reads this mask at two confirmed sites. Map setup uses it to close an overlay that is already open, and the world-pane Tab handler uses it to reject a new map request. A zero mask makes both bit tests false while leaving the `Winter` bit and low-nibble weather or lighting mode untouched.

This patch removes only the `NoMap` restriction. Non-Rogue characters still receive the normal non-zoomable map configuration unless [Map zoom](map-zoom.md) is also applied.

See [`SMapSize`](../../network/server/021-0x15-map-size.md) for the unpatched flag handling. Apply the change with the [safe launcher workflow](safe-launcher.md).

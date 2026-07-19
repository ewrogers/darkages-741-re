# Map zoom

This patch gives every character class the zoom-enabled Tab map configuration normally selected only for Rogues.

It applies only to the version 741 target with SHA-256 `054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6`.

## Target

At static address `0x005F0EC3` (RVA `0x001F0EC3`, file offset `0x001F02C3` for reference), replace:

```diff
- 000: 75 68 | jne fixed_map_scale ; non-Rogues use the non-zoomable configuration
+ 000: 90 90 | nop; nop            ; every class falls through to the zoom-enabled configuration
```

The world-pane Tab handler compares the current character class with `2`, the Rogue class value. Rogues fall through to the zoom-enabled overlay setup; other classes jump to a setup with a fixed scale. Removing only that jump reuses the existing Rogue path without changing the stored character class or any other class-dependent behavior.

The earlier `NoMap` check remains active. Use [Allow map](allow-map.md) as well when zoom should be available on maps that carry that flag.

See [`SMapSize`](../../network/server/021-0x15-map-size.md) for the complete Tab-map decision. Apply the change with the [safe launcher workflow](safe-launcher.md).

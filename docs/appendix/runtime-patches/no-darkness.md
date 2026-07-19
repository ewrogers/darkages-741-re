# No darkness

This patch disables the special lantern-style Darkness mode selected by the low nibble of `SMapSize.flags`.

It applies only to the version 741 target with SHA-256 `054A5D6ADC56099C6BFD9D2A58675AFF62DC788B63209A3D906492F5B89E96C6`.

## Target

At static data address `0x0068A5F7` (RVA `0x0028A5F7`, file offset `0x002891F7` for reference), replace:

```diff
- 000: 03 | db 0x03 ; recognize low-nibble mode 3 as Darkness
+ 000: FF | db 0xFF ; no low-nibble map mode can select Darkness
```

The client reads this constant in three places. They enable the black ambient-light setup, select the Darkness fallback in the map-lighting update, and attach lantern masks to human objects. `SMapSize.flags & 0x0F` can only produce `0x00` through `0x0F`, so changing the shared comparison constant to `0xFF` makes all three checks fail.

The patch leaves map loading, Snow mode, Rain mode, ordinary time-of-day lighting, and HEA masks unchanged. Maps without cached lighting metadata use the client’s normal non-Darkness fallback instead of starting from black.

See [`SMapSize`](../../network/server/021-0x15-map-size.md) and [Map lighting](../../rendering/lighting.md) for the unpatched flow. Apply the change with the [safe launcher workflow](safe-launcher.md).

# Hide walls

This patch skips drawing every static map object without changing collision or other world layers.

## Target

At static address `0x005E47FF` (RVA `0x001E47FF`), replace:

```diff
- 000: 74 05 | je draw_body        ; draw when the object's hidden byte is zero
+ 000: EB 00 | jmp skip_draw_branch ; land on the existing jump to the normal epilogue
```

`render_static_object` normally skips drawing only when the object's hidden byte is set. The patch forces the same existing jump to the normal function epilogue for every static object.

This hides walls, trees, and fixed map decorations. It does not hide ground, characters, items, or effects, and it does not change collision.

For a live `?` button toggle, use a DLL hook instead of rewriting these bytes while the process is running. The hook design is described in [Walls and occlusion](../../rendering/walls-and-occlusion.md).

Apply it with the [safe launcher workflow](safe-launcher.md).

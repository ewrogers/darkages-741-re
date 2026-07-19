# Hide map art

This patch skips drawing every static map object without changing collision or other world layers.

## Target

| Static address | RVA | Verify bytes and instruction | Write bytes and instruction |
| --- | --- | --- | --- |
| `0x005E47FF` | `0x001E47FF` | `74 05` `je draw_epilogue` | `EB 00` `jmp draw_epilogue` |

`render_static_object` normally skips drawing only when the object's hidden byte is set. The patch forces the same existing jump to the normal function epilogue for every static object.

This hides walls, trees, and fixed map decorations. It does not hide ground, characters, items, or effects, and it does not change collision.

For a live `?` button toggle, use a DLL hook instead of rewriting these bytes while the process is running. The hook design is described in [Walls and occlusion](../../rendering/walls-and-occlusion.md).

Apply it with the [safe launcher workflow](safe-launcher-workflow.md).

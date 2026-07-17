# Text color markup

Formatted text can change color in the middle of a string with a three-byte code:

```text
{=<letter>
```

The braces are not paired. A code changes the color of the text that follows until another code changes it again.

```text
{=uCharacter name
{=eHealth: 100 / 100
```

`ui_text_insert_formatted` passes the string to `ui_text_insert_color_markup`. The parser writes ordinary text as runs. When it sees a valid code, it finishes the current run, changes that run style's palette index, skips the three code bytes, and continues.

Only lowercase `a` through `x` are accepted. Uppercase letters and incomplete codes remain ordinary visible text. The actual letter `x` is valid and selects palette index 0.

## Code table

| Code | Palette index | Code | Palette index |
| --- | ---: | --- | ---: |
| `{=a` | `0x14` | `{=m` | `0x1E` |
| `{=b` | `0x28` | `{=n` | `0x1F` |
| `{=c` | `0x45` | `{=o` | `0x24` |
| `{=d` | `0x89` | `{=p` | `0x6D` |
| `{=e` | `0x58` | `{=q` | `0x80` |
| `{=f` | `0x5C` | `{=r` | `0x89` |
| `{=g` | `0x12` | `{=s` | `0x97` |
| `{=h` | `0x14` | `{=t` | `0xA7` |
| `{=i` | `0x16` | `{=u` | `0xFF` |
| `{=j` | `0x18` | `{=v` | `0x58` |
| `{=k` | `0x1A` | `{=w` | `0x24` |
| `{=l` | `0x1C` | `{=x` | `0x00` |

Several letters are aliases. `a` and `h`, `d` and `r`, `e` and `v`, and `o` and `w` select the same index.

These are palette indexes, not fixed RGB colors. The renderer resolves them through palette slot 0, loaded from `legend.pal`. `SSelfLook` legend-mark colors use this same palette path. Keep the numeric index as the stable definition when building another renderer.

## Plain and formatted controls

The code belongs to the rich text insertion path. A plain edit control may store the same bytes without interpreting them. This is why a profile can keep `{=u` in `profile.txt`, send those bytes to the server, and show colored text later when `UserInfoPane` feeds the returned profile to a formatted text control.

There is also a text-object flag that bypasses markup parsing. Code that creates a custom text pane must choose whether it wants formatted or literal text.

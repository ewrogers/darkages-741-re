# FNT fixed fonts

FNT belongs to an older fixed-size font path that remains compiled into the client. The matching assets are present, but the 7.41 renderer does not call their loaders. LFT is the active format.

## English files

`eng00.fnt` and `eng01.fnt` are each 1,128 bytes. That is 94 records of 12 bytes, one for every printable ASCII character from `!` (`0x21`) through `~` (`0x7E`).

The dormant loader allocates a 256 by 12-byte table and copies the file to offset `0x18C`, which is `0x21 * 12`. This makes the character byte usable as the direct record index. Space is handled separately.

```c
struct EngFnt {
    u8 glyph[94][12];
};
```

## Korean files

`han00.fnt` through `han03.fnt` are each 57,624 bytes. Each glyph occupies 24 bytes, so every file contains 2,401 glyphs.

The dormant mapper recognizes two code page 949 ranges:

- `B0A1` through `C8FE`: 2,350 precomposed Hangul syllables from the KS X 1001 Wansung set
- `A4A1` through `A4D3`: 51 Hangul jamo records placed after those syllables

```c
struct HanFnt {
    u8 syllables[2350][24];
    u8 jamo[51][24];
};
```

Bytes outside those ranges fall back to one built-in 24-byte glyph.

## Status

`Darkages.cfg` still reads and writes `EngFont` and `HanFont` indexes, but the matching loader functions have no code or data references and are not virtual methods. The exact bit-to-pixel orientation of these dormant records is not yet verified through a live drawing call.

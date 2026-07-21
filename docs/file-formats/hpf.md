# HPF static images

HPF stores palette-indexed static art such as `stcNNNNN.hpf`. Most files use a small adaptive bit-tree codec. The same reader also accepts uncompressed input.

## Stream format

```text
file HpfCompressedStream {
    u32le magic               // 0xFF02AA55
    bits_lsb_first tree_stream[to end_of_file]
}
```

If the magic is absent, `file_hpf_decode` copies the input unchanged. This is an intentional raw fallback, not a failed decode.

The inspected static-art archive contains 23,506 HPF entries. Of those, 22,665 use the magic and codec, while 841 use the raw fallback.

The tree has byte symbols 0 through 255 plus symbol 256 as the end marker. It begins as a complete binary tree. A zero bit follows the left child and a one bit follows the right child. After each byte, and after the end marker, the tree rotates using the same rule.

## Decode

```text
decode_hpf(input):
    if read_u32_le(input) != 0xFF02AA55:
        return copy(input)

    tree = complete_tree(symbols = 0 .. 256)
    output = []

    loop:
        node = tree.root
        while node is not a symbol:
            bit = read_bit_lsb_first(input)
            node = bit == 0 ? node.left : node.right

        symbol = node.symbol
        rotate_tree(tree, node)

        if symbol == 256:
            return output
        output.push(symbol)
```

The rotation is the unusual part. Preserve it exactly in both directions.

```text
rotate_tree(tree, node):
    while parent[node] != root_parent:
        p = parent[node]
        g = parent[p]
        other = child of g that is not p

        replace p with node under g
        replace node with other under p
        parent[node] = g
        parent[other] = p
        node = g
```

## Encode

Encoding is the inverse walk. For each input byte, find its leaf, record the path from leaf to root, write that path in root-to-leaf order, then rotate the tree. Finish by writing symbol 256 and rotating once more.

```text
encode_hpf(bytes):
    write_u32_le(0xFF02AA55)
    tree = complete_tree(symbols = 0 .. 256)

    for symbol in bytes followed by 256:
        path = path_from_leaf_to_root(tree, symbol)
        write_reversed_path_lsb_first(path)
        rotate_tree(tree, leaf(symbol))
```

This encoder was checked by decoding, encoding, and decoding several local static images. The generated compressed bytes matched those samples exactly.

## Decoded static image

`file_open_static_tile` ignores the first eight decoded bytes. The remaining bytes are palette indexes for an image that is 28 pixels wide.

```text
decoded HpfStaticImage {
    bytes unknown_header[8]   // preserve exactly
    u8 palette_indexes[to end_of_decoded_data]
}

width = 28
height = palette_indexes.length / 28
```

The palette comes from `stcpal.tbl`. In the common sprite path, palette index 0 is transparent. See [PAL files](pal.md) and [Exporting images](image-export.md).

## Evidence

- `file_hpf_decode` at `0x004319B0`
- `file_hpf_tree_initialize` at `0x00431B80`
- `file_hpf_decode_symbol` at `0x00431C40`
- `file_hpf_rotate_tree` at `0x00431D20`
- `file_load_static_tile_pixmap` at `0x005FD500`
- `file_open_static_tile` at `0x005FD700`

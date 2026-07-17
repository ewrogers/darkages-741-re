# Packet body notation

Packet pages use a small field-list notation that reads in the same order as the bytes on the wire. It is meant to show the protocol directly, without C padding, compiler rules, or packet-object memory offsets.

Every multibyte integer in a Dark Ages packet is big-endian. The packet schemas therefore use short names such as `u16`, `u24`, and `u32` without repeating an endian suffix on every field.

This rule applies to packet bodies and the common frame header. File formats and runtime memory structures state their own byte order separately.

## Basic shape

```text
packet SExample {
    u8      opcode                    // command byte
    u16     entity_id
    string8 name
}
```

`packet` describes one complete plaintext packet body. The first field is the opcode. The common `AA` marker, body size, encryption transform, sequence, and trailer belong to the framing layer and are not repeated on every page.

Fields appear in wire order. The notation does not use semicolons because it is a protocol description, not a C declaration.

A capitalized field comment such as `// Direction` names a type from [Shared protocol types](protocol-types.md). The packet page links to the matching value table and keeps only behavior unique to that packet.

## Field types

| Type | Wire encoding |
| --- | --- |
| `u8`, `s8` | One unsigned or signed byte |
| `u16`, `s16` | Two-byte big-endian integer |
| `u24`, `s24` | Three-byte big-endian integer |
| `u32`, `s32` | Four-byte big-endian integer |
| `string8` | `u8` byte length followed by that many text bytes |
| `bytes value[count]` | Exactly `count` opaque bytes |

`string8` is byte text, not a promise of Unicode. The client may interpret those bytes through an ANSI code page, including Korean code page 949 where applicable.

An array count may use an earlier field or a simple expression. For example, `bytes greeting[body_size - 2]` consumes the rest of a body whose common frame size includes the opcode and one control byte.

## Conditional and repeated blocks

```text
packet SExample {
    u8 opcode
    u8 flags

    if flags & 0x01 {
        u32 health
        u32 mana
    }

    u8 entry_count
    repeat entry_count {
        u16 icon
        string8 name
    }
}
```

A conditional block is present only when its expression is true. A `repeat` block consumes the enclosed fields in order for the stated count. Nested braces make the exact scope visible.

`record` names a nested or separately explained group of fields when that makes a large packet easier to read:

```text
record legend_mark {
    u8      icon
    u8      color
    string8 key
    string8 text
}
```

A record is still wire data. It is not a claim about the client object's in-memory layout. A record may appear inside a packet at the exact point where its fields are consumed.

## Values and uncertainty

Comments may record constants, observed ranges, or parser behavior:

```text
u8 opcode                    // 0x39
u8 ignored_after_name        // consumed but not interpreted
u8 observed_trailing_zero    // captured, but not consumed by this parser
```

Names beginning with `unknown_` preserve fields whose purpose is unresolved. An `ignored_` field is consumed by the client but not used. An `observed_trailing_` field was seen in captures but lies beyond what the verified parser reads.

Object-relative offsets and local buffer sizes belong in the runtime-structure appendix. Packet schemas describe only the wire body.

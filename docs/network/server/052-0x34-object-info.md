# Object Info (`SObjectInfo`)

`SObjectInfo` supplies another character's equipment appearance, identity text, legend entries, portrait, and profile. It is the response paired with [`CRequestObjectInfo`](../client/067-0x43-request-object-info.md).

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x34` |
| Transform | `derived` |
| Name provenance | Provisional project-owner protocol name |
| RTTI | No concrete server-packet RTTI class |
| UI owner | Exact RTTI `UserInfoPane_ForOthers` |

## Body

```text
packet SObjectInfo {
    u8 opcode                    // 0x34
    u32 object_id

    repeat 18 {
        u16 equipment_sprite
        u8 equipment_color
    }

    u8 identity_flag_1
    string8 name
    u8 identity_flag_2
    string8 identity_text_2
    u8 identity_flag_3
    string8 identity_text_3
    string8 identity_text_4
    string8 identity_text_5

    u8 legend_count
    repeat legend_count {
        u8 icon
        u8 color
        string8 key
        string8 text
    }

    u16 content_length           // 4 + portrait_length + profile_length
    u16 portrait_length
    bytes portrait[portrait_length]
    string16 profile
}
```

The parser proves the order and widths, but the three identity flag meanings and four identity-text roles are not yet resolved. The 18 equipment records are remapped through the same user-info slot table used elsewhere rather than being displayed in wire order.

The nested portrait/profile tail uses the same decoder and length convention as [`CSendPortrait`](../client/079-0x4f-send-portrait.md). Either nested field may be empty.

## UI routing

The decoded body bypasses the server packet factory. Its handler first finds `object_id` in the current world and requires that object to be a living object. It then creates or refreshes exact RTTI `UserInfoPane_ForOthers`, applies the equipment and identity fields, rebuilds the legend list, and decodes the portrait and profile.

If the object is absent or is not a living object, the client consumes the packet without opening the pane.

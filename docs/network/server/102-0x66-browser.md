# Browser (`SBrowser`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x66` (102) |
| Transform | `static` |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

This packet carries browser-related data. Subtype `3` supplies the homepage URL requested by [`CRequestHomepage`](../client/104-0x68-request-homepage.md).

The constructor calls `net_server_packet_base_ctor` with opcode `0x66` and installs the `SBrowser` vtable. `net_server_packet_factory_ctor` registers the same opcode with this constructor.

`SBrowser` is the exact RTTI name. “Homepage URL” is the narrower behavioral name for subtype `3`; it does not replace the class name.

## Body

```text
packet SBrowser {
    u8      opcode                    // 0x66
    u8      subtype

    if subtype == 1 || subtype == 2 {
        u16     first_size
        bytes   first_data[first_size]
        u16     second_size
        bytes   second_data[second_size]
    }

    if subtype == 3 {
        u8      url_size
        bytes   url[url_size]
    }
}
```

`net_handle_browser` opens related URL alert panes for subtypes `1` and `2`. The exact roles of their two byte strings remain unresolved.

For subtype `3`, the handler copies the URL into a 256-byte global buffer and marks it available. The observed body is:

```text
66 03 17 "http://www.darkages.com"
```

The handler caches this value; it does not immediately launch a browser.

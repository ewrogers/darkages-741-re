# Block Listen (`CBlockListen`)

`CBlockListen` asks the server to list or change the current character's ignored users. The historic packet name says "block listen," while the player-facing behavior is an ignore list.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0D` (13) |
| Transform | `derived` |
| Runtime owners | `BlockListenInputPane`, `AddToBlockListenInputPane`, `DeleteFromBlockListenInputPane` |
| Name provenance | Project-owner protocol vocabulary, supported by exact RTTI pane names |

## Body

```text
packet CBlockListen {
    u8      opcode                    // 0x0D
    u8      operation                 // BlockListenOperation

    if operation == 2 || operation == 3 {
        string8 character_name
    }
}
```

The client builds three operations:

| Value | Operation | Remaining body |
| ---: | --- | --- |
| `1` | List | None |
| `2` | Add | `string8 character_name` |
| `3` | Remove | `string8 character_name` |

The ordinary add and remove UI copies at most 15 name bytes and does not send empty input. The packet text is the client's byte-oriented game text, not Unicode. The builders place a trailing zero in scratch memory, but that zero is outside the submitted packet length and is not transmitted.

No other operation value is produced by the traced client.

## UI flow

`ui_open_block_listen_input` creates the singleton `BlockListenInputPane`. The gameplay shortcut reaches it through translated key code `0x8D`; the physical key mapping remains unresolved.

The pane accepts one command character:

- `?` sends operation `1` to list ignored users.
- `A` or `a` opens RTTI class `AddToBlockListenInputPane`; nonempty input sends operation `2`.
- `D` or `d` opens RTTI class `DeleteFromBlockListenInputPane`; nonempty input sends operation `3`.

The three panes use localized prompt-string indexes `0x1C`, `0x1D`, and `0x1E`. Their literal text depends on the installed client data and is not reproduced here.

## Ownership and persistence

The client keeps only transient input-pane state and a singleton pointer for the open `BlockListenInputPane`. This flow has no local ignored-user collection, cache file, or registry persistence.

Project-owner runtime behavior confirms that the list is stored by the server per character. It remains in effect after using a different computer or client installation. The client therefore sends add, remove, and list commands but does not own the durable list.

The exact server response packet used for list output and success or error feedback is not yet confirmed by a capture. Server opcode [`0x0D`](../server/013-0x0d-say.md) is the unrelated `SSay`; command numbers are direction-specific.

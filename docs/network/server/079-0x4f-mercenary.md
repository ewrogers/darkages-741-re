# Mercenary (`SMercenary`)

`SMercenary` opens and updates `EmployeeDialogPane`, the employee shop UI paired with [`CMercenary`](../client/084-0x54-mercenary.md). This path handles the decoded body directly and does not construct a concrete RTTI server-packet class.

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Opcode | `0x4F` |
| Transform | `derived` |
| Name provenance | Project-owner protocol name; client debug strings call the body an Employee packet |
| RTTI | No concrete server-packet RTTI class |
| UI owner | Exact RTTI `EmployeeDialogPane` |

## Body

```text
packet SMercenary {
    u8 opcode                    // 0x4F
    u8 category                  // must be 1
    u32 employee_id
    u8 message_code

    if message_code == 0 {
        u32 gold
        u8 capacity
        u8 item_count

        repeat item_count {
            u32 item_id

            if item_id == 0 {
                u32 gold_entry
            }

            if item_id != 0 {
                u16 sprite
                u8 color
                string8 name
                u8 has_description

                if has_description == 1 {
                    string8 description
                }

                u8 unknown
                u32 quantity
                u32 sell_price
                u32 buy_price
            }
        }
    }

    if message_code == 1 {
        u32 item_id

        if item_id == 0 {
            u32 gold_entry
        }

        if item_id != 0 {
            u16 sprite
            u8 color
            string8 name
            u8 has_description

            if has_description == 1 {
                string8 description
            }

            u8 unknown
            u32 quantity
            u32 sell_price
            u32 buy_price
        }
    }

    if message_code == 2 {
        u32 item_id
    }

    if message_code == 3 {
        u32 previous_item_id
        u32 item_id                 // nonzero
        u16 sprite
        u8 color
        string8 name
        u8 has_description

        if has_description == 1 {
            string8 description
        }

        u8 unknown
        u32 quantity
        u32 sell_price
        u32 buy_price
    }

    if message_code == 4 {
        string8 message
    }
}
```

The client rejects other category values. An open pane also rejects messages whose `employee_id` does not match its saved ID.

| Code | Client debug name | Behavior |
| ---: | --- | --- |
| `0` | `Open` | Create or replace the employee-shop state |
| `1` | `AddItem` | Add or update one item or gold entry |
| `2` | `RemoveItem` | Clear one item |
| `3` | `StartTrade` | Replace the matched item with trade state |
| `4` | `RequestResponse` | Show the returned employee message |

Only code `0` can create `EmployeeDialogPane`. Codes `1` through `4` are consumed by the pane after it exists.

## Opening handshake

The central packet dispatcher recognizes decoded opcode `0x4F`. When `category` is `1` and `message_code` is `0`, it allocates `EmployeeDialogPane` and passes the complete body to its constructor. After building `lshop0.txt` and applying the Open payload, the constructor immediately sends `CMercenary` action `5`, RequestInfo.

## Minimal test body

This plaintext body supplies employee ID `1`, zero gold, zero capacity, and no item records:

```text
4F 01 00 00 00 01 00 00 00 00 00 00 00
```

If the pane opens successfully, the client immediately sends this plaintext `CMercenary` RequestInfo body for the same employee ID:

```text
54 01 00 00 00 01 05
```

The normal derived transform and packet framing still apply outside these plaintext bodies. The test also depends on the local `lshop0.txt` layout being present and no existing `EmployeeDialogPane` singleton blocking construction.

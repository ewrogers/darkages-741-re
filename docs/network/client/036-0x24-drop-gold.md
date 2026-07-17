# Drop Gold (`CDropGold`)

`CDropGold` asks the server to remove some of the character's gold and place it on the ground. The packet carries the tile selected by the player, but the server places the gold beneath the character instead.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x24` (36) |
| Transform | derived |
| Runtime owner | `DropGoldDialogPane` |
| Success | `SDrawObjects` ground item beneath the character |
| Rejection | `SMessage` for a distant target or insufficient gold |
| Name provenance | Project-owner protocol name, confirmed against the local builder |

## Plaintext body

```text
packet CDropGold {
    u8      opcode                    // 0x24
    u32     amount
    u16     x
    u16     y
}
```

The body is 9 bytes including the opcode. Unlike [`CDrop`](008-0x08-drop.md), it does not include an inventory slot.

## Dialog flow

Dragging inventory slot `60` into the world opens `DropGoldDialogPane` instead of sending an item drop. The dialog retains the selected target tile and asks the player for an amount through the `_nmoney.txt` controls.

Action `0` parses and submits the amount. Action `1` cancels and closes the dialog. A parsed amount of zero also closes the dialog without sending `CDropGold`.

`net_send_drop_gold` writes the nonzero amount first, followed by the retained X and Y coordinates.

## Coordinate behavior

The client sends the map tile selected during the drag. It does not replace those fields with the character's current position before transmission.

The server does not honor the supplied X and Y for final placement. Project-owner behavior confirms that dropped gold always appears on the character's tile. However, the server can reject a target that is too far away, so the requested coordinates still participate in distance validation.

## Server outcome

On success, the server sends [`SDrawObjects`](../server/007-0x07-draw-objects.md) with a ground-item record on the character's tile. The server chooses the item sprite to indicate the relative size of the dropped amount. Observed representations include a silver coin, gold coin, silver pile, and gold pile.

The `SDrawObjects` item record does not carry the numeric gold amount. The client therefore does not calculate the coin-or-pile tier from the amount. It renders the sprite selected by the server. The exact amount thresholds and sprite IDs for each representation remain unconfirmed.

If the selected tile is too far away or the character does not have the requested amount, the server sends [`SMessage`](../server/010-0x0a-message.md) instead.

The body, dialog actions, zero-amount behavior, and origin of the transmitted coordinates are confirmed in the version 741 binary. Placement beneath the character, distance validation, insufficient-gold rejection, and server-side sprite selection are project-owner server behavior.

# Change Direction (`CChangeDirection`)

`CChangeDirection` asks the server to turn the local player without moving. The body carries only the requested facing because the connection already identifies the player.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x11` (17) |
| Transform | derived |
| Runtime owner | `WorldPane` |
| Name provenance | Project-owner protocol name, confirmed against the world input path |

## Turning locally

Directional input first compares the requested direction with the local `WorldObject_User` facing. A different direction turns the player and sends `CChangeDirection`. Pressing the same direction attempts a one-tile [`CMove`](006-0x06-move.md) instead.

Keyboard and pointer input produce only the four cardinal [`Direction`](../protocol-types.md#direction) values. An interaction with an adjacent object can also turn the player toward that object before continuing the action.

`ui_world_pane_request_change_direction` updates the local facing first and then calls `net_send_change_direction`. This makes the turn visible immediately rather than waiting for the network round trip.

The client has no derived packet RTTI for this name. The builder writes opcode `0x11` followed by one direction byte and submits the two-byte plaintext body.

## Plaintext body

```text
packet CChangeDirection {
    u8      opcode                    // 0x11
    u8      direction                 // Direction
}
```

`direction` uses the shared [`Direction`](../protocol-types.md#direction) type.

## Server update

The normal response is [`SChangeDirection`](../server/017-0x11-change-direction.md), which includes a 32-bit object ID as well as the direction. That form lets the server confirm or correct the local player and turn any other living object in view.

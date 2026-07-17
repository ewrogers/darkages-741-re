# Request Object (`CRequestObject`)

`CRequestObject` asks the server to describe a world object that the client cannot update safely. Change-direction and speech handlers use it for an unknown ID, while another movement handler also uses it when the current object is not the expected living type.

| Item | Value |
| --- | --- |
| Direction | Client to server |
| Command | `0x0C` (12) |
| Transform | derived |
| Runtime owner | `WorldPane` |
| Response | `SDrawObjects` or `SDrawHumanObjects` |
| Name provenance | Project-owner protocol name, confirmed against the local builder |

## Purpose

The builder writes opcode `0x0C`, a four-byte big-endian object ID, and submits a five-byte body. Confirmed callers send it after a world-object lookup misses or the found object cannot be treated as the expected living object.

One confirmed recovery path is [`SChangeDirection`](../server/017-0x11-change-direction.md). If its target is absent, the client sends this request with `SChangeDirection.user_id`.

The client has no derived packet RTTI for this name.

## Plaintext body

```text
packet CRequestObject {
    u8      opcode                    // 0x0C
    u32     object_id
}
```

There are no other request fields.

## Server response

The server looks up `object_id` and answers with the normal packet for that object's type:

- [`SDrawObjects`](../server/007-0x07-draw-objects.md) for creatures, Mundanes, and ground items.
- [`SDrawHumanObjects`](../server/051-0x33-draw-human-objects.md) for player and other human objects.

Those packets create or replace the matching local world object. This response selection is project-owner protocol behavior. The request layout and the client-side object-recovery callers are independently confirmed in the version 741 binary.

# Translucent walk refresh

This injected runtime mitigation preserves a Hide or unhide appearance change that arrives while the local player is taking a step. It defers the current-user `SDrawHumanObjects` record until movement commits, replaces its stale coordinates with the committed tile, and replays it through the native server-event dispatcher.

## Trigger and evidence

A captured hidden record described the local player at `(9, 16)`. The following movement acknowledgement left native state at `(10, 16)` with walking idle. The client stayed visually unhidden and on the old tile until F5, after which it showed the player translucent at `(10, 16)`.

The issue reproduces for both entering and leaving Hide during a step. The same updates work while stationary. Equipment-only `SDrawHumanObjects` records are excluded because they do not change hidden state and observed equipment changes finish the movement normally.

## Runtime design

The decoded-event observer runs after the ordinary handler. It considers only a current-user `SDrawHumanObjects` record whose parsed hidden or translucent state differs from native state. It copies the record into one fixed 256-byte slot and coalesces a newer matching update over an older one.

The main-thread tick normally returns after checking one validity flag. For a pending record, it waits until native walking is idle and native coordinates differ from the stale packet coordinates. It then writes the committed X and Y to body offsets `1` and `3` as big-endian `u16` values and calls the native dispatcher. A replay flag prevents the observer from queuing its own replay. Pending data expires after two seconds.

```c
on_self_draw(body, parsed) {
    if (parsed.hidden == native_hidden())
        return;
    pending = copy_bounded(body, parsed.x, parsed.y, now);
}

on_tick() {
    if (!pending.valid)
        return;
    if (expired(pending, now)) {
        clear_pending();
        return;
    }
    if (native_is_walking())
        return;

    current = native_position();
    if (current == pending.packet_position)
        return;

    write_u16_be(pending.body + 1, current.x);
    write_u16_be(pending.body + 3, current.y);
    dispatch_server_event(pending.body);
    clear_pending();
}
```

## Why coordinates are rewritten

Replaying the record unchanged would reintroduce its pre-step tile. F5 demonstrates the desired combined state: the new appearance at the acknowledged tile. Substituting the committed native coordinates produces that same combination after the acknowledgement.

## Scope and safety

The implementation validates the client fingerprint and runs on the main thread. The hooks perform no allocation, logging, IPC, or waiting. Packet storage is bounded, stale work expires, and the original executable is not modified.

## Verification

The project owner reproduced the failure and confirmed the mitigation in a live Eidolon session. The implementation is in da-rpc commit [`fe548f366acc780d44e237a747f600f6c2d17c5e`](https://github.com/ewrogers/da-rpc/commit/fe548f366acc780d44e237a747f600f6c2d17c5e). Its workspace tests, Clippy checks, mdBook build, focused 32-bit Windows tests, and hook harness passed. The optimized idle path averaged zero microseconds over about 309,000 calls, with a measured maximum of 398 microseconds.

## Rejected instruction patch

An earlier proposed in-place change at static address `0x005F36F1`, from `75 1E` to `75 2A`, was tested and did not correct the behavior. It must not be deployed as the solution. The working mitigation is the deferred, coordinate-corrected replay described above.

# Level Point (`SLevelPoint`)

| Item | Value |
| --- | --- |
| Direction | Server to client |
| Command | `0x3D` (61) |
| Encoding | derived |
| Name provenance | Microsoft C++ RTTI in the target |

## Purpose

The server uses this packet to update the available level-up points in `StatusInfoPane` and make the related controls flash. It is a focused version of two fields that also appear in [`SStatus`](008-0x08-status.md).

The class and its UI handler are both live in this client. Whether the matching server still sends it during normal play remains a runtime question.

## Body

```text
packet SLevelPoint {
    u8      opcode                    // 0x3D
    u8      has_stat_points
    u8      stat_points
}
```

`net_deserialize_level_point_server_packet` reads exactly these two payload bytes. It does not range-check either value.

`has_stat_points` gates drawing the five stat-increase controls. Zero hides them and any nonzero value shows them. `stat_points` is the displayed point count. The pointer handler also formats `Level Up Point : %d` while the pointer is inside the pane and the count is nonzero.

## Flashing behavior

`ui_status_info_apply_level_point_packet` copies both fields into pane-owned state, clears the pane's existing timers, and invalidates the pane for redraw. If `stat_points` is nonzero, it starts timer `0` with a 500 ms delay.

Each timer tick toggles a one-byte phase between zero and one, redraws the pane, and schedules the next 500 ms tick while the count remains nonzero. The draw path uses that phase to alternate the point count and the normal stat-button artwork. A zero count stops further ticks, but does not explicitly reset the phase byte.

## Relationship to `SStatus`

The `SStatus` stats block contains the same fields in the same order. `StatusInfoPane` copies them to the same two local bytes:

```text
SLevelPoint.has_stat_points -> StatusInfoPane +0x1ED
SLevelPoint.stat_points     -> StatusInfoPane +0x1EC
```

The important difference is the timer. The `SStatus` handler only copies the values. It does not clear or start the flashing timer. `SLevelPoint` therefore remains useful as a focused notification even though the complete status packet can carry the current values.

The packet changes no session-wide character model in the identified path. Its state is owned by `StatusInfoPane`. Receiving it sends no immediate client response. Activating one of the five visible controls sends [`CAddStat`](../client/071-0x47-add-stat.md), and the client waits for a later server update rather than decrementing the count locally.

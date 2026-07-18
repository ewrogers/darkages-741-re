# Skip the intro

This patch follows the client's normal post-video state instead of creating the intro pane.

## Target

| Static address | RVA | Verify | Write |
| --- | --- | --- | --- |
| `0x004ACA85` | `0x000ACA85` | `6A 01` | `6A 02` |

`event_handle_intro_state` normally posts intro state 1. The patch posts state 2 instead.

State 2 is the normal continuation after both video clips finish. This is narrower than changing Bink playback because it follows the client's own state machine and avoids creating the video pane.

Apply it with the [safe launcher workflow](safe-launcher-workflow.md).

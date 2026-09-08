# Application

The application layer brings the client to life, keeps it running, and closes it cleanly. It covers startup, configuration, crash reporting, and shutdown. The [game loop](game-loop.md) has its own chapter for the repeated work of the running client.

## Choose a starting point

| Question | Start with | Then follow |
| --- | --- | --- |
| How does the client reach the running game? | [Application lifecycle](lifecycle.md) | [Game loop](game-loop.md) for messages, events, and timers |
| Which startup settings apply to this build? | [Distribution markers](distribution-markers.md) | [Configuration](configuration.md), keeping active and dormant parsers separate |
| Why does the client need writable files or administrator mode? | [Program Files and administrator mode](program-files-and-administrator.md) | [Configuration](configuration.md) for the files and settings involved |
| What happens when the window loses focus? | [Background-window behavior](game-loop.md#foreground-and-minimized-windows) | [Renderer lifecycle](../rendering/lifecycle.md) for presentation |

## Read next

- [Application lifecycle](lifecycle.md) follows startup through shutdown.
- [Configuration](configuration.md) explains startup settings and command-line behavior.
- [Distribution markers](distribution-markers.md) separates the active distribution from dormant regional support.
- [Program Files and administrator mode](program-files-and-administrator.md) explains writable client files and the patcher handoff.
- [CPU affinity](cpu-affinity.md) separates client behavior from the optional DirectDraw wrapper that can restrict the process to CPU 0.
- [Crash reporting](crash-reporting.md) follows the exceptional exit path.

Continue with [Game loop](game-loop.md) for the repeated work that drives the running client.

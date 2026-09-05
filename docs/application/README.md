# Application

The application layer brings the client to life, keeps it running, and closes it cleanly. It covers the work around the game itself: startup, configuration, the main loop, crash reporting, and shutdown.

## Read next

- [Application lifecycle](lifecycle.md) follows startup through shutdown.
- [Configuration](configuration.md) explains startup settings and command-line behavior.
- [Distribution markers](distribution-markers.md) separates the active distribution from dormant regional support.
- [Program Files and administrator mode](program-files-and-administrator.md) explains writable client files and the patcher handoff.
- [CPU affinity](cpu-affinity.md) separates client behavior from the optional DirectDraw wrapper that can restrict the process to CPU 0.
- [Crash reporting](crash-reporting.md) follows the exceptional exit path.

Continue with [Game loop](game-loop.md) for the repeated work that drives the running client.

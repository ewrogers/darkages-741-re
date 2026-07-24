# Application

The application layer brings the client to life, keeps it running, and closes it cleanly. It covers the work around the game itself: startup, configuration, the main loop, crash reporting, and shutdown.

Start with [Application lifecycle](lifecycle.md) for the full flow. [Configuration](configuration.md) and [Distribution markers](distribution-markers.md) explain the choices made during startup. [Program Files and administrator mode](program-files-and-administrator.md) explains why writable client files and the patcher conflict with a protected installation. [Game loop](game-loop.md) covers the repeated work that drives the running client, while [Crash reporting](crash-reporting.md) describes the exceptional path.

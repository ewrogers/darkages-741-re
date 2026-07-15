# User interface

The version-741 UI is a C++ pane hierarchy backed by declarative text layouts stored in `setoa.dat`. The archive files define geometry and presentation. C++ pane constructors choose concrete control classes, attach children, and handle actions.

- [Declarative layout files](layout-files.md)
- [UI loading, input, and rendering](runtime.md)
- [UI pane class catalog](pane-classes.md)
- [SStatus character and bottom-bar field mapping](../network/server/008-0x08-status.md)

The executable retains Microsoft Visual C++ RTTI names for hundreds of pane and control classes. These names are authoritative internal names from this client, not names inferred from another game.

The machine-readable class export is `ida/exports/ui-pane-classes.yaml`. It records RTTI string addresses and confirmed links to archive layouts and friendly functions.

## Main finding

The layout files do not register callbacks by name. A pane constructor looks up controls such as `OK`, `Cancel`, `Name`, and `Password`, constructs a concrete pane for each one, and attaches the children in a fixed order. The parent receives a numeric child ID and handles it in a virtual action method.

This division explains why changing a rectangle or sprite in an archive can change appearance without changing behavior, while adding a new named control does not create working behavior by itself.

# File formats

The client uses a mix of memory-mapped resource archives and small text configuration files. This section records byte layouts, compression, reversible transforms, and minimal C-style examples suitable for writing independent readers.

- [Fastfile `.dat` archives](fastfile-archives.md)
- [Compression](compression.md)
- [Configuration, NFO, profile, and table files](config-and-table-files.md)
- [Declarative UI layout files](../ui/layout-files.md)

The version-741 binary is the source for the layouts and transforms documented here. Original game assets are not part of this repository.

When adding a format, include its byte order, field widths, storage location, transforms, compression, parser addresses, and confidence level. Keep compression separate from encryption or scrambling even when they appear in the same container.

UI layout text is documented under the [UI subsystem](../ui/README.md) because its archive representation, pane construction, input handling, and rendering need to be read together.

# Binary Ninja scripts

Place reusable Binary Ninja import, export, validation, and focused analysis scripts here.

Scripts must be cross-platform, must not depend on a hard-coded Binary Ninja installation path, and must not write original client bytes or secrets into committed output. An exporter should be deterministic, and its importer should be tested against a fresh local `.bndb` before the format is treated as stable.

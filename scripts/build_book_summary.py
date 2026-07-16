#!/usr/bin/env python3
"""Build mdBook navigation from the stable section list and packet pages."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUTPUT = DOCS / "SUMMARY.md"


def title(path: Path) -> str:
    first = path.read_text(encoding="utf-8").splitlines()[0]
    return first.removeprefix("# ")


def packet_lines(directory: str, indent: str) -> list[str]:
    base = DOCS / "network" / directory
    lines = []
    for path in sorted(base.glob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(DOCS).as_posix()
        opcode = path.stem.split("-", 2)[1]
        opcode = "0x" + opcode.removeprefix("0x").upper()
        lines.append(f"{indent}- [{opcode} - {title(path)}]({relative})")
    return lines


def main() -> None:
    lines = [
        "# Summary",
        "",
        "- [Inside the Dark Ages client](README.md)",
        "- [Getting started](getting-started.md)",
        "- [How we study the client](methodology.md)",
        "",
        "# Application",
        "",
        "- [Application lifecycle](application/lifecycle.md)",
        "- [Configuration](application/configuration.md)",
        "- [Game loop](application/game-loop.md)",
        "",
        "# Game systems",
        "",
        "- [Event system](systems/events.md)",
        "- [UI and panes](systems/ui.md)",
        "- [Event proxy design](systems/event-proxy.md)",
        "",
        "# Rendering",
        "",
        "- [Rendering system](rendering/README.md)",
        "- [Renderer lifecycle](rendering/lifecycle.md)",
        "- [World rendering](rendering/world.md)",
        "- [Snow and weather](rendering/weather.md)",
        "- [Walls and occlusion](rendering/walls-and-occlusion.md)",
        "- [Blending](rendering/blending.md)",
        "",
        "# Audio",
        "",
        "- [Audio system](audio/README.md)",
        "- [Audio lifecycle](audio/lifecycle.md)",
        "- [Music](audio/music.md)",
        "- [Sound effects](audio/sound-effects.md)",
        "- [MIDI support](audio/midi.md)",
        "",
        "# File formats",
        "",
        "- [File formats](file-formats/README.md)",
        "- [DAT archives](file-formats/dat-archives.md)",
        "- [HPF static images](file-formats/hpf.md)",
        "- [HEA light masks](file-formats/hea.md)",
        "- [PAL color palettes](file-formats/pal.md)",
        "- [TBL lookup files](file-formats/table-files.md)",
        "- [Compression and checks](file-formats/compression.md)",
        "- [Metadata files](file-formats/metadata.md)",
        "- [Exporting images](file-formats/image-export.md)",
        "- [MAP files](file-formats/map.md)",
        "- [Raw map tile banks](file-formats/map-tile-banks.md)",
        "- [Tile animation tables](file-formats/tile-animation-tables.md)",
        "- [SOTP static tile flags](file-formats/sotp.md)",
        "- [EPF images](file-formats/epf.md)",
        "- [SPF images](file-formats/spf.md)",
        "- [EFA effects](file-formats/efa.md)",
        "- [Effect.tbl](file-formats/effect-table.md)",
        "",
        "# Network",
        "",
        "- [Network system](network/README.md)",
        "- [Initial connection](network/connection.md)",
        "- [Network transport](network/transport.md)",
        "- [Packet transforms](network/packet-transforms.md)",
        "- [Checksums](network/checksums.md)",
        "- [Server list and greeting](network/server-tables.md)",
        "- [Client packets](network/client/README.md)",
    ]
    lines.extend(packet_lines("client", "  "))
    lines.append("- [Server packets](network/server/README.md)")
    lines.extend(packet_lines("server", "  "))
    lines.extend([
        "",
        "# Appendices",
        "",
        "- [Function reference](appendix/functions.md)",
        "- [Runtime patches](appendix/runtime-patches.md)",
        "- [Runtime structures](appendix/runtime-structures.md)",
        "- [Pane types and inheritance](appendix/pane-types.md)",
    ])

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

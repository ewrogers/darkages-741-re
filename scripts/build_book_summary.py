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
        "- [Distribution markers](application/distribution-markers.md)",
        "- [Game loop](application/game-loop.md)",
        "",
        "# Game systems",
        "",
        "- [Event system](systems/events.md)",
        "- [UI and panes](systems/ui.md)",
        "- [UI layout files](systems/ui-layouts.md)",
        "- [Asset loading and lifetime](systems/asset-loading.md)",
        "- [Movement and swimming](systems/movement-and-swimming.md)",
        "- [Player popup menu](systems/player-popup-menu.md)",
        "- [Player exchange](systems/player-exchange.md)",
        "- [Messages and history](systems/messages-and-history.md)",
        "- [Game settings](systems/game-settings.md)",
        "- [Character creation](systems/character-creation.md)",
        "- [Changing a password](systems/change-password.md)",
        "- [Screenshots and the photo album](systems/screenshots-and-photo-album.md)",
        "- [Portraits and profiles](systems/portraits-and-profiles.md)",
        "- [NPC dialogs](systems/npc-dialogs.md)",
        "- [NPC dialog illustrations](systems/npc-dialog-illustrations.md)",
        "- [Text color markup](systems/text-color-markup.md)",
        "- [Event proxy design](systems/event-proxy.md)",
        "",
        "# Rendering",
        "",
        "- [Rendering system](rendering/README.md)",
        "- [Renderer lifecycle](rendering/lifecycle.md)",
        "- [Text and fonts](rendering/text.md)",
        "- [World rendering](rendering/world.md)",
        "- [Map lighting](rendering/lighting.md)",
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
        "- [LFT bitmap fonts](file-formats/lft.md)",
        "- [FNT fixed fonts](file-formats/fnt.md)",
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
        "- [Album.dat](file-formats/album.md)",
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
        "- [Packet body notation](network/packet-body-notation.md)",
        "- [Shared protocol types](network/protocol-types.md)",
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
        "  - [Safe launcher workflow](appendix/runtime-patches/safe-launcher-workflow.md)",
        "  - [Allow multiple clients](appendix/runtime-patches/allow-multiple-clients.md)",
        "  - [Clear stuck modifier keys on focus loss](appendix/runtime-patches/clear-stuck-modifier-keys.md)",
        "  - [Minigame support patch](appendix/runtime-patches/minigame-support.md)",
        "  - [Skip the intro](appendix/runtime-patches/skip-intro.md)",
        "  - [Ignore the local Bad Guy marker (Good Guy)](appendix/runtime-patches/ignore-local-bad-guy-marker.md)",
        "  - [Enable the positional endpoint parser](appendix/runtime-patches/enable-positional-endpoint-parser.md)",
        "  - [Disable the official endpoint fallback](appendix/runtime-patches/disable-official-endpoint-fallback.md)",
        "  - [Suppress the stipulation window](appendix/runtime-patches/suppress-stipulation-window.md)",
        "  - [Remove the fixed server-transfer delay](appendix/runtime-patches/remove-fixed-server-transfer-delay.md)",
        "  - [Hide all static map art](appendix/runtime-patches/hide-all-static-map-art.md)",
        "  - [Hold Alt to show translucent ground-item hints](appendix/runtime-patches/reveal-ground-items-through-static-map-art.md)",
        "  - [Skip the exchange count prompt for a one-item stack](appendix/runtime-patches/skip-single-item-exchange-count-prompt.md)",
        "  - [Exchange UI quality-of-life hooks](appendix/runtime-patches/exchange-ui-quality-of-life.md)",
        "  - [Photo album quality-of-life patches](appendix/runtime-patches/photo-album-quality-of-life.md)",
        "  - [Show inventory quantities in screen menus](appendix/runtime-patches/show-inventory-quantities-in-screen-menus.md)",
        "- [Runtime structures](appendix/runtime-structures.md)",
        "  - [Network packet objects](appendix/runtime/network-objects.md)",
        "  - [Session and character state](appendix/runtime/session.md)",
        "  - [Inventory and character panes](appendix/runtime/inventory-ui.md)",
        "  - [Pane and event layouts](appendix/runtime/panes.md)",
        "  - [Rendering objects](appendix/runtime/rendering.md)",
        "  - [World objects](appendix/runtime/world.md)",
        "- [Pane types and inheritance](appendix/pane-types.md)",
        "- [UI layout registry](appendix/ui-layout-registry.md)",
    ])

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build mdBook navigation and packet indexes from their page titles and metadata."""

import argparse
import re
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


def packet_index(directory: str) -> tuple[Path, str]:
    base = DOCS / "network" / directory
    path = base / "README.md"
    text = path.read_text(encoding="utf-8")
    rows = ["| Packet | Transform |", "| --- | --- |"]
    for packet in sorted(base.glob("*.md")):
        if packet.name == "README.md":
            continue
        metadata = packet.read_text(encoding="utf-8")
        modes = re.findall(r"^\| Transform \| (.+) \|$", metadata, re.MULTILINE)
        if len(modes) != 1:
            raise ValueError(f"{packet.relative_to(ROOT)} must have one Transform row")
        opcode = "0x" + packet.stem.split("-", 2)[1][2:].upper()
        rows.append(f"| [{opcode} - {title(packet)}]({packet.name}) | {modes[0]} |")
    text, count = re.subn(
        r"^\| Packet \| Transform \|\n(?:\|[^\n]*\n)+",
        "\n".join(rows) + "\n",
        text,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(f"{path.relative_to(ROOT)} must have one packet index")
    return path, text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale output without writing")
    args = parser.parse_args()
    lines = [
        "# Summary",
        "",
        "- [Inside the Dark Ages client](README.md)",
        "",
        "# The client",
        "",
        "- [Application](application/README.md)",
        "  - [Application lifecycle](application/lifecycle.md)",
        "  - [Configuration](application/configuration.md)",
        "  - [Distribution markers](application/distribution-markers.md)",
        "  - [Program Files and administrator mode](application/program-files-and-administrator.md)",
        "  - [CPU affinity](application/cpu-affinity.md)",
        "  - [Crash reporting](application/crash-reporting.md)",
        "",
        "- [Game loop](application/game-loop.md)",
        "",
        "- [Game systems](systems/README.md)",
        "  - [Event system](systems/events.md)",
        "  - [UI and panes](systems/ui.md)",
        "  - [Native UI controls](systems/ui-controls.md)",
        "  - [UI layout files](systems/ui-layouts.md)",
        "  - [Asset loading and lifetime](systems/asset-loading.md)",
        "  - [Random number generation](systems/randomness.md)",
        "  - [Map loading and cache](systems/map-loading.md)",
        "  - [Movement and swimming](systems/movement-and-swimming.md)",
        "  - [World interactions](systems/world-interactions.md)",
        "  - [Pathfinding and following](systems/pathfinding-and-pursuit.md)",
        "  - [Inventory drag actions](systems/inventory-drag-actions.md)",
        "  - [Skill and spell action delays](systems/action-delays.md)",
        "  - [Fishing minigame](systems/fishing.md)",
        "  - [Player popup menu](systems/player-popup-menu.md)",
        "  - [Player exchange](systems/player-exchange.md)",
        "  - [Bulletin boards and mail](systems/bulletin-and-mail.md)",
        "  - [Manufacturing manuals](systems/manufacturing.md)",
        "  - [NPC dialogs](systems/npc-dialogs.md)",
        "  - [Server message dialogs](systems/message-dialogs.md)",
        "  - [NPC dialog illustrations](systems/npc-dialog-illustrations.md)",
        "  - [Character creation](systems/character-creation.md)",
        "  - [Changing a password](systems/change-password.md)",
        "  - [Game settings](systems/game-settings.md)",
        "  - [Item and ability descriptions](systems/item-and-ability-descriptions.md)",
        "  - [Messages and history](systems/messages-and-history.md)",
        "  - [Korean text input](systems/korean-text-input.md)",
        "  - [Text color markup](systems/text-color-markup.md)",
        "  - [Screenshots and the photo album](systems/screenshots-and-photo-album.md)",
        "  - [Portraits and profiles](systems/portraits-and-profiles.md)",
        "  - [Local command dispatcher](systems/local-command-dispatcher.md)",
        "  - [Event proxy design](systems/event-proxy.md)",
        "",
        "- [Rendering](rendering/README.md)",
        "  - [Renderer lifecycle](rendering/lifecycle.md)",
        "  - [Text and fonts](rendering/text.md)",
        "  - [World rendering](rendering/world.md)",
        "  - [Tab wireframe map](rendering/tab-map.md)",
        "  - [Town map overlay](rendering/town-map.md)",
        "  - [Player rendering](rendering/players.md)",
        "  - [UI composition and compact layout](rendering/ui-composition.md)",
        "  - [Map lighting](rendering/lighting.md)",
        "  - [Snow and weather](rendering/weather.md)",
        "  - [Walls and occlusion](rendering/walls-and-occlusion.md)",
        "  - [Blending](rendering/blending.md)",
        "",
        "- [Audio](audio/README.md)",
        "  - [Audio lifecycle](audio/lifecycle.md)",
        "  - [Music](audio/music.md)",
        "  - [Sound effects](audio/sound-effects.md)",
        "  - [MIDI support](audio/midi.md)",
        "",
        "- [File formats](file-formats/README.md)",
        "  - [DAT archives](file-formats/dat-archives.md)",
        "  - [LFT bitmap fonts](file-formats/lft.md)",
        "  - [FNT fixed fonts](file-formats/fnt.md)",
        "  - [HPF static images](file-formats/hpf.md)",
        "  - [HEA light masks](file-formats/hea.md)",
        "  - [PAL color palettes](file-formats/pal.md)",
        "  - [TBL lookup files](file-formats/table-files.md)",
        "  - [Compression and checks](file-formats/compression.md)",
        "  - [Metadata files](file-formats/metadata.md)",
        "  - [Exporting images](file-formats/image-export.md)",
        "  - [MAP files](file-formats/map.md)",
        "  - [Raw map tile banks](file-formats/map-tile-banks.md)",
        "  - [Tile animation tables](file-formats/tile-animation-tables.md)",
        "  - [SOTP static tile flags](file-formats/sotp.md)",
        "  - [Album.dat](file-formats/album.md)",
        "  - [EPF images](file-formats/epf.md)",
        "  - [SPF images](file-formats/spf.md)",
        "  - [EFA effects](file-formats/efa.md)",
        "  - [Effect.tbl](file-formats/effect-table.md)",
        "  - [Motion effect table](file-formats/motion-effect-table.md)",
        "  - [Bulletin abuse warning list](file-formats/bulletin-bang-list.md)",
        "",
        "- [Network](network/README.md)",
        "  - [Initial connection](network/connection.md)",
        "  - [Network transport](network/transport.md)",
        "  - [Packet body notation](network/packet-body-notation.md)",
        "  - [Shared protocol types](network/protocol-types.md)",
        "  - [Packet transforms](network/packet-transforms.md)",
        "  - [Checksums](network/checksums.md)",
        "  - [Server list and greeting](network/server-tables.md)",
        "  - [Packet interaction flows](network/interaction-flows.md)",
        "  - [Client packets](network/client/README.md)",
    ]
    lines.extend(packet_lines("client", "    "))
    lines.append("  - [Server packets](network/server/README.md)")
    lines.extend(packet_lines("server", "    "))
    lines.extend([
        "",
        "# Lookup material",
        "",
        "- [Appendices](appendix/README.md)",
        "  - [Function reference](appendix/functions.md)",
        "  - [Player rendering evidence](appendix/player-rendering.md)",
        "  - [Executable-page integrity records](appendix/executable-page-integrity.md)",
        "  - [Runtime patches](appendix/runtime-patches.md)",
        "    - [Safe launcher](appendix/runtime-patches/safe-launcher.md)",
        "    - [Multiple clients](appendix/runtime-patches/multiple-clients.md)",
        "    - [Stuck modifiers](appendix/runtime-patches/stuck-modifiers.md)",
        "    - [Stale pursuit](appendix/runtime-patches/stale-pursuit.md)",
        "    - [Translucent walk refresh](appendix/runtime-patches/translucent-walk-refresh.md)",
        "    - [Bulletin pagination](appendix/runtime-patches/bulletin-pagination.md)",
        "    - [Walk-route collision](appendix/runtime-patches/walk-route-collision.md)",
        "    - [Auto-follow pathfinding](appendix/runtime-patches/auto-follow-pathfinding.md)",
        "    - [Appearance editor](appendix/runtime-patches/appearance-editor.md)",
        "    - [Minigame assets](appendix/runtime-patches/minigame-assets.md)",
        "    - [Skip intro](appendix/runtime-patches/skip-intro.md)",
        "    - [Ignore Bad Guy marker](appendix/runtime-patches/ignore-bad-guy-marker.md)",
        "    - [Command-line endpoint](appendix/runtime-patches/command-line-endpoint.md)",
        "    - [Disable endpoint fallback](appendix/runtime-patches/disable-endpoint-fallback.md)",
        "    - [Bootstrap sequence race](appendix/runtime-patches/bootstrap-sequence-race.md)",
        "    - [Hide stipulation](appendix/runtime-patches/hide-stipulation.md)",
        "    - [Early Continue](appendix/runtime-patches/early-continue.md)",
        "    - [Fast server transfer](appendix/runtime-patches/fast-server-transfer.md)",
        "    - [Hide walls](appendix/runtime-patches/hide-walls.md)",
        "    - [Ground item hints](appendix/runtime-patches/ground-item-hints.md)",
        "    - [Extended friend highlights](appendix/runtime-patches/extended-friend-highlights.md)",
        "    - [No blind](appendix/runtime-patches/no-blind.md)",
        "    - [No darkness](appendix/runtime-patches/no-darkness.md)",
        "    - [Weather packet](appendix/runtime-patches/weather-packet.md)",
        "    - [Allow map](appendix/runtime-patches/allow-map.md)",
        "    - [Map zoom](appendix/runtime-patches/map-zoom.md)",
        "    - [One-item exchange](appendix/runtime-patches/one-item-exchange.md)",
        "    - [Exchange UI](appendix/runtime-patches/exchange-ui.md)",
        "    - [Photo album](appendix/runtime-patches/photo-album.md)",
        "    - [Menu item quantities](appendix/runtime-patches/menu-item-quantities.md)",
        "  - [Runtime structures](appendix/runtime-structures.md)",
        "    - [Runtime state walking](appendix/runtime/state-walking.md)",
        "    - [Manual native actions](appendix/runtime/manual-actions.md)",
        "    - [Network packet objects](appendix/runtime/network-objects.md)",
        "    - [Session and character state](appendix/runtime/session.md)",
        "    - [Inventory and character panes](appendix/runtime/inventory-ui.md)",
        "    - [Pane and event layouts](appendix/runtime/panes.md)",
        "    - [Rendering objects](appendix/runtime/rendering.md)",
        "    - [World objects](appendix/runtime/world.md)",
        "  - [Pane types and inheritance](appendix/pane-types.md)",
        "  - [UI layout registry](appendix/ui-layout-registry.md)",
        "",
        "# Research workflow",
        "",
        "- [Getting started](getting-started.md)",
        "- [How we study the client](methodology.md)",
    ])

    summary = "\n".join(lines) + "\n"
    linked = re.findall(r"\]\(([^)#]+\.md)\)", summary)
    pages = {path.relative_to(DOCS).as_posix() for path in DOCS.rglob("*.md")}
    pages.remove("SUMMARY.md")
    if set(linked) != pages or len(linked) != len(set(linked)):
        raise ValueError(
            f"Navigation mismatch: unlisted={sorted(pages - set(linked))}, "
            f"missing={sorted(set(linked) - pages)}, duplicates={len(linked) - len(set(linked))}"
        )

    outputs = [(OUTPUT, summary), packet_index("client"), packet_index("server")]
    stale = [path for path, text in outputs if path.read_text(encoding="utf-8") != text]
    if args.check:
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(ROOT)}")
            raise SystemExit(1)
        print("Navigation and packet indexes are current; every book page is listed once.")
        return
    for path, text in outputs:
        if path in stale:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

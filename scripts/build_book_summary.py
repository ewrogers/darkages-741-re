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
        lines.append(f"{indent}- [{title(path)}]({relative})")
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
        "# Network",
        "",
        "- [Network system](network/README.md)",
        "- [Initial connection](network/connection.md)",
        "- [Network transport](network/transport.md)",
        "- [Packet transforms](network/packet-transforms.md)",
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

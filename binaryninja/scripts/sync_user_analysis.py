"""Import or export the focused user analysis manifest in Binary Ninja.

Run this file from Binary Ninja's Python console so the current BinaryView is
available as ``bv``. The optional binary_path check verifies the private input
before any user analysis is changed.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

import yaml


class _IndentedSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow, False)


def _address(value: str) -> int:
    return int(value, 0)


def _sort_records(manifest: dict[str, Any]) -> None:
    for key in ("functions", "data_symbols", "comments"):
        manifest[key].sort(key=lambda record: _address(record["address"]))
    manifest["runtime_patches"].sort(key=lambda record: _address(record["rva"]))
    for direction in manifest.get("packet_indexes", {}).values():
        direction.get("packets", []).sort(
            key=lambda record: _address(record["opcode"])
        )


def _packet_record_count(manifest: dict[str, Any]) -> int:
    return sum(
        len(direction.get("packets", []))
        for direction in manifest.get("packet_indexes", {}).values()
    )


def load_manifest(path: str | os.PathLike[str]) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as stream:
        manifest = yaml.safe_load(stream)

    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported analysis manifest schema")

    required = {"target", "functions", "data_symbols", "comments", "runtime_patches"}
    missing = required.difference(manifest)
    if missing:
        raise ValueError(f"manifest is missing: {', '.join(sorted(missing))}")

    _sort_records(manifest)
    return manifest


def verify_binary(
    binary_path: str | os.PathLike[str], target: dict[str, Any]
) -> None:
    path = Path(binary_path)
    digest = hashlib.sha256()
    size = 0

    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            size += len(block)
            digest.update(block)

    if size != target["size"]:
        raise ValueError(f"target size mismatch: expected {target['size']}, got {size}")
    if digest.hexdigest().lower() != target["sha256"].lower():
        raise ValueError("target SHA-256 mismatch")


def _containing_function(bv: Any, address: int) -> Any:
    functions = bv.get_functions_containing(address)
    if not functions:
        raise ValueError(f"no function contains 0x{address:08X}")
    return functions[0]


def import_manifest(
    bv: Any,
    manifest_path: str | os.PathLike[str],
    binary_path: str | os.PathLike[str] | None = None,
) -> dict[str, int]:
    """Apply names and comments to the current BinaryView as user analysis."""

    from binaryninja import Symbol, SymbolType

    manifest = load_manifest(manifest_path)
    if binary_path is not None:
        verify_binary(binary_path, manifest["target"])

    for record in manifest["functions"]:
        address = _address(record["address"])
        if bv.get_function_at(address) is None:
            raise ValueError(f"function is missing at 0x{address:08X}")
        symbol = Symbol(SymbolType.FunctionSymbol, address, record["name"])
        bv.define_user_symbol(symbol)

    for record in manifest["data_symbols"]:
        address = _address(record["address"])
        symbol = Symbol(SymbolType.DataSymbol, address, record["name"])
        bv.define_user_symbol(symbol)

    for record in manifest["comments"]:
        address = _address(record["address"])
        _containing_function(bv, address).set_comment_at(address, record["text"])

    bv.update_analysis_and_wait()
    return {
        "functions": len(manifest["functions"]),
        "data_symbols": len(manifest["data_symbols"]),
        "comments": len(manifest["comments"]),
        "packet_records": _packet_record_count(manifest),
    }


def export_manifest(
    bv: Any,
    manifest_path: str | os.PathLike[str],
    binary_path: str | os.PathLike[str] | None = None,
) -> dict[str, int]:
    """Refresh tracked names and comments without exporting analysis noise."""

    path = Path(manifest_path)
    manifest = load_manifest(path)
    if binary_path is not None:
        verify_binary(binary_path, manifest["target"])

    for record in manifest["functions"]:
        address = _address(record["address"])
        function = bv.get_function_at(address)
        if function is None:
            raise ValueError(f"function is missing at 0x{address:08X}")
        record["name"] = function.name

    for record in manifest["data_symbols"]:
        address = _address(record["address"])
        symbol = bv.get_symbol_at(address)
        if symbol is None:
            raise ValueError(f"data symbol is missing at 0x{address:08X}")
        record["name"] = symbol.name

    for record in manifest["comments"]:
        address = _address(record["address"])
        record["text"] = _containing_function(bv, address).get_comment_at(address)

    _sort_records(manifest)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        yaml.dump(
            manifest,
            stream,
            Dumper=_IndentedSafeDumper,
            allow_unicode=False,
            default_flow_style=False,
            sort_keys=False,
            width=1000,
        )
    os.replace(temporary, path)

    return {
        "functions": len(manifest["functions"]),
        "data_symbols": len(manifest["data_symbols"]),
        "comments": len(manifest["comments"]),
        "packet_records": _packet_record_count(manifest),
    }

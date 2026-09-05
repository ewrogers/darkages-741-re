#!/usr/bin/env python3
"""Check BN-verified player tables and private asset metadata without extracting art."""

import argparse
import hashlib
from pathlib import Path
import struct


SHA256 = "054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def executable_reader(path):
    data = path.read_bytes()
    require(len(data) == 3112960, "executable size mismatch")
    require(hashlib.sha256(data).hexdigest() == SHA256, "executable hash mismatch")
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    count = struct.unpack_from("<H", data, pe + 6)[0]
    optional_size = struct.unpack_from("<H", data, pe + 20)[0]
    image_base = struct.unpack_from("<I", data, pe + 24 + 28)[0]
    sections = [
        struct.unpack_from("<IIII", data, pe + 24 + optional_size + i * 40 + 8)
        for i in range(count)
    ]

    def read(address, size):
        rva = address - image_base
        for _, start, raw_size, offset in sections:
            if start <= rva and rva + size <= start + raw_size:
                return data[offset + rva - start:offset + rva - start + size]
        raise ValueError(f"address is not file-backed: {address:#x}")

    return read


def check_tables(read):
    back = [0, 10, 12, 14, 1, 20, 2, 3, 5, 18, 6, 17, 8, 7, 19, 4, 16, 15, 9, 11, 13]
    front = [17, 10, 12, 14, 1, 20, 2, 3, 4, 5, 18, 6, 8, 7, 19, 16, 15, 0, 9, 11, 13]
    head = [17, 10, 12, 14, 8, 1, 20, 2, 3, 4, 5, 18, 6, 7, 19, 16, 15, 0, 9, 11, 13]
    require(read(0x68C380, 84) == bytes(back + front + front + back), "default order")
    require(read(0x68C3D8, 84) == read(0x68C380, 84), "alternate order")
    require(read(0x68C430, 84) == bytes(back + head + head + back), "body-5 order")
    require(read(0x68C284, 21) == b"SBNLHUDAWCGCGCGPEFUAO", "normal letters")
    require(read(0x68C29C, 21) == b"SBNLHIDJWCGCGCGPEFIJO", "extended letters")
    anchors = list(struct.iter_unpack("<ii", read(0x68C488, 21 * 8)))
    require(anchors == [(70, 55 if 8 <= i <= 15 else 28) for i in range(21)], "anchors")
    rows = [
        (0x6D3D00, [6, 8, 6, 8], [2, 4, 4, 4, 2, 4, 4, 4]),
        (0x6D3E48, [3, 4, 3, 4], [1, 2, 2, 2, 1, 2, 2, 2]),
        (0x6D3F90, [1, 2, 3, 4], [1, 1, 2, 2, 3, 3, 4, 4]),
        (0x6D40D8, [100] * 4, [50] * 8),
        (0x6D4220, [114] * 4, [57] * 8),
    ]
    for base, coarse, smooth in rows:
        for count, expected in ((4, coarse), (8, smooth)):
            values = struct.unpack(f"<{count}i", read(base + count * 36 + 4, count * 4))
            require(list(values) == expected, f"walk table {base:#x}, row {count}")
    require(struct.unpack("<4i", read(0x6D4388, 16)) == (1, 1, -1, -1), "X signs")
    require(struct.unpack("<4i", read(0x6D4398, 16)) == (-1, 1, 1, -1), "Y signs")
    # Instruction sites checked in Binary Ninja, not inferred from asset dimensions.
    for address, expected in [
        (0x48B8C3, "0f bf 44 0a 04"),  # signed EPF bottom
        (0x48B8D8, "0f bf 44 0a 06"),  # signed EPF right
        (0x48B8ED, "0f bf 04 0a"),     # signed EPF top
        (0x48B901, "0f bf 44 0a 02"),  # signed EPF left
        (0x5FEDC8, "f7 d8"),           # mirrored right becomes negative left
        (0x5FEDD0, "f7 d9"),           # mirrored left becomes negative right
    ]:
        encoded = bytes.fromhex(expected)
        require(read(address, len(encoded)) == encoded, f"instruction {address:#x}")
    print("PASS fingerprint, part letters/orders/anchors, walk rows/signs, signed bounds and mirror instructions")


def archive_index(path):
    with path.open("rb") as stream:
        count = struct.unpack("<I", stream.read(4))[0]
        require(1 < count < 100000, f"invalid archive count: {path.name}")
        raw = stream.read(count * 17)
    require(len(raw) == count * 17, f"short archive index: {path.name}")
    entries = [
        (struct.unpack_from("<I", raw, i * 17)[0],
         raw[i * 17 + 4:i * 17 + 17].split(b"\0")[0].decode("ascii").lower())
        for i in range(count)
    ]
    require(entries[-1][1] == "", f"missing sentinel: {path.name}")
    size = path.stat().st_size
    require(all(count * 17 + 4 <= a[0] <= b[0] <= size
                for a, b in zip(entries, entries[1:])), f"invalid offsets: {path.name}")
    return {name: (start, entries[i + 1][0] - start)
            for i, (start, name) in enumerate(entries[:-1])}


def read_entry(path, index, name):
    require(name in index, f"missing {name} in {path.name}")
    start, size = index[name]
    with path.open("rb") as stream:
        stream.seek(start)
        return stream.read(size)


def check_assets(root):
    indexes = {}
    companions = []
    idle_counts = []
    for prefix in ("m", "w"):
        for group in ("ad", "eh", "im", "ns", "tz"):
            path = root / f"khan{prefix}{group}.dat"
            index = archive_index(path)
            indexes[path.name] = index
            for name in sorted(index):
                if name.startswith(("m", "w")) and name.endswith(".tbl"):
                    companions.append((path.name, name))
                if name.startswith(("m", "w")) and name.endswith("04.epf"):
                    data = read_entry(path, index, name)
                    idle_counts.append(struct.unpack_from("<H", data)[0])
    samples = [
        ("khanmim.dat", "mm00101.epf", (25, 19, 76, 40), (28, 70)),
        ("khanwim.dat", "wm00101.epf", None, (28, 70)),
        ("khanmtz.dat", "mu00101.epf", None, (28, 70)),
        ("khanmtz.dat", "mw00101.epf", (41, 67, 53, 78), (55, 70)),
        ("khanmns.dat", "ms00101.epf", None, (28, 70)),
        ("khanmad.dat", "mc00101.epf", (0, -111, 0, -111), (55, 70)),
    ]
    for archive, name, expected_bounds, anchor in samples:
        data = read_entry(root / archive, indexes[archive], name)
        frames, width, height, _, displacement = struct.unpack_from("<4HI", data)
        require(frames == 10, f"walk frame count changed: {name}")
        table = 12 + displacement
        require(table + frames * 16 <= len(data), f"short EPF table: {name}")
        top, left, bottom, right, primary, _ = struct.unpack_from("<4h2I", data, table + 16)
        require(12 + primary + (right - left) * (bottom - top) <= table,
                f"primary crop exceeds pixel blob: {name}")
        if expected_bounds is not None:
            require((top, left, bottom, right) == expected_bounds, f"sample bounds changed: {name}")
        print(f"PASS {archive}/{name}: {frames} frames, header {width}x{height}, "
              f"frame 1 crop {right-left}x{bottom-top} at ({left-anchor[0]}, {top-anchor[1]})")
    print(f"Asset scan: {len(companions)} character position companions; "
          f"{len(idle_counts)} standing resources, {sum(n % 2 for n in idle_counts)} odd frame counts")
    if companions:
        print("Installation differs from the documented no-companion scan; inspect the position records.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-root", type=Path, required=True)
    args = parser.parse_args()
    check_tables(executable_reader(args.client_root / "Darkages.exe"))
    check_assets(args.client_root)


if __name__ == "__main__":
    main()

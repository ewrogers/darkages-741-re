#!/usr/bin/env python3
"""Verify crash-patch specifications without writing client or process bytes.

Default: fingerprint, original bytes, relocation and book-listing checks.
--emulate additionally executes original/patched instructions in Unicorn's
isolated x86 memory. It never attaches to a client or contacts a server.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[2]
TARGET_SHA256 = "054a5d6adc56099c6bfd9d2a58675aff62dc788b63209a3d906492f5b89e96c6"
PREFERRED_BASE = 0x400000
STUB_TEMPLATE = bytes.fromhex("""
8B 85 BC FE FF FF 9C 85 C0 74 06 9D E9 00 00 00
00 9D E9 00 00 00 00 90 90 90 90 90 90 90 90 90
0F BF 88 FC 04 00 00 9C 83 F9 09 76 02 31 C9 9D
E9 00 00 00 00 90 90 90 90 90 90 90 90 90 90 90
0F BF 91 FE 04 00 00 9C 83 FA 09 76 02 31 D2 9D
E9 00 00 00 00 90 90 90 90 90 90 90 90 90 90 90
E8 00 00 00 00 9C 60 FF B5 D0 FE FF FF E8 00 00
00 00 61 9D E9 00 00 00 00 90 90 90 90 90 90 90
9C 60 8B 45 0C 85 C0 74 1F 8B 48 10 2B 48 08 7E
17 8B 48 14 2B 48 0C 7E 0F 61 9D 8D 4D 84 E8 00
00 00 00 E9 00 00 00 00 61 9D 31 C0 E9 00 00 00
00 90 90 90 90 90 90 90 90 90 90 90 90 90 90 90
8B 4D D0 85 C9 0F 84 B4 00 00 00 84 F6 75 08 66
8B 16 83 C6 02 EB F4 80 EE 01 0F B6 FA 0F 6E D7
0F B7 38 0F 6E C7 0F B7 3B 0F 6E CF 0F 6F 1D 00
00 00 00 0F F9 DA 0F 6F 25 00 00 00 00 0F 6F EC
0F 6F F4 0F DB E0 0F 71 D4 05 0F DB E9 0F 71 D5
05 0F D5 E2 0F D5 EB 0F FD E5 0F DB E6 0F 6F FC
0F 6F 25 00 00 00 00 0F 6F EC 0F 6F F4 0F DB E0
0F DB E9 0F D5 E2 0F D5 EB 0F FD E5 0F 71 D4 05
0F DB E6 0F EB FC 0F 6F 25 00 00 00 00 0F 6F EC
0F 6F F4 0F DB E0 0F DB E9 0F D5 E2 0F D5 EB 0F
FD E5 0F 71 D4 05 0F DB E6 0F EB FC 0F 7E FF 66
89 3B 83 C0 02 83 C3 02 49 0F 85 4C FF FF FF E9
00 00 00 00
""")


@dataclass(frozen=True)
class Patch:
    id: str
    rva: int
    original: str
    entry: int | None = None
    fixed: str | None = None

    @property
    def replacement_template(self):
        if self.fixed:
            return self.fixed
        return "E9 <rel32>" + " 90" * (len(bytes.fromhex(self.original)) - 5)


PATCHES = (
    Patch("field-map-palette", 0x76FCF, "E8 9C B4 FF FF", fixed="E8 4C B7 FF FF"),
    Patch("ground-item-null", 0x1F32EB, "8B 85 BC FE FF FF", entry=0x000),
    Patch("status-attack", 0x175AF2, "0F BF 88 FC 04 00 00", entry=0x020),
    Patch("status-defense", 0x175B1C, "0F BF 91 FE 04 00 00", entry=0x040),
    Patch("balloon-palette", 0x74434, "E8 17 42 0D 00", entry=0x060),
    Patch("empty-pixmap", 0x538AD, "8D 4D 84 E8 0B D4 02 00", entry=0x080),
    Patch("alpha-tail", 0x11C67, "F6 C6 FC 74 1F", entry=0x0C0),
)

# Operand offset within the shared allocation, operand kind, target image RVA.
RELOCATIONS = (
    (0x00D, "rel32", 0x1F32F1),
    (0x013, "rel32", 0x1F32FE),
    (0x031, "rel32", 0x175AF9),
    (0x051, "rel32", 0x175B23),
    (0x061, "rel32", 0x148650),
    (0x06E, "rel32", 0x72760),
    (0x075, "rel32", 0x74439),
    (0x09F, "rel32", 0x80CC0),
    (0x0A4, "rel32", 0x538B5),
    (0x0AD, "rel32", 0x53A5E),
    (0x0EF, "abs32", 0x2C4264),
    (0x0F9, "abs32", 0x2D90D8),
    (0x123, "abs32", 0x2D90D0),
    (0x149, "abs32", 0x2D90C8),
    (0x180, "rel32", 0x11DA4),
)


def u32(data, offset=0):
    return struct.unpack_from("<I", data, offset)[0]


def rel32(target, next_instruction):
    displacement = target - next_instruction
    if not -(1 << 31) <= displacement < (1 << 31):
        raise ValueError("allocation is outside signed rel32 range")
    return struct.pack("<i", displacement)


def build_plan(module_base, stub_base):
    """Return byte strings for review/emulation; never install them."""
    if not (0 <= module_base <= 0xFFFFFFFF - 0x5057A8):
        raise ValueError("module does not fit the x86 address space")
    if not (0 <= stub_base <= 0xFFFFFFFF - len(STUB_TEMPLATE)):
        raise ValueError("stub does not fit the x86 address space")
    stub = bytearray(STUB_TEMPLATE)
    for offset, kind, rva in RELOCATIONS:
        assert stub[offset:offset + 4] == b"\0" * 4
        target = module_base + rva
        stub[offset:offset + 4] = (
            rel32(target, stub_base + offset + 4)
            if kind == "rel32" else struct.pack("<I", target)
        )
    replacements = {}
    for patch in PATCHES:
        original = bytes.fromhex(patch.original)
        replacement = (
            bytes.fromhex(patch.fixed) if patch.fixed
            else b"\xe9" + rel32(stub_base + patch.entry, module_base + patch.rva + 5)
            + b"\x90" * (len(original) - 5)
        )
        assert len(replacement) == len(original)
        replacements[patch.rva] = replacement
    return bytes(stub), replacements


class Image:
    def __init__(self, path):
        self.data = path.read_bytes()
        if len(self.data) != 3112960 or hashlib.sha256(self.data).hexdigest() != TARGET_SHA256:
            raise ValueError("the private executable does not match the 7.41 fingerprint")
        pe = u32(self.data, 0x3C)
        assert self.data[pe:pe + 4] == b"PE\0\0"
        assert struct.unpack_from("<H", self.data, pe + 4)[0] == 0x14C
        count = struct.unpack_from("<H", self.data, pe + 6)[0]
        opt = struct.unpack_from("<H", self.data, pe + 20)[0]
        assert struct.unpack_from("<H", self.data, pe + 24)[0] == 0x10B
        assert u32(self.data, pe + 52) == PREFERRED_BASE
        self.size = u32(self.data, pe + 80)
        self.sections = [
            struct.unpack_from("<8sIIII", self.data, pe + 24 + opt + i * 40)
            for i in range(count)
        ]

    def offset(self, rva):
        for _, _, start, size, offset in self.sections:
            if start <= rva < start + size:
                return offset + rva - start
        raise ValueError(f"RVA {rva:#x} has no raw file bytes")

    def read(self, rva, size):
        offset = self.offset(rva)
        return self.data[offset:offset + size]


def verify_spec(image):
    for patch in PATCHES:
        original = bytes.fromhex(patch.original)
        assert image.read(patch.rva, len(original)) == original, patch.id
    for module, allocation in [(0x400000, 0x1000000), (0x12000000, 0x30000000)]:
        stub, replacements = build_plan(module, allocation)
        for offset, kind, rva in RELOCATIONS:
            target = (allocation + offset + 4 + struct.unpack_from("<i", stub, offset)[0]
                      if kind == "rel32" else u32(stub, offset))
            assert target == module + rva
        for patch in PATCHES:
            code = replacements[patch.rva]
            if patch.entry is not None:
                assert module + patch.rva + 5 + struct.unpack_from("<i", code, 1)[0] == allocation + patch.entry
    page = ROOT / "docs/appendix/runtime-patches/client-crash-fixes.md"
    text = page.read_text()
    listing = bytearray()
    for match in re.finditer(r"^([0-9A-F]{3}): ([0-9A-F ]+?)\s+\|", text, re.MULTILINE):
        assert int(match[1], 16) == len(listing), "book stub listing is discontinuous"
        listing.extend(bytes.fromhex(match[2]))
    assert listing == STUB_TEMPLATE, "book stub bytes differ from the verifier"
    for patch in PATCHES:
        row = next(line for line in text.splitlines() if line.startswith(f"| `{patch.id}` |"))
        assert f"0x{patch.rva:08X}" in row and patch.original in row
        assert patch.replacement_template in row
    for offset, kind, rva in RELOCATIONS:
        assert f"| `0x{offset:03X}` | `{kind}` | `0x{rva:08X}` |" in text
    # Check the focused manifest's simple scalar patch records without adding a
    # YAML dependency to this read-only verifier. This is not a general parser.
    manifest = (ROOT / "analysis/exports/client-crash-faults.yaml").read_text()
    records = {}
    for block in manifest.split("\nruntime_patches:", 1)[1].split("\n  - id: ")[1:]:
        lines = block.splitlines()
        records[lines[0].strip("'\"")] = {
            line.strip().split(": ", 1)[0]: line.strip().split(": ", 1)[1].strip("'\"")
            for line in lines[1:] if ": " in line
        }
    for patch in PATCHES:
        rec = records[patch.id]
        assert int(rec["rva"], 0) == patch.rva
        assert int(rec["static_address"], 0) == PREFERRED_BASE + patch.rva
        assert int(rec["file_offset_for_reference_only"], 0) == image.offset(patch.rva)
        assert rec["original_bytes"] == patch.original
        if patch.fixed:
            assert rec["replacement_bytes"] == patch.fixed
        else:
            assert rec["replacement_template"] == (
                f"E9 <rel32 to shared stub + 0x{patch.entry:03X}>"
                + " 90" * (len(bytes.fromhex(patch.original)) - 5)
            )
    print(f"Verified fingerprint, {len(PATCHES)} hook sites, {len(RELOCATIONS)} relocations, book bytes, and manifest.")


def emulate(image):
    """Exercise the documented bytes, native continuations, and buffer bounds."""
    try:
        import unicorn as uc
        from unicorn import x86_const as x
    except ImportError as error:
        raise SystemExit("--emulate requires unicorn: python -m pip install unicorn==2.1.4") from error

    class Machine:
        base = 0x400000
        stub = 0x1000000
        frame = 0x2008000
        stack = 0x2007000
        arena = 0x3000000
        stop = 0x1000F00

        def __init__(self, patched=True):
            self.cpu = uc.Uc(uc.UC_ARCH_X86, uc.UC_MODE_32)
            self.cpu.mem_map(self.base, (image.size + 4095) & ~4095)
            for _, _, rva, size, offset in image.sections:
                if size:
                    self.cpu.mem_write(self.base + rva, image.data[offset:offset + size])
            self.cpu.mem_map(self.stub, 4096)
            self.cpu.mem_write(self.stop, b"\xf4")  # bounded translation at the return sentinel
            self.cpu.mem_map(0x2000000, 0x10000)
            self.cpu.mem_map(self.arena, 0x10000)
            code, sites = build_plan(self.base, self.stub)
            self.cpu.mem_write(self.stub, code)
            if patched:
                for rva, replacement in sites.items():
                    self.cpu.mem_write(self.base + rva, replacement)
            self.set(x.UC_X86_REG_EBP, self.frame)
            self.set(x.UC_X86_REG_ESP, self.stack)
            self.set(x.UC_X86_REG_EFLAGS, 0x246)

        def get(self, reg):
            return self.cpu.reg_read(reg)

        def set(self, reg, value):
            self.cpu.reg_write(reg, value & 0xFFFFFFFF)

        def word(self, address, value):
            self.cpu.mem_write(address, struct.pack("<H", value & 0xFFFF))

        def dword(self, address, value):
            self.cpu.mem_write(address, struct.pack("<I", value & 0xFFFFFFFF))

        def read32(self, address):
            return u32(self.cpu.mem_read(address, 4))

        def ret(self, arguments=0):
            esp = self.get(x.UC_X86_REG_ESP)
            self.set(x.UC_X86_REG_EIP, self.read32(esp))
            self.set(x.UC_X86_REG_ESP, esp + 4 + arguments)

        def run(self, entry, stops, calls=None):
            reached = []
            calls = calls or {}

            def step(cpu, address, size, opaque):
                if address in stops:
                    reached.append(address)
                    cpu.emu_stop()
                elif address in calls:
                    calls[address](self)

            hook = self.cpu.hook_add(uc.UC_HOOK_CODE, step)
            try:
                self.cpu.emu_start(entry, 0, count=200000)
                assert reached, "emulation did not reach a documented continuation"
                return reached[0]
            finally:
                self.cpu.hook_del(hook)

    # The native contains/release helpers execute; only filesystem lookup is mocked.
    for patched in (False, True):
        m = Machine(patched)
        pool = m.arena + 0x1000

        def find_entry(machine):
            free = next((pool + i * 0x14 for i in range(20)
                         if not machine.read32(pool + i * 0x14)), 0)
            if free:
                machine.dword(free, 1)
            machine.set(x.UC_X86_REG_EAX, free)
            machine.ret(4)

        for attempt in range(40):
            m.set(x.UC_X86_REG_ESP, m.stack)
            m.dword(m.stack, m.arena)
            m.set(x.UC_X86_REG_ECX, m.arena + 0x400)
            m.run(0x476FCF, {0x476FD4}, {0x472470: find_entry})
            expected = 1 if patched else (pool + attempt * 0x14 if attempt < 20 else 0)
            assert m.get(x.UC_X86_REG_EAX) == expected
            assert m.get(x.UC_X86_REG_ESP) == m.stack + 4
        assert sum(bool(m.read32(pool + i * 0x14)) for i in range(20)) == (0 if patched else 20)
    print("PASS archive pool: original exhausts 20 slots; patched 40 probes leave zero busy.")

    for value in (0, 0x3000100):
        m = Machine()
        m.dword(m.frame - 0x144, value)
        m.dword(m.frame - 0x13C, value)
        reached = m.run(0x5F32EB, {0x5F32F1, 0x5F32FE})
        assert reached == (0x5F32F1 if value else 0x5F32FE)
        assert m.get(x.UC_X86_REG_EAX) == value
        assert m.get(x.UC_X86_REG_ESP) == m.stack
        assert m.get(x.UC_X86_REG_EFLAGS) == 0x246
        if not value:
            m.dword(m.frame - 4, 1)
            m.run(reached, {0x5F3319})
            assert m.read32(m.frame - 4) == 0xFFFFFFFF
    m = Machine(False)
    m.dword(m.frame - 0x144, 0)
    try:
        m.run(0x5F32EB, {0x5F32F3})
    except uc.UcError as error:
        assert error.errno == uc.UC_ERR_READ_UNMAPPED
        assert m.get(x.UC_X86_REG_EIP) == 0x5F32F1
    else:
        raise AssertionError("original null-item dereference unexpectedly succeeded")
    print("PASS item result: original null dereference reproduced; patched cleanup and valid path preserved.")

    for defense in (False, True):
        for value in (*range(256), 0xFFFF, 0x8000):
            m = Machine()
            m.word(m.arena + (0x4FE if defense else 0x4FC), value)
            m.set(x.UC_X86_REG_ECX if defense else x.UC_X86_REG_EAX, m.arena)
            for i in range(10):
                m.dword(m.frame - 0x28 + i * 4, m.arena + 0x1000 + i * 16)
            m.run(0x575B1C if defense else 0x575AF2, {0x575B27 if defense else 0x575AFD})
            selected = m.get(x.UC_X86_REG_EAX if defense else x.UC_X86_REG_EDX)
            assert selected == m.arena + 0x1000 + (value if value <= 9 else 0) * 16
            assert m.get(x.UC_X86_REG_EFLAGS) == 0x246
            assert m.get(x.UC_X86_REG_ESP) == m.stack
            assert bytes(m.cpu.mem_read(m.arena + (0x4FE if defense else 0x4FC), 2)) == struct.pack("<H", value)
    m = Machine(False)
    m.word(m.arena + 0x4FC, 10)
    m.set(x.UC_X86_REG_EAX, m.arena)
    m.dword(m.frame, 0xDEAD0000)
    m.run(0x575AF2, {0x575AFD})
    assert m.get(x.UC_X86_REG_EDX) == 0xDEAD0000
    print("PASS elements: both 0..255 domains plus negative s16 values; raw fields, flags, and stack preserved.")

    for patched in (False, True):
        m = Machine(patched)
        handle = m.arena + 0x500
        m.dword(handle, 1)
        m.dword(m.frame - 0x130, handle)
        m.dword(m.stack, 7)
        m.dword(m.stack + 4, m.arena + 0x1000)
        m.set(x.UC_X86_REG_ECX, m.arena + 0x2000)
        loaded = []

        def palette_load(machine):
            esp = machine.get(x.UC_X86_REG_ESP)
            assert machine.read32(esp + 4) == 7
            assert machine.read32(esp + 8) == machine.arena + 0x1000
            assert machine.get(x.UC_X86_REG_ECX) == machine.arena + 0x2000
            loaded.append(True)
            for reg, value in [(x.UC_X86_REG_EAX, 0x12345678), (x.UC_X86_REG_ECX, 0x22446688),
                               (x.UC_X86_REG_EDX, 0x55667788), (x.UC_X86_REG_EFLAGS, 0x202)]:
                machine.set(reg, value)
            machine.ret(8)

        m.run(0x474434, {0x474439}, {0x548650: palette_load})
        assert len(loaded) == 1 and m.read32(handle) == (0 if patched else 1)
        assert m.get(x.UC_X86_REG_EAX) == 0x12345678
        assert m.get(x.UC_X86_REG_ECX) == 0x22446688
        assert m.get(x.UC_X86_REG_EDX) == 0x55667788
        assert m.get(x.UC_X86_REG_EFLAGS) == 0x202
        assert m.get(x.UC_X86_REG_ESP) == m.stack + 8
    print("PASS balloon: one palette load, one native release, ret-8 stack and return registers preserved.")

    for bounds in (None, (0, 0, 0, 10), (0, 0, 10, 0), (10, 0, 9, 10), (0, 10, 10, 9), (0, 0, 10, 10)):
        m = Machine()
        m.dword(m.frame + 0xC, m.arena if bounds else 0)
        m.dword(m.frame - 4, 0xFFFFFFFF)
        if bounds:
            m.cpu.mem_write(m.arena + 8, struct.pack("<4i", *bounds))
        constructed = []

        def region_ctor(machine):
            assert machine.get(x.UC_X86_REG_ECX) == machine.frame - 0x7C
            constructed.append(True)
            machine.ret()

        reached = m.run(0x4538AD, {0x4538B5, 0x453A5E}, {0x480CC0: region_ctor})
        valid = bounds == (0, 0, 10, 10)
        assert reached == (0x4538B5 if valid else 0x453A5E)
        assert len(constructed) == int(valid)
        assert m.read32(m.frame - 4) == 0xFFFFFFFF
        assert m.get(x.UC_X86_REG_ESP) == m.stack
    print("PASS pixmap guard: null, zero, reversed and valid extents; region construction precedes no invalid draw.")

    def blend(source, dest, alpha, red, green):
        inverse = (32 - alpha) & 0xFFFF
        first = ((((source & red) >> 5) * alpha + ((dest & red) >> 5) * inverse) & 0xFFFF) & red
        def component(mask):
            return ((((source & mask) * alpha + (dest & mask) * inverse) & 0xFFFF) >> 5) & mask
        return first | component(green) | component(31)

    def draw(width, red, green, clipped=0, flip=False, patched=True):
        m = Machine(patched)
        height, stride = 2, 0x2000
        draw_width = width - clipped
        rows, sources, destinations, weights = [], [], [], []
        for row in range(height):
            source_page = 0x4000000 + row * stride
            dest_page = 0x6000000 + row * stride
            alpha_page = 0x5000000 + row * stride
            for page in (source_page, dest_page, alpha_page):
                m.cpu.mem_map(page, 4096)  # the following page stays unmapped
            source = [(i * 4253 + row * 997) & 0xFFFF for i in range(width)]
            dest = [(i * 7307 + 0x1234 + row * 8) & 0xFFFF for i in range(draw_width)]
            tokens, alphas = [], []
            remaining, run = width, 0
            while remaining:
                count = min(255, remaining)
                alpha = (row * 17 + run * 13 + width) % 33
                tokens.append(count << 8 | alpha)
                alphas.extend([alpha] * count)
                remaining -= count
                run += 1
            source_ptr = source_page + 4096 - 2 * width
            dest_ptr = dest_page + 4096 - 2 * draw_width
            alpha_ptr = alpha_page + 4096 - 2 * len(tokens)
            m.cpu.mem_write(source_ptr, struct.pack(f"<{width}H", *source))
            m.cpu.mem_write(dest_ptr, struct.pack(f"<{draw_width}H", *dest))
            m.cpu.mem_write(alpha_ptr, struct.pack(f"<{len(tokens)}H", *tokens))
            rows.append((source_ptr, dest_ptr, alpha_ptr))
            sources.append(source)
            destinations.append(dest)
            weights.append(alphas)
            m.dword(m.arena + 0x100 + row * 4, alpha_ptr)
        m.cpu.mem_write(0x6D90D8, struct.pack("<4H", *([red] * 4)))
        m.cpu.mem_write(0x6D90D0, struct.pack("<4H", *([green] * 4)))
        m.cpu.mem_write(0x6D90C8, struct.pack("<4H", *([31] * 4)))
        m.cpu.mem_write(0x6D8FD8, bytes([2 if flip else 0]))
        m.cpu.mem_write(m.arena, struct.pack("<4I", 0, clipped, height, width))
        args = [rows[0][0], m.arena, stride, rows[0][1], 0, 0, stride, m.arena + 0x100, 0, 0, 0]
        m.cpu.mem_write(m.stack, struct.pack("<12I", m.stop, *args))
        saved = [(x.UC_X86_REG_EBX, 0x12345678), (x.UC_X86_REG_ESI, 0x87654321),
                 (x.UC_X86_REG_EDI, 0x11223344), (x.UC_X86_REG_EBP, m.frame)]
        for reg, value in saved:
            m.set(reg, value)
        try:
            m.run(0x4119C0, {m.stop})
        except uc.UcError as error:
            if patched:
                raise AssertionError((width, clipped, flip, hex(red),
                                      hex(m.get(x.UC_X86_REG_EIP)),
                                      hex(m.get(x.UC_X86_REG_ESP)), str(error))) from error
            raise
        for row in range(height):
            target_row = height - row - 1 if flip else row
            expected = [blend(sources[row][i + clipped], destinations[target_row][i],
                              weights[row][i + clipped], red, green) for i in range(draw_width)]
            actual = struct.unpack(f"<{draw_width}H", m.cpu.mem_read(rows[target_row][1], 2 * draw_width))
            assert list(actual) == expected, (width, clipped, flip, hex(red), row)
        assert m.get(x.UC_X86_REG_ESP) == m.stack + 4
        for reg, value in saved:
            assert m.get(reg) == value

    cases = 0
    for red, green in [(0xF800, 0x7E0), (0x7C00, 0x3E0)]:
        for width in (1, 2, 3, 4, 5, 7, 8, 31, 32, 33, 255, 256, 639, 640, 641):
            for clipped in (0, 1) if width > 1 else (0,):
                for flip in (False, True):
                    draw(width, red, green, clipped, flip)
                    cases += 1
    for width in (1, 4, 640):
        try:
            draw(width, 0xF800, 0x7E0, patched=False)
        except uc.UcError as error:
            assert error.errno == uc.UC_ERR_READ_UNMAPPED
        else:
            raise AssertionError(f"original width-{width} tail unexpectedly respected guard pages")
    print(f"PASS MMX tail: {cases} guarded full-function cases, RGB555/565, clipping, vertical flip, scalar pixel oracle; 3 original failures reproduced.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=ROOT / "client/Darkages.exe")
    parser.add_argument("--emulate", action="store_true")
    args = parser.parse_args()
    image = Image(args.binary)
    verify_spec(image)
    if args.emulate:
        emulate(image)
    assert hashlib.sha256(args.binary.read_bytes()).hexdigest() == TARGET_SHA256
    print("All requested checks passed; executable unchanged. This verifier does not run Windows/Arbiter integration checks.")


if __name__ == "__main__":
    main()

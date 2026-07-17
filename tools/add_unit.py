#!/usr/bin/env python3
"""Add a decompiled translation unit: writes src file, splits.txt entry, and a
configure.py Object in the Runtime.PPCEABI.H lib group. Reusable for the
from-scratch grind on trivial functions.

Usage: python3 tools/add_unit.py <unit_path> <start_hex> <end_hex> <src_file>
  where src_file is a path to the C source content to install at src/<unit_path>.
"""
import sys, os

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
SPLITS = os.path.join(ROOT, "config/RSBE01_02/splits.txt")
CONFIG = os.path.join(ROOT, "configure.py")


def add(unit_path, start, end, csource):
    # 1. src file
    dst = os.path.join(ROOT, "src", unit_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w").write(csource)
    # 2. splits.txt (append)
    with open(SPLITS, "a") as f:
        f.write(f"\n{unit_path}:\n\t.text       start:0x{start:08X} end:0x{end:08X}\n")
    # 3. configure.py: add Object into Runtime.PPCEABI.H group (after last TRK/Runtime object)
    c = open(CONFIG).read()
    anchor = '            Object(Matching, "TRK_MINNOW_DOLPHIN/udp_cc.c"),\n'
    line = f'            Object(Matching, "{unit_path}"),\n'
    if line in c:
        return  # already present
    # insert after the anchor if present, else after the exceptions object
    if anchor in c:
        c = c.replace(anchor, anchor + line, 1)
    else:
        a2 = '            Object(NonMatching, "Runtime.PPCEABI.H/__init_cpp_exceptions.cpp"),\n'
        c = c.replace(a2, a2 + line, 1)
    open(CONFIG, "w").write(c)


if __name__ == "__main__":
    unit_path, start, end, src_file = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16), sys.argv[4]
    add(unit_path, start, end, open(src_file).read())
    print(f"added unit {unit_path} [0x{start:08X}-0x{end:08X}]")

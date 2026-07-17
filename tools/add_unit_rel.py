#!/usr/bin/env python3
"""Add a decompiled unit to a REL module: writes src file, the module's
splits.txt entry, and an Object in the module's lib group in configure.py."""
import sys, os, re

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
CONFIG = os.path.join(ROOT, "configure.py")


def add(module, unit_path, start, end, csource):
    # 1. src file
    dst = os.path.join(ROOT, "src", unit_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w").write(csource)
    # 2. module splits.txt (append)
    splits = os.path.join(ROOT, "config/RSBE01_02/rels", module, "splits.txt")
    with open(splits, "a") as f:
        f.write(f"\n{unit_path}:\n\t.text       start:0x{start:08X} end:0x{end:08X}\n")
    # 3. configure.py: insert Object into the module's lib group
    c = open(CONFIG).read()
    line = f'            Object(Matching, "{unit_path}"),\n'
    if line in c:
        return
    # find the module's lib group: '"lib": "<module>",' then the group's objects list closing '],'
    key = f'"lib": "{module}",'
    idx = c.find(key)
    if idx < 0:
        raise SystemExit(f"module group '{module}' not found in configure.py")
    # find the closing '],' of this group's objects (first '],' after 'objects': [ ... )
    obj_idx = c.find('"objects": [', idx)
    close_idx = c.find('\n        ],', obj_idx)
    if obj_idx < 0 or close_idx < 0:
        raise SystemExit(f"objects list for '{module}' not found")
    c = c[:close_idx] + "\n" + line.rstrip("\n") + c[close_idx:]
    open(CONFIG, "w").write(c)


if __name__ == "__main__":
    module, unit_path, start, end, src_file = sys.argv[1], sys.argv[2], int(sys.argv[3], 16), int(sys.argv[4], 16), sys.argv[5]
    add(module, unit_path, start, end, open(src_file).read())
    print(f"added REL unit [{module}] {unit_path} [0x{start:08X}-0x{end:08X}]")

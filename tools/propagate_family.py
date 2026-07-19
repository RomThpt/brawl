#!/usr/bin/env python3
"""Apply one decompiled function to every byte-identical instance of its family.

That is the whole point of the family approach: the expensive part is working out
the C once, and this makes the payoff automatic instead of manual copy-paste.

The C template must name the function @NAME@; each instance gets its own symbol.

Usage: python3 tools/propagate_family.py <ref_module> <ref_hex_addr> <size> <template.c>
"""
import struct, re, os, sys, glob

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
sys.path.insert(0, os.path.join(ROOT, "tools"))
import add_unit_rel

ref_mod, ref_addr, size, tmpl_path = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3]), sys.argv[4]
template = open(tmpl_path).read()
if "@NAME@" not in template:
    raise SystemExit("le template doit contenir @NAME@ à la place du nom de fonction")


def text_section(rel):
    so = struct.unpack('>I', rel[0x10:0x14])[0]
    num = struct.unpack('>I', rel[0xC:0x10])[0]
    for i in range(num):
        o, s = struct.unpack('>II', rel[so + i * 8:so + i * 8 + 8])
        if (o & 1) and s:
            return o & ~3
    return None


rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{ref_mod}.rel"), "rb").read()
toff = text_section(rel)
ref_bytes = rel[toff + ref_addr:toff + ref_addr + size]

added = 0
for sym in sorted(glob.glob(os.path.join(ROOT, "config/RSBE01_02/rels/*/symbols.txt"))):
    mod = sym.split('/')[-2]
    relf = os.path.join(ROOT, f"orig/RSBE01_02/files/module/{mod}.rel")
    if not os.path.exists(relf):
        continue
    r2 = open(relf, "rb").read()
    t2 = text_section(r2)
    if t2 is None:
        continue
    done = []
    for l in open(sym.replace('symbols.txt', 'splits.txt')):
        m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', l)
        if m:
            done.append((int(m.group(1), 16), int(m.group(2), 16)))
    for l in open(sym):
        m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', l)
        if not m:
            continue
        n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
        if sz != size or any(s <= a < e for s, e in done):
            continue
        if not re.match(r'^[A-Za-z_]\w*$', n):
            continue
        if r2[t2 + a:t2 + a + size] != ref_bytes:
            continue
        add_unit_rel.add(mod, f"mo_stub/{mod}/fam_{n}.c", a, a + size,
                         template.replace("@NAME@", n))
        print(f"  {mod} {n} @0x{a:X}")
        added += 1

print(f"{added} instances instanciées")

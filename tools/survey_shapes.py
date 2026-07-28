#!/usr/bin/env python3
"""Relever les formes dominantes parmi les fonctions non encore matchées.

Regroupe par (taille, suite d'opcodes primaires). Les fonctions contenant un
dispatch virtuel (bctr/bctrl) sont exclues: aucune formulation C ne les atteint.

Usage: python3 tools/survey_shapes.py [taille_max] [top_n]
"""
import struct, re, os, sys, glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAXSZ = int(sys.argv[1]) if len(sys.argv) > 1 else 80
TOPN = int(sys.argv[2]) if len(sys.argv) > 2 else 25
IDENT = re.compile(r'^[A-Za-z_]\w*$')
VIRT = (0x4E800420, 0x4E800421)          # bctr / bctrl

groups = defaultdict(list)
total_unmatched = total_bytes = 0

for relpath in sorted(glob.glob(os.path.join(ROOT, "orig/RSBE01_02/files/module/*.rel"))):
    module = os.path.basename(relpath)[:-4]
    cfg = os.path.join(ROOT, "config/RSBE01_02/rels", module)
    if not os.path.isdir(cfg):
        continue
    rel = open(relpath, "rb").read()
    sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
    nsec = struct.unpack('>I', rel[0xC:0x10])[0]
    textoff = None
    for i in range(nsec):
        o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
        if (o & 1) and s:
            textoff = o & ~3
            break
    if textoff is None:
        continue

    done = []
    sp = os.path.join(cfg, "splits.txt")
    if os.path.exists(sp):
        for line in open(sp):
            m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', line)
            if m:
                done.append((int(m.group(1), 16), int(m.group(2), 16)))

    for line in open(os.path.join(cfg, "symbols.txt")):
        m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', line)
        if not m:
            continue
        n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
        if any(s <= a < e for s, e in done):
            continue
        total_unmatched += 1
        total_bytes += sz
        if sz > MAXSZ or sz < 8 or sz % 4 or not IDENT.match(n):
            continue
        try:
            w = struct.unpack(f'>{sz // 4}I', rel[textoff + a:textoff + a + sz])
        except struct.error:
            continue
        if any(x in VIRT for x in w):
            continue
        key = (sz, tuple(x >> 26 for x in w))
        groups[key].append((module, n, a))

items = sorted(groups.items(), key=lambda kv: -len(kv[1]) * kv[0][0])
print(f"non matchées: {total_unmatched} fonctions, {total_bytes} octets")
print(f"{len(groups)} formes retenues (<= {MAXSZ} o, sans dispatch virtuel)\n")
print(f"{'n':>6} {'taille':>6} {'octets':>9} {'%code':>7}  exemple")
for (sz, ops), lst in items[:TOPN]:
    b = len(lst) * sz
    mod, name, a = lst[0]
    print(f"{len(lst):>6} {sz:>6} {b:>9} {100.0 * b / total_bytes:>6.3f}%  "
          f"{mod}/{name} @{a:08X}  ops={','.join(map(str, ops))}")

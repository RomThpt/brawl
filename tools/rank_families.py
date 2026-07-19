#!/usr/bin/env python3
"""Rank duplicate families by tractability, not just raw gain.

A 140-byte C++ destructor with 4 external calls is far harder to match than a
200-byte pure-computation routine with none. External relocations mean the C
source has to name the right callees/globals, which usually means reconstructing
a class layout first. Zero-reloc families are self-contained: read the asm,
write the C, done.

Usage: python3 tools/rank_families.py [min_size] [max_relocs] [top_n]
"""
import struct, re, os, sys, glob, hashlib
from collections import defaultdict

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
MIN_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 100
MAX_REL = int(sys.argv[2]) if len(sys.argv) > 2 else 999
TOP_N = int(sys.argv[3]) if len(sys.argv) > 3 else 25
TOTAL_CODE = 15833548


def text_section(rel):
    so = struct.unpack('>I', rel[0x10:0x14])[0]
    num = struct.unpack('>I', rel[0xC:0x10])[0]
    for i in range(num):
        o, s = struct.unpack('>II', rel[so + i * 8:so + i * 8 + 8])
        if (o & 1) and s:
            return o & ~3, i
    return None, None


def relocs(rel, tidx):
    imp_off, imp_size = struct.unpack('>II', rel[0x28:0x30])
    out = {}
    for i in range(imp_size // 8):
        mid, roff = struct.unpack('>II', rel[imp_off + i * 8:imp_off + i * 8 + 8])
        pos, cur_sec, cur = roff, -1, 0
        while pos + 8 <= len(rel):
            off, typ, sec, add = struct.unpack('>HBBI', rel[pos:pos + 8])
            pos += 8
            if typ == 203:
                break
            if typ == 202:
                cur_sec, cur = sec, 0
                continue
            cur += off
            if typ == 201:
                continue
            if cur_sec == tidx:
                out[cur] = (typ, mid, sec, add)
    return out


def normalise(code, base, rl):
    out = bytearray(code)
    for i in range(0, len(code) - 3, 4):
        w = struct.unpack('>I', code[i:i + 4])[0]
        prim = w >> 26
        if prim in (16, 18):
            w &= 0xFC000003
        elif base + i in rl:
            w &= 0xFFFF0000
        out[i:i + 4] = struct.pack('>I', w)
    return bytes(out)


def load_done(splits):
    d = []
    if os.path.exists(splits):
        for l in open(splits):
            m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', l)
            if m:
                d.append((int(m.group(1), 16), int(m.group(2), 16)))
    return d


groups = defaultdict(list)
meta = {}
for sym in sorted(glob.glob(os.path.join(ROOT, "config/RSBE01_02/rels/*/symbols.txt"))):
    mod = sym.split('/')[-2]
    relf = os.path.join(ROOT, f"orig/RSBE01_02/files/module/{mod}.rel")
    if not os.path.exists(relf):
        continue
    rel = open(relf, "rb").read()
    toff, tidx = text_section(rel)
    if toff is None:
        continue
    rl = relocs(rel, tidx)
    done = load_done(sym.replace('symbols.txt', 'splits.txt'))
    isd = lambda a: any(s <= a < e for s, e in done)
    for l in open(sym):
        m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', l)
        if not m:
            continue
        n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
        if sz < MIN_SIZE or isd(a):
            continue
        code = rel[toff + a:toff + a + sz]
        if len(code) < sz:
            continue
        inside = sorted((o - a, t, mid, sec, add) for o, (t, mid, sec, add) in rl.items()
                        if a <= o < a + sz)
        h = hashlib.sha1(normalise(code, a, rl) + repr(inside).encode()).hexdigest()
        groups[h].append((mod, n, a, sz))
        # bctrl = virtual dispatch: needs a reconstructed vtable, much harder than
        # plain arithmetic. Count it so we can rank those families down.
        nv = sum(1 for i in range(0, sz - 3, 4)
                 if struct.unpack('>I', code[i:i + 4])[0] == 0x4E800421)
        meta[h] = (len(inside), nv)

MAX_VCALL = int(os.environ.get("MAX_VCALL", "999"))
rows = []
for h, v in groups.items():
    if len(v) < 2:
        continue
    nrel, nv = meta[h]
    if nrel > MAX_REL or nv > MAX_VCALL:
        continue
    rows.append((len(v) * v[0][3], len(v), v[0][3], nrel, nv, v[0]))
rows.sort(reverse=True)

cum = sum(r[0] for r in rows)
print(f"familles : <={MAX_REL} reloc, <={MAX_VCALL} appels virtuels, taille >={MIN_SIZE}o "
      f"-> {len(rows)} familles")
print(f"gain cumulé si toutes décompilées : {cum} o ({100*cum/TOTAL_CODE:.3f}% du code)\n")
print(f"{'gain':>9} {'inst':>5} {'taille':>7} {'reloc':>6} {'vcall':>6}  module / fonction")
for tot, cnt, sz, nrel, nv, ref in rows[:TOP_N]:
    print(f"{tot:9d} {cnt:5d} {sz:7d} {nrel:6d} {nv:6d}  {ref[0]} {ref[1]} @0x{ref[2]:X}")

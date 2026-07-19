#!/usr/bin/env python3
"""Find duplicate large functions across REL modules.

Big functions hold most of the code but each needs a hand-written decompilation.
The multiplier: many are byte-identical across modules (the 34 character modules
are built from the same templates). Decompile one, match it in N places.

Normalises away everything the linker patches (relocated fields from the REL
relocation table) plus branch offsets, then groups by hash.

Usage: python3 tools/find_dupes.py [min_size] [top_n]
"""
import re, struct, os, sys, glob, hashlib
from collections import defaultdict

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
MIN_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 100
TOP_N = int(sys.argv[2]) if len(sys.argv) > 2 else 25
TOTAL_CODE = 15833548


def text_section(rel):
    """(file_offset, section_index) of the first executable section."""
    sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
    num = struct.unpack('>I', rel[0xC:0x10])[0]
    for i in range(num):
        o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
        if (o & 1) and s:
            return o & ~3, i
    return None, None


def relocated_offsets(rel, text_idx):
    """Byte offsets inside .text that the loader patches (so they differ per module)."""
    try:
        imp_off = struct.unpack('>I', rel[0x28:0x2C])[0]
        imp_size = struct.unpack('>I', rel[0x2C:0x30])[0]
    except struct.error:
        return set()
    out = set()
    for i in range(imp_size // 8):
        e = imp_off + i * 8
        if e + 8 > len(rel):
            break
        _, roff = struct.unpack('>II', rel[e:e + 8])
        pos, cur_sec, cur = roff, -1, 0
        while pos + 8 <= len(rel):
            off, typ, sec, add = struct.unpack('>HBBI', rel[pos:pos + 8])
            pos += 8
            if typ == 203:          # R_DOLPHIN_END
                break
            if typ == 202:          # R_DOLPHIN_SECTION
                cur_sec, cur = sec, 0
                continue
            cur += off
            if typ == 201:          # R_DOLPHIN_NOP (advance only)
                continue
            if cur_sec == text_idx:
                out.add(cur)
    return out


def normalise(code, base, relocs):
    """Zero out linker-patched fields and branch displacements."""
    out = bytearray(code)
    for i in range(0, len(code) - 3, 4):
        w = struct.unpack('>I', code[i:i + 4])[0]
        prim = w >> 26
        if prim in (16, 18):        # bc / b / bl -> displacement varies per module
            w &= 0xFC000003
        elif base + i in relocs:    # relocated immediate (address of a global, etc.)
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
for sym in sorted(glob.glob(os.path.join(ROOT, "config/RSBE01_02/rels/*/symbols.txt"))):
    mod = sym.split('/')[-2]
    relf = os.path.join(ROOT, f"orig/RSBE01_02/files/module/{mod}.rel")
    if not os.path.exists(relf):
        continue
    rel = open(relf, "rb").read()
    toff, tidx = text_section(rel)
    if toff is None:
        continue
    relocs = relocated_offsets(rel, tidx)
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
        h = hashlib.sha1(normalise(code, a, relocs)).hexdigest()
        groups[h].append((mod, n, a, sz))

fam = [(len(v) * v[0][3], len(v), v[0][3], v) for v in groups.values() if len(v) > 1]
fam.sort(reverse=True)

uniq = len(groups)
dup_bytes = sum(f[0] for f in fam)
dup_funcs = sum(f[1] for f in fam)
print(f"fonctions >={MIN_SIZE}o non matchées : {sum(len(v) for v in groups.values())} "
      f"({uniq} formes uniques)")
print(f"dont dupliquées : {dup_funcs} fonctions dans {len(fam)} familles")
print(f"code couvrable en décompilant 1 exemplaire par famille : "
      f"{dup_bytes} octets ({100*dup_bytes/TOTAL_CODE:.3f}% du code total)\n")
print(f"top {TOP_N} familles (gain = instances x taille) :")
for tot, cnt, sz, v in fam[:TOP_N]:
    mods = ",".join(sorted(set(x[0] for x in v))[:4])
    more = "..." if len(set(x[0] for x in v)) > 4 else ""
    print(f"  {tot:8d} o | {cnt:3d} x {sz:5d}o | {v[0][1]:<22} | {mods}{more}")

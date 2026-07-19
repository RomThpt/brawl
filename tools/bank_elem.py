#!/usr/bin/env python3
"""Auto-decompile array-element accessors: return &p->array[i].

    mulli r0, r4, M ; add r3, r3, r0 ; addi r3, r3, A ; blr   -> p + i*M + A
    slwi  r0, r4, K ; add r3, r3, r0 ; addi r3, r3, A ; blr   -> p + i*(1<<K) + A

The compiler picks slwi over mulli when the element size is a power of two, so
both encodings mean the same source. The trailing addi is optional (element at
offset zero).

Usage: python3 tools/bank_elem.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"

rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
nsec = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = None
for i in range(nsec):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff = o & ~3
        break


def w(a, i):
    return struct.unpack('>I', rel[textoff + a + i * 4:textoff + a + i * 4 + 4])[0]


def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v


def scale_of(x):
    """First instruction -> element size, or None."""
    if (x >> 26) == 7 and ((x >> 21) & 31) == 0 and ((x >> 16) & 31) == 4:   # mulli r0,r4,M
        m = sign16(x & 0xFFFF)
        return m if m > 0 else None
    if (x >> 26) == 21:                                                      # rlwinm = slwi
        rS, rA, SH, MB, ME = ((x >> 21) & 31, (x >> 16) & 31, (x >> 11) & 31,
                              (x >> 6) & 31, (x >> 1) & 31)
        if rS == 4 and rA == 0 and MB == 0 and ME == 31 - SH and SH:
            return 1 << SH
    return None


def classify(a, sz):
    if sz not in (12, 16):
        return None
    if w(a, sz // 4 - 1) != 0x4E800020:
        return None
    scale = scale_of(w(a, 0))
    if scale is None:
        return None
    if w(a, 1) != 0x7C630214:                       # add r3, r3, r0
        return None
    if sz == 12:
        return scale, 0
    x = w(a, 2)                                     # addi r3, r3, A
    if (x & 0xFFFF0000) != 0x38630000:
        return None
    return scale, sign16(x & 0xFFFF)


done = []
for line in open(os.path.join(ROOT, "config/RSBE01_02/rels", module, "splits.txt")):
    m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', line)
    if m:
        done.append((int(m.group(1), 16), int(m.group(2), 16)))
isd = lambda a: any(s <= a < e for s, e in done)

bad = set()
if os.path.exists(BADFILE):
    for m2, a2 in re.findall(r'([A-Za-z]\w*):([0-9A-Fa-f]{8})', open(BADFILE).read()):
        if m2 == module:
            bad.add(int(a2, 16))

banked, addrs = 0, []
for line in open(os.path.join(ROOT, "config/RSBE01_02/rels", module, "symbols.txt")):
    m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', line)
    if not m:
        continue
    n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
    if isd(a) or a in bad or not re.match(r'^[A-Za-z_]\w*$', n):
        continue
    if banked >= maxf:
        break
    c = classify(a, sz)
    if not c:
        continue
    scale, off = c
    tail = f" + {off}" if off else ""
    src = f"void* {n}(void* p, int i) {{\n    return (char*)p + i * {scale}{tail};\n}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/el_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} element accessors")

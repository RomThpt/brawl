#!/usr/bin/env python3
"""Auto-decompile computed-index field loads (24 bytes):

    lwz r0, F(r3) ; subf r0, r0, r5 ; slwi r0, r0, 2 ; add r3, r3, r0 ; lwz r3, G(r3) ; blr

i.e. return *(int*)((char*)p + (i - p->F)*4 + G), with the base index i in r5
(so the source has an unused second parameter, verified: all instances use r5).

Usage: python3 tools/bank_cidx.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
LAST = os.path.join(ROOT, ".bankstate", "last_rel.txt")
BADFILE = os.path.join(ROOT, ".bankstate", "bad_rel.txt")
IDENT = re.compile(r'^[A-Za-z_]\w*$')

rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
nsec = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = None
for i in range(nsec):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff = o & ~3
        break


def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v


def classify(a, sz):
    if sz != 24:
        return None
    w = struct.unpack('>6I', rel[textoff + a:textoff + a + 24])
    if w[5] != 0x4E800020:
        return None
    if (w[0] >> 26) != 32 or ((w[0] >> 21) & 31) != 0 or ((w[0] >> 16) & 31) != 3:   # lwz r0, F(r3)
        return None
    if ((w[1] >> 1) & 0x3FF) != 40 or ((w[1] >> 21) & 31) != 0 \
            or ((w[1] >> 16) & 31) != 0 or ((w[1] >> 11) & 31) != 5:                  # subf r0, r0, r5
        return None
    if w[2] != 0x5400103A or w[3] != 0x7C630214:                                      # slwi r0,r0,2 ; add r3,r3,r0
        return None
    if (w[4] >> 26) != 32 or ((w[4] >> 21) & 31) != 3 or ((w[4] >> 16) & 31) != 3:    # lwz r3, G(r3)
        return None
    return sign16(w[0] & 0xFFFF), sign16(w[4] & 0xFFFF)


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
    if isd(a) or a in bad or not IDENT.match(n):
        continue
    if banked >= maxf:
        break
    c = classify(a, sz)
    if not c:
        continue
    f, g = c
    src = (f"int {n}(void* p, int d, int i) {{\n"
           f"    return *(int*)((char*)p + (i - *(int*)((char*)p + {f})) * 4 + {g});\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/ci_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} computed-index field loads")

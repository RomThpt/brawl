#!/usr/bin/env python3
"""Auto-decompile single-byte bitfield setters (16 bytes):

    lbz r0, OFF(r3) ; rlwimi r0, r4, SH, MB, ME ; stb r0, OFF(r3) ; blr

i.e. s->field = v, where field is a WIDTH-bit bitfield inside the byte at OFF,
starting START bits from the top of the byte. START = MB-24, WIDTH = ME-MB+1;
MWCC picks SH itself, so reproducing the struct is enough.

Usage: python3 tools/bank_bfbyte.py <module> [max_functions]
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


def classify(a, sz):
    if sz != 16:
        return None
    w = struct.unpack('>4I', rel[textoff + a:textoff + a + 16])
    if w[3] != 0x4E800020:
        return None
    if (w[0] >> 26) != 34 or ((w[0] >> 21) & 31) != 0 or ((w[0] >> 16) & 31) != 3:   # lbz r0, OFF(r3)
        return None
    if (w[1] >> 26) != 20 or ((w[1] >> 21) & 31) != 4 or ((w[1] >> 16) & 31) != 0:   # rlwimi r0, r4
        return None
    if (w[2] >> 26) != 38 or ((w[2] >> 21) & 31) != 0 or ((w[2] >> 16) & 31) != 3:   # stb r0, OFF(r3)
        return None
    off = w[0] & 0xFFFF
    if off != (w[2] & 0xFFFF):
        return None
    mb = (w[1] >> 6) & 31
    me = (w[1] >> 1) & 31
    if mb < 24 or me < mb:                                                            # must sit inside the byte
        return None
    return off, mb - 24, me - mb + 1


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
    off, start, width = c
    pad = f"    unsigned char p0 : {start};\n" if start else ""
    src = (f"typedef struct {{\n    char pad[{off}];\n{pad}"
           f"    unsigned char f : {width};\n}} S;\n\n"
           f"void {n}(S* s, unsigned char v) {{\n    s->f = v;\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/bb_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} single-byte bitfield setters")

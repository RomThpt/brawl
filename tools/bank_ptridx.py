#!/usr/bin/env python3
"""Auto-decompile indexed accessors through a pointer field (16 bytes):

    lwz rB, OFF(r3) ; slwi r0, idx, 2 ; <indexed op> ; blr

where the object holds a pointer at OFF and the body loads/stores element [i] of
the int/float array it points at:

    lwzx  r3, rB, r0   -> int   f(void* p, int i)          return arr[i];
    lfsx  f1, rB, r0   -> float f(void* p, int i)          return arr[i];
    stfsx f1, rB, r0   -> void  f(void* p, int i, float v) arr[i] = v;
    stwx  r4, rB, r0   -> void  f(void* p, int v, int i)   arr[i] = v;

with arr = (T*)*(void**)((char*)p + OFF). All four register signatures are fixed
(verified homogeneous across the corpus); scale is always 4.

Usage: python3 tools/bank_ptridx.py <module> [max_functions]
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

# xo -> (idx_reg, src_reg) that this generator knows how to name
SHAPE = {23: ("lwzx", 4, 3), 535: ("lfsx", 4, 1),
         663: ("stfsx", 4, 1), 151: ("stwx", 5, 4)}


def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v


def classify(a, sz):
    if sz != 16:
        return None
    w = struct.unpack('>4I', rel[textoff + a:textoff + a + 16])
    if w[3] != 0x4E800020:
        return None
    if (w[0] >> 26) != 32 or ((w[0] >> 16) & 31) != 3:      # lwz rB, OFF(r3)
        return None
    rB = (w[0] >> 21) & 31
    off = sign16(w[0] & 0xFFFF)
    if (w[1] >> 26) != 21:                                  # slwi r0, idx, SH
        return None
    idx, rA1, SH, MB, ME = ((w[1] >> 21) & 31, (w[1] >> 16) & 31,
                            (w[1] >> 11) & 31, (w[1] >> 6) & 31, (w[1] >> 1) & 31)
    if rA1 != 0 or MB != 0 or ME != 31 - SH or SH != 2:
        return None
    if (w[2] >> 26) != 31:
        return None
    xo = (w[2] >> 1) & 0x3FF
    if xo not in SHAPE:
        return None
    op, want_idx, want_src = SHAPE[xo]
    src, rAx, rBx = (w[2] >> 21) & 31, (w[2] >> 16) & 31, (w[2] >> 11) & 31
    if rAx != rB or rBx != 0 or idx != want_idx or src != want_src:
        return None
    return op, off


def source(n, op, off):
    arr_i = f"((int*)*(void**)((char*)p + {off}))"
    arr_f = f"((float*)*(void**)((char*)p + {off}))"
    if op == "lwzx":
        return f"int {n}(void* p, int i) {{\n    return {arr_i}[i];\n}}\n"
    if op == "lfsx":
        return f"float {n}(void* p, int i) {{\n    return {arr_f}[i];\n}}\n"
    if op == "stfsx":
        return f"void {n}(void* p, int i, float v) {{\n    {arr_f}[i] = v;\n}}\n"
    return f"void {n}(void* p, int v, int i) {{\n    {arr_i}[i] = v;\n}}\n"


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
    op, off = c
    add_unit_rel.add(module, f"mo_stub/{module}/pi_{n}.c", a, a + sz, source(n, op, off))
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} pointer-indexed accessors")

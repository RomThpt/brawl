#!/usr/bin/env python3
"""Auto-decompile read-modify-write accessors on a pointer-field array (24 bytes):

    lwz rB, OFF(r3) ; slwi r3, i, 2 ; lwzx r0, rB, r3 ; <op> r0 ; stwx r0, rB, r3 ; blr

i.e. arr[i] OP= val, with arr = (int*)*(void**)((char*)p + OFF), val in r4, i in r5.
The middle op selects the compound assignment:

    andc r0,r0,r4 -> &= ~val      or  r0,r0,r4 -> |= val
    add  r0,r0,r4 -> += val       subf r0,r4,r0 -> -= val
    mullw r0,r0,r4 -> *= val

All register signatures are fixed and verified homogeneous.

Usage: python3 tools/bank_rmwidx.py <module> [max_functions]
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


# op word (r0,r4 operands) -> C compound assignment fragment
OPS = {
    0x7C002078: "{a} &= ~val;",     # andc r0,r0,r4
    0x7C002378: "{a} |= val;",      # or   r0,r0,r4
    0x7C002214: "{a} += val;",      # add  r0,r0,r4
    0x7C040050: "{a} -= val;",      # subf r0,r4,r0
    0x7C0021D6: "{a} *= val;",      # mullw r0,r0,r4
}


def classify(a, sz):
    if sz != 24:
        return None
    w = struct.unpack('>6I', rel[textoff + a:textoff + a + 24])
    if w[5] != 0x4E800020:
        return None
    if (w[0] >> 26) != 32 or ((w[0] >> 16) & 31) != 3:            # lwz rB, OFF(r3)
        return None
    rB = (w[0] >> 21) & 31
    if w[1] != 0x54A3103A:                                        # slwi r3, r5, 2
        return None
    if w[2] != (31 << 26 | 0 << 21 | rB << 16 | 3 << 11 | 23 << 1):  # lwzx r0, rB, r3
        return None
    if w[3] not in OPS:
        return None
    if w[4] != (31 << 26 | 0 << 21 | rB << 16 | 3 << 11 | 151 << 1):  # stwx r0, rB, r3
        return None
    return OPS[w[3]], sign16(w[0] & 0xFFFF)


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
    frag, off = c
    body = frag.format(a=f"((int*)*(void**)((char*)p + {off}))[i]")
    src = f"void {n}(void* p, int val, int i) {{\n    {body}\n}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/rm_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} read-modify-write accessors")

#!/usr/bin/env python3
"""Auto-decompile two-output word+float getters (20 bytes):

    lwz r0, A(r3) ; stw r0, 0(r4) ; lfs f0, B(r3) ; stfs f0, 0(r5) ; blr

i.e. void f(this, int* a, float* b) { *a = this->A; *b = this->B; } reading an int
field and a float field of the object and writing them through two out-pointers.

Usage: python3 tools/bank_mcopy.py <module> [max_functions]
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
    if sz != 20:
        return None
    w = struct.unpack('>5I', rel[textoff + a:textoff + a + 20])
    if w[4] != 0x4E800020:
        return None
    if (w[0] >> 26) != 32 or ((w[0] >> 21) & 31) != 0 or ((w[0] >> 16) & 31) != 3:   # lwz r0, A(r3)
        return None
    if w[1] != (36 << 26 | 0 << 21 | 4 << 16):                                        # stw r0, 0(r4)
        return None
    if (w[2] >> 26) != 48 or ((w[2] >> 21) & 31) != 0 or ((w[2] >> 16) & 31) != 3:    # lfs f0, B(r3)
        return None
    if w[3] != (52 << 26 | 0 << 21 | 5 << 16):                                        # stfs f0, 0(r5)
        return None
    return sign16(w[0] & 0xFFFF), sign16(w[2] & 0xFFFF)


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
    ao, bo = c
    src = (f"void {n}(void* t, int* a, float* b) {{\n"
           f"    *a = *(int*)((char*)t + {ao});\n"
           f"    *b = *(float*)((char*)t + {bo});\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/mc_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} two-output word+float getters")

#!/usr/bin/env python3
"""Auto-decompile consecutive-int setters:

    stw r4, o0(r3) ; stw r5, o1(r3) ; ... ; stw r(N+3), oN(r3) ; blr

storing N int parameters into N fields of one object. N ranges over 2..7;
offsets are read from the instructions.

Usage: python3 tools/bank_iset.py <module> [max_functions]
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
    if sz < 12 or sz % 4:
        return None
    n = sz // 4 - 1
    if n < 2 or n > 7:
        return None
    w = struct.unpack(f'>{sz // 4}I', rel[textoff + a:textoff + a + sz])
    if w[-1] != 0x4E800020:
        return None
    offs = []
    for k in range(n):                                 # stw r(k+4), o(r3)
        if (w[k] >> 26) != 36 or ((w[k] >> 21) & 31) != k + 4 or ((w[k] >> 16) & 31) != 3:
            return None
        offs.append(sign16(w[k] & 0xFFFF))
    return offs


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
    offs = classify(a, sz)
    if not offs:
        continue
    params = ", ".join(f"int a{k}" for k in range(len(offs)))
    body = "".join(f"    *(int*)((char*)p + {o}) = a{k};\n" for k, o in enumerate(offs))
    src = f"void {n}(void* p, {params}) {{\n{body}}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/is_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} consecutive-int setters")

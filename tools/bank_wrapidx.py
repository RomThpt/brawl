#!/usr/bin/env python3
"""Auto-decompile wrapped-index subobject accessors.

Shape (r3 = object, r4 = index):

    lwz r0, OFF(r3) ; srawi r0, r0, SH ; add r4, r0, r4
    cmpwi r4, N ; blt +8 ; addi r4, r4, -N
    mulli r0, r4, M ; add r3, r3, r0 ; addi r3, r3, A ; blr

which is a ring-buffer style lookup: take a stored cursor from a field, offset it
by the argument, wrap it into [0, N), and return the element's address.

Every constant (OFF, SH, N, M, A) is read straight out of the instructions.

Usage: python3 tools/bank_wrapidx.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 200
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"

rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
num = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = None
for i in range(num):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff = o & ~3
        break


def sign16(v):
    return v - 0x10000 if v >= 0x8000 else v


def classify(a, sz):
    if sz != 40:
        return None
    w = [struct.unpack('>I', rel[textoff + a + i * 4:textoff + a + i * 4 + 4])[0]
         for i in range(10)]
    # lwz r0, OFF(r3)
    if (w[0] >> 26) != 32 or ((w[0] >> 21) & 31) != 0 or ((w[0] >> 16) & 31) != 3:
        return None
    off = sign16(w[0] & 0xFFFF)
    # srawi r0, r0, SH
    if (w[1] >> 26) != 31 or ((w[1] >> 1) & 0x3FF) != 824:
        return None
    if ((w[1] >> 21) & 31) != 0 or ((w[1] >> 16) & 31) != 0:
        return None
    sh = (w[1] >> 11) & 31
    # add r4, r0, r4
    if w[2] != 0x7C802214:
        return None
    # cmpwi r4, N
    if (w[3] >> 26) != 11 or ((w[3] >> 16) & 31) != 4:
        return None
    n = sign16(w[3] & 0xFFFF)
    # blt cr0, +8  (BO=12, BI=0)
    if w[4] != 0x41800008:
        return None
    # addi r4, r4, -N
    if (w[5] & 0xFFFF0000) != 0x38840000 or sign16(w[5] & 0xFFFF) != -n:
        return None
    # mulli r0, r4, M
    if (w[6] >> 26) != 7 or ((w[6] >> 21) & 31) != 0 or ((w[6] >> 16) & 31) != 4:
        return None
    mul = sign16(w[6] & 0xFFFF)
    # add r3, r3, r0 ; addi r3, r3, A ; blr
    if w[7] != 0x7C630214 or (w[8] & 0xFFFF0000) != 0x38630000 or w[9] != 0x4E800020:
        return None
    return off, sh, n, mul, sign16(w[8] & 0xFFFF)


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
    off, sh, cnt, mul, add = c
    src = (f"void* {n}(void* p, int i) {{\n"
           f"    int idx = (*(int*)((char*)p + {off}) >> {sh}) + i;\n"
           f"    if (idx >= {cnt}) idx -= {cnt};\n"
           f"    return (char*)p + idx * {mul} + {add};\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/wi_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} wrapped-index accessors")

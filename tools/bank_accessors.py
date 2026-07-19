#!/usr/bin/env python3
"""Auto-decompile index-to-subobject accessors.

Two hand-decompiled families turned out to share one formulaic shape:

    cmpwi r4, N ; bne skip ; addi r3, r3, OFF ; blr     (repeated, N descending)
    li r3, 0 ; blr

That is mechanical, so there is no reason to write it by hand each time. This
recognises the shape anywhere in the REL modules and emits the matching C.

Usage: python3 tools/bank_accessors.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 40
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


def words(a, n):
    return [struct.unpack('>I', rel[textoff + a + i * 4:textoff + a + i * 4 + 4])[0]
            for i in range(n)]


def parse_accessor(a, sz):
    """-> list of (case_value, offset) if the function is an accessor cascade."""
    if sz < 24 or sz % 4 or (sz - 8) % 16:
        return None
    n_cases = (sz - 8) // 16
    w = words(a, sz // 4)
    cases = []
    for k in range(n_cases):
        cmp_, bne, addi, blr = w[k * 4:k * 4 + 4]
        # cmpwi r4, imm
        if (cmp_ >> 26) != 11 or ((cmp_ >> 16) & 31) != 4:
            return None
        # bne cr0, +12
        if bne != 0x4082000C:
            return None
        # addi r3, r3, off
        if (addi & 0xFFFF0000) != 0x38630000:
            return None
        if blr != 0x4E800020:
            return None
        v = cmp_ & 0xFFFF
        cases.append((v - 0x10000 if v >= 0x8000 else v,
                      addi & 0xFFFF))
    # tail: li r3, 0 ; blr
    if w[-2] != 0x38600000 or w[-1] != 0x4E800020:
        return None
    return cases


done = []
splits = os.path.join(ROOT, "config/RSBE01_02/rels", module, "splits.txt")
for line in open(splits):
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
    cases = parse_accessor(a, sz)
    if not cases:
        continue
    body = "".join(f"    if (i == {v}) return (char*)p + {off};\n" for v, off in cases)
    src = f"void* {n}(void* p, int i) {{\n{body}    return 0;\n}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/acc_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} accessors")

#!/usr/bin/env python3
"""Auto-decompile a few small leftover shapes.

    li r0,0 ; stb r0,OFF(r3) ; blr              -> p->byte = 0
    lha r0,0(r4) ; sth r0,0(r3) ; blr           -> *dst = *src   (short copy)
    li r0,V ; stw r0,OFF(r3) ; blr              -> p->word = V
    li r0,V ; sth r0,OFF(r3) ; blr              -> p->half = V

Small individually, but they add up and cost nothing to recognise.

Usage: python3 tools/bank_misc.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"
IDENT = re.compile(r'^[A-Za-z_]\w*$')

# Modules dont le .text généré est correct mais dont le REL diffère malgré tout
# (la table de relocations ne retombe pas sur ses pieds). Vérifié, pas récupérable
# depuis ce générateur.
SKIP = {"sora_melee"}
if module in SKIP:
    print(f"[{module}] skipped (rejette ces formes, cf. NOTES.md)")
    sys.exit(0)

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


STORE = {38: ("char", 1), 44: ("short", 2), 36: ("int", 4)}


def classify(a, sz):
    if sz != 12:
        return None
    w0, w1, w2 = struct.unpack('>III', rel[textoff + a:textoff + a + 12])
    if w2 != 0x4E800020:
        return None
    # lha r0,0(r4) ; sth r0,0(r3) -> copie de short
    if w0 == 0xA8040000 and w1 == 0xB0030000:
        return ("copy", None, None, None)
    # li r0, V ; st{b,h,w} r0, OFF(r3)
    if (w0 & 0xFFFF0000) != 0x38000000:
        return None
    val = sign16(w0 & 0xFFFF)
    prim = w1 >> 26
    if prim not in STORE or ((w1 >> 21) & 31) != 0 or ((w1 >> 16) & 31) != 3:
        return None
    ty, _ = STORE[prim]
    return ("set", ty, sign16(w1 & 0xFFFF), val)


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
    kind, ty, off, val = c
    if kind == "copy":
        src = f"void {n}(short* dst, short* src) {{\n    *dst = *src;\n}}\n"
    else:
        src = (f"void {n}(void* p) {{\n"
               f"    *({ty}*)((char*)p + {off}) = {val};\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/ms_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} misc small functions")

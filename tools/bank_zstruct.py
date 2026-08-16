#!/usr/bin/env python3
"""Return-a-zeroed-8-byte-struct (32 bytes, one fixed shape):

    stwu r1,-16 ; li r0,0 ; li r3,0 ; li r4,0 ; stw r0,8(r1) ; stw r0,12(r1) ; addi r1,r1,16 ; blr
    -> typedef struct { int a, b; } S;  S f(void) { S s = {0, 0}; return s; }

Usage: python3 tools/bank_zstruct.py <module> [max_functions]
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
SHAPE = (0x9421FFF0, 0x38000000, 0x38600000, 0x38800000,
         0x90010008, 0x9001000C, 0x38210010, 0x4E800020)
rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
nsec = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = None
for i in range(nsec):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff = o & ~3; break
done = []
for line in open(os.path.join(ROOT, "config/RSBE01_02/rels", module, "splits.txt")):
    m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', line)
    if m: done.append((int(m.group(1), 16), int(m.group(2), 16)))
isd = lambda a: any(s <= a < e for s, e in done)
bad = set()
if os.path.exists(BADFILE):
    for m2, a2 in re.findall(r'([A-Za-z]\w*):([0-9A-Fa-f]{8})', open(BADFILE).read()):
        if m2 == module: bad.add(int(a2, 16))
banked, addrs = 0, []
for line in open(os.path.join(ROOT, "config/RSBE01_02/rels", module, "symbols.txt")):
    m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', line)
    if not m: continue
    n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
    if sz != 32 or isd(a) or a in bad or not IDENT.match(n): continue
    if banked >= maxf: break
    if struct.unpack('>8I', rel[textoff + a:textoff + a + 32]) != SHAPE: continue
    src = ("typedef struct { int a, b; } S;\n\n"
           f"S {n}(void) {{\n    S s = {{0, 0}};\n    return s;\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/zs_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}"); banked += 1
open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} zeroed-struct returns")

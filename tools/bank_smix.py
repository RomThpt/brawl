#!/usr/bin/env python3
"""Mixed char+int+float field setter (16 bytes):

    stb r4,A(r3) ; stw r5,B(r3) ; stfs f1,C(r3) ; blr
    -> void f(void* p, char a, int b, float c) { p->A=a; p->B=b; p->C=c; }

Register layout is fixed (verified homogeneous); offsets read from instructions.

Usage: python3 tools/bank_smix.py <module> [max_functions]
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
        textoff = o & ~3; break
def sign16(v): return v - 0x10000 if v >= 0x8000 else v
def classify(a, sz):
    if sz != 16: return None
    w = struct.unpack('>4I', rel[textoff + a:textoff + a + 16])
    if w[3] != 0x4E800020: return None
    if (w[0] >> 26) != 38 or ((w[0] >> 21) & 31) != 4 or ((w[0] >> 16) & 31) != 3: return None  # stb r4,A(r3)
    if (w[1] >> 26) != 36 or ((w[1] >> 21) & 31) != 5 or ((w[1] >> 16) & 31) != 3: return None  # stw r5,B(r3)
    if (w[2] >> 26) != 52 or ((w[2] >> 21) & 31) != 1 or ((w[2] >> 16) & 31) != 3: return None  # stfs f1,C(r3)
    return sign16(w[0] & 0xFFFF), sign16(w[1] & 0xFFFF), sign16(w[2] & 0xFFFF)
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
    if isd(a) or a in bad or not IDENT.match(n): continue
    if banked >= maxf: break
    c = classify(a, sz)
    if not c: continue
    A, B, C = c
    src = (f"void {n}(void* p, char a, int b, float c) {{\n"
           f"    *(char*)((char*)p + {A}) = a;\n"
           f"    *(int*)((char*)p + {B}) = b;\n"
           f"    *(float*)((char*)p + {C}) = c;\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/sm_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}"); banked += 1
open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} mixed char+int+float setters")

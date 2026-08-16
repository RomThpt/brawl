#!/usr/bin/env python3
"""Large-offset subobject address (12 bytes):

    addis r3,r3,HI ; addi r3,r3,LO ; blr   ->  return (char*)p + ((HI<<16)+LO)

The big-offset counterpart of bank_field's single addi.

Usage: python3 tools/bank_bigfield.py <module> [max_functions]
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
textoff = textidx = None
for i in range(nsec):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff, textidx = o & ~3, i; break
def sign16(v): return v - 0x10000 if v >= 0x8000 else v
# offsets in .text that carry a relocation (addis/addi -> a global address, NOT a
# constant offset). HA/LO relocs sit at instruction+2, so record both.
RELOC = set()
_imp_off, _imp_size = struct.unpack('>II', rel[0x28:0x30])
for _i in range(_imp_size // 8):
    _mid, _roff = struct.unpack('>II', rel[_imp_off + _i * 8:_imp_off + _i * 8 + 8])
    _pos, _cs, _cur = _roff, -1, 0
    while _pos + 8 <= len(rel):
        _o, _t, _sec, _add = struct.unpack('>HBBI', rel[_pos:_pos + 8]); _pos += 8
        if _t == 203: break
        if _t == 202: _cs, _cur = _sec, 0; continue
        _cur += _o
        if _t == 201: continue
        if _cs == textidx: RELOC.add(_cur); RELOC.add(_cur - 2)
def classify(a, sz):
    if sz != 12: return None
    if (a in RELOC) or (a + 4 in RELOC):                # addis/addi to a global -> skip
        return None
    w = struct.unpack('>3I', rel[textoff + a:textoff + a + 12])
    if w[2] != 0x4E800020: return None
    if (w[0] >> 26) != 15 or ((w[0] >> 21) & 31) != 3 or ((w[0] >> 16) & 31) != 3:   # addis r3,r3,HI
        return None
    if (w[1] >> 26) != 14 or ((w[1] >> 21) & 31) != 3 or ((w[1] >> 16) & 31) != 3:   # addi r3,r3,LO
        return None
    return (w[0] & 0xFFFF) * 0x10000 + sign16(w[1] & 0xFFFF)
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
    off = classify(a, sz)
    if off is None: continue
    src = f"void* {n}(void* p) {{\n    return (char*)p + {off};\n}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/lo_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}"); banked += 1
open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} large-offset field addresses")

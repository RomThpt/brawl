#!/usr/bin/env python3
"""Auto-decompile trivial deleting destructors.

MWCC emits one of these next to every class whose destructor does nothing but
possibly free the object:

    if (this) { if (flag > 0) operator delete(this); }
    return this;

Shape (64 bytes): frame, cmpwi r3,0 early, save r31 = this, the two guards, a
call whose relocation points at operator delete, then restore and return this.

The callee is read from the REL24 relocation rather than assumed, so a module
calling something else is skipped instead of silently mismatched.

Usage: python3 tools/bank_dtor.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"

rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
nsec = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = textidx = None
for i in range(nsec):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff, textidx = o & ~3, i
        break


def load_relocs():
    imp_off, imp_size = struct.unpack('>II', rel[0x28:0x30])
    out = {}
    for i in range(imp_size // 8):
        mid, roff = struct.unpack('>II', rel[imp_off + i * 8:imp_off + i * 8 + 8])
        pos, cur_sec, cur = roff, -1, 0
        while pos + 8 <= len(rel):
            off, typ, sec, add = struct.unpack('>HBBI', rel[pos:pos + 8])
            pos += 8
            if typ == 203:
                break
            if typ == 202:
                cur_sec, cur = sec, 0
                continue
            cur += off
            if typ == 201:
                continue
            if cur_sec == textidx:
                out[cur] = (typ, mid, sec, add)
    return out


R = load_relocs()

# DOL symbols, to name the callee when the relocation points into the main binary
DOLSYM = {}
for line in open(os.path.join(ROOT, "config/RSBE01_02/symbols.txt")):
    m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);', line)
    if m:
        DOLSYM.setdefault(int(m.group(2), 16), m.group(1))

# fixed prologue/epilogue of the shape; only the call word varies
HEAD = [0x9421FFF0, 0x7C0802A6, 0x2C030000, 0x90010014, 0x93E1000C,
        0x7C7F1B78, 0x41820010, 0x2C040000, 0x40810008]
TAIL = [0x7FE3FB78, 0x83E1000C, 0x80010014, 0x7C0803A6, 0x38210010, 0x4E800020]


def classify(a, sz):
    if sz != 64:
        return None
    w = [struct.unpack('>I', rel[textoff + a + i * 4:textoff + a + i * 4 + 4])[0]
         for i in range(16)]
    if w[:9] != HEAD or w[10:] != TAIL:
        return None
    if (w[9] >> 26) != 18 or not (w[9] & 1):          # must be a bl
        return None
    r = R.get(a + 9 * 4)
    if not r or r[0] != 10:                            # REL24 relocation
        return None
    typ, mid, sec, add = r
    if mid != 0:                                       # only the DOL case here
        return None
    name = DOLSYM.get(add)
    if not name or not re.match(r'^[A-Za-z_]\w*$', name):
        return None
    return name


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
    callee = classify(a, sz)
    if not callee or callee == n:
        continue
    src = (f"extern void {callee}(void* p);\n\n"
           f"void* {n}(void* p, int flag) {{\n"
           f"    if (p) {{\n        if (flag > 0) {{\n            {callee}(p);\n"
           f"        }}\n    }}\n    return p;\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/dt_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} trivial deleting destructors")

#!/usr/bin/env python3
"""Auto-decompile getters that read or take the address of a module global.

    lis rX, HA(sym) ; lfs f1, LO(sym)(rX) ; blr    -> return sym;      (float)
    lis rX, HA(sym) ; addi r3, rX, LO(sym) ; blr   -> return &sym;

The immediates are zero in the file: the address arrives through a pair of
relocations (type 6 = ADDR16_HA on the lis, type 4 = ADDR16_LO on the second
instruction), and those carry the target section and offset. Resolving that
against the module's symbol table gives the name to reference.

Note the relocation sits at instruction+2, since it patches the low halfword.

Usage: python3 tools/bank_globals.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"

# REL section index -> the name the symbol table uses
SECNAME = {1: ".text", 2: ".ctors", 3: ".dtors", 4: ".rodata", 5: ".data", 6: ".bss"}

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

# symbol table: (section name, offset) -> name, keeping the largest symbol that starts there
SYMS = {}
for line in open(os.path.join(ROOT, "config/RSBE01_02/rels", module, "symbols.txt")):
    m = re.match(r'(\S+)\s*=\s*(\.\w+):0x([0-9A-Fa-f]+);', line)
    if m and re.match(r'^[A-Za-z_]\w*$', m.group(1)):
        SYMS.setdefault((m.group(2), int(m.group(3), 16)), m.group(1))


def w(a, i):
    return struct.unpack('>I', rel[textoff + a + i * 4:textoff + a + i * 4 + 4])[0]


def target_of(a):
    """Resolve the HA/LO relocation pair starting at instruction address a."""
    hi, lo = R.get(a + 2), R.get(a + 6)
    if not hi or not lo or hi[0] != 6 or lo[0] != 4:
        return None
    if hi[1] != lo[1] or hi[2] != lo[2] or hi[3] != lo[3]:
        return None
    sec = SECNAME.get(hi[2])
    if sec is None:
        return None
    return SYMS.get((sec, hi[3]))


def classify(a, sz):
    if sz != 12:
        return None
    w0, w1, w2 = w(a, 0), w(a, 1), w(a, 2)
    if w2 != 0x4E800020:
        return None
    if (w0 >> 26) != 15 or ((w0 >> 16) & 31) != 0:      # lis rX, 0
        return None
    rX = (w0 >> 21) & 31
    name = target_of(a)
    if not name:
        return None
    if (w1 >> 26) == 48 and ((w1 >> 16) & 31) == rX:    # lfs f1, LO(rX)
        if ((w1 >> 21) & 31) != 1:
            return None
        return ("float", name)
    if (w1 >> 26) == 14 and ((w1 >> 16) & 31) == rX:    # addi r3, rX, LO
        if ((w1 >> 21) & 31) != 3:
            return None
        return ("addr", name)
    return None


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
    if isd(a) or a in bad or not re.match(r'^[A-Za-z_]\w*$', n) or n == m.group(1) == "":
        continue
    if banked >= maxf:
        break
    c = classify(a, sz)
    if not c:
        continue
    kind, sym = c
    if sym == n:
        continue
    if kind == "float":
        src = f"extern const float {sym};\n\nfloat {n}(void) {{\n    return {sym};\n}}\n"
    else:
        src = f"extern char {sym};\n\nvoid* {n}(void) {{\n    return &{sym};\n}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/gl_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} global getters")

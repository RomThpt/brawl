#!/usr/bin/env python3
"""Auto-decompile cross-module tail-call thunks.

    addi r3, r3, X ; b target        -> return target((char*)p + X);

where target lives in another module (or the DOL). The branch carries a REL24
relocation giving the target module id and offset; resolving that against the
target's symbol table yields the name.

Two things make this safe to automate:
  - the callee is read from the relocation, never guessed;
  - names that are not valid C identifiers are skipped. Many targets are C++
    template methods whose mangled names contain angle brackets, and those simply
    cannot be declared from a C file.

Usage: python3 tools/bank_xmod.py <module> [max_functions]
"""
import struct, re, os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"
IDENT = re.compile(r'^[A-Za-z_]\w*$')

# module id -> name, read from each REL header
ID2MOD = {}
for f in glob.glob(os.path.join(ROOT, "orig/RSBE01_02/files/module/*.rel")):
    ID2MOD[struct.unpack('>I', open(f, "rb").read(4))[0]] = os.path.basename(f)[:-4]

_symcache = {}


def text_symbols(mod_name):
    """(offset in .text) -> symbol name, for a module or the DOL."""
    if mod_name in _symcache:
        return _symcache[mod_name]
    path = (os.path.join(ROOT, "config/RSBE01_02/symbols.txt") if mod_name is None
            else os.path.join(ROOT, "config/RSBE01_02/rels", mod_name, "symbols.txt"))
    out = {}
    if os.path.exists(path):
        for line in open(path):
            m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function', line)
            if m:
                out.setdefault(int(m.group(2), 16), m.group(1))
    _symcache[mod_name] = out
    return out


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


def classify(a, sz):
    if sz != 8:
        return None
    w0, w1 = struct.unpack('>II', rel[textoff + a:textoff + a + 8])
    if (w0 & 0xFFFF0000) != 0x38630000:          # addi r3, r3, X
        return None
    if (w1 >> 26) != 18 or (w1 & 3):             # plain b, no link, no absolute
        return None
    r = R.get(a + 4)
    if not r or r[0] != 10:                      # REL24
        return None
    _, mid, sec, add = r
    if mid == 0:                                 # into the DOL
        name = text_symbols(None).get(add)
    else:
        mod_name = ID2MOD.get(mid)
        if mod_name is None or mod_name == module:
            return None
        name = text_symbols(mod_name).get(add)
    if not name or not IDENT.match(name):        # C++ template manglings, etc.
        return None
    v = w0 & 0xFFFF
    return name, (v - 0x10000 if v >= 0x8000 else v)


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
    callee, off = c
    if callee == n:
        continue
    src = (f"extern int {callee}();\n\n"
           f"int {n}(void* p) {{\n    return {callee}((char*)p + ({off}));\n}}\n")
    add_unit_rel.add(module, f"mo_stub/{module}/xm_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} cross-module thunks")

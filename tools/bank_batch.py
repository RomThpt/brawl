#!/usr/bin/env python3
"""Batch-decompile trivial functions (empty / return-const) from the DOL.
Scans for undecompiled trivial functions, groups contiguous ones into units,
and creates src+split+configure for a batch. Then the caller builds/verifies.

Usage: python3 tools/bank_batch.py <max_functions>
"""
import re, struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import add_unit

ROOT = add_unit.ROOT
dol = open(os.path.join(ROOT, "orig/RSBE01_02/sys/main.dol"), "rb").read()
offs = struct.unpack('>7I', dol[0x00:0x1C]); addrs = struct.unpack('>7I', dol[0x48:0x64]); sizes = struct.unpack('>7I', dol[0x90:0xAC])


def rd(va, n):
    for o, a, s in zip(offs, addrs, sizes):
        if s and a <= va < a + s:
            return dol[o + va - a:o + va - a + n]
    return None


done = []
for line in open(os.path.join(ROOT, "config/RSBE01_02/splits.txt")):
    m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', line)
    if m:
        done.append((int(m.group(1), 16), int(m.group(2), 16)))
isdone = lambda a: any(s <= a < e for s, e in done)

# bad-list: functions that break the DOL when carved (skip them)
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_funcs.txt"
bad = set()
if os.path.exists(BADFILE):
    for line in open(BADFILE):
        line = line.strip()
        if line:
            bad.add(int(line, 16))


def soff(w0):
    o = w0 & 0xFFFF
    return o - 0x10000 if o >= 0x8000 else o


# load/store getter/setter opcodes: (high16, kind, ctype)
GET = {0x8063: ("int", "int"), 0x8863: ("uchar", "unsigned char"), 0xA063: ("ushort", "unsigned short")}
SET = {0x9083: ("int", "int"), 0x9883: ("uchar", "unsigned char"), 0xB083: ("ushort", "unsigned short")}


def kind(a, sz):
    if sz == 4:
        b = rd(a, 4)
        if b and struct.unpack('>I', b)[0] == 0x4E800020:
            return ("empty", None)
    if sz == 8:
        b = rd(a, 8)
        if b and len(b) == 8:
            w0, w1 = struct.unpack('>II', b)
            if w1 != 0x4E800020:
                return None
            hi = w0 >> 16
            if (w0 & 0xFFFF0000) == 0x38600000:
                return ("const", struct.unpack('>h', struct.pack('>H', w0 & 0xFFFF))[0])
            if hi in GET:  # lwz/lbz/lhz r3, off(r3) ; blr  => getter
                return ("get", (GET[hi][1], soff(w0)))
            if hi in SET:  # stw/stb/sth r4, off(r3) ; blr  => setter
                return ("set", (SET[hi][1], soff(w0)))
            if (w0 & 0xFC0007FE) == 0x7C000378:  # mr r3,rN ; blr => return argN
                rS, rA, rB = (w0 >> 21) & 0x1F, (w0 >> 16) & 0x1F, (w0 >> 11) & 0x1F
                if rA == 3 and rS == rB and 4 <= rS <= 10:
                    return ("argret", rS - 3)
    return None


# collect trivial funcs (only fn_ auto-named => safe extern C stubs; C names are self-contained too)
funcs = []
for line in open(os.path.join(ROOT, "config/RSBE01_02/symbols.txt")):
    m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', line)
    if not m:
        continue
    n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
    if isdone(a) or a in bad or '__' in n:  # skip decompiled + bad + mangled C++
        continue
    k = kind(a, sz)
    if k:
        funcs.append((a, sz, n, k))
funcs.sort()

# group contiguous
maxf = int(sys.argv[1]) if len(sys.argv) > 1 else 40
groups = []
cur = []
for f in funcs:
    if cur and f[0] == cur[-1][0] + cur[-1][1]:
        cur.append(f)
    else:
        if cur:
            groups.append(cur)
        cur = [f]
    if sum(len(g) for g in groups) + len(cur) >= maxf:
        break
if cur:
    groups.append(cur)

banked = 0
banked_addrs = []
for g in groups:
    if banked >= maxf:
        break
    start = g[0][0]
    end = g[-1][0] + g[-1][1]
    banked_addrs.extend(f[0] for f in g)
    body = []
    for a, sz, n, (kk, v) in g:
        if kk == "empty":
            body.append(f"void {n}(void) {{\n}}\n")
        elif kk == "const":
            body.append(f"int {n}(void) {{\n    return {v};\n}}\n")
        elif kk == "get":
            ctype, off = v
            body.append(f"int {n}(void* p) {{\n    return *({ctype}*)((char*)p + {off});\n}}\n")
        elif kk == "set":
            ctype, off = v
            body.append(f"void {n}(void* p, int q) {{\n    *({ctype}*)((char*)p + {off}) = q;\n}}\n")
        elif kk == "argret":
            params = ", ".join("int a%d" % i for i in range(v + 1))
            body.append(f"int {n}({params}) {{\n    return a{v};\n}}\n")
    src = "\n".join(body)
    path = f"stub/{g[0][2]}.c"
    add_unit.add(path, start, end, src)
    print(f"unit {path} [0x{start:08X}-0x{end:08X}] {len(g)} fn")
    banked += len(g)
with open("/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_batch.txt", "w") as f:
    f.write("\n".join("%08X" % a for a in banked_addrs))
print(f"TOTAL banked units: {len(groups)} covering {banked} functions")

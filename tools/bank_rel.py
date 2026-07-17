#!/usr/bin/env python3
"""Batch-decompile trivial functions (empty/const/getter/setter) in a REL module.
Usage: python3 tools/bank_rel.py <module> <max_functions>
"""
import re, struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import add_unit_rel

ROOT = add_unit_rel.ROOT
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"

module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 40

rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
num = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = None
for i in range(num):
    o, s = struct.unpack('>II', rel[sec_off + i*8:sec_off + i*8 + 8])
    if (o & 1) and s:  # first executable section = .text
        textoff = o & ~3
        break


def rdb(a, n):
    return rel[textoff + a:textoff + a + n]


GET = {0x8063: "int", 0x8863: "unsigned char", 0xA063: "unsigned short"}
SET = {0x9083: "int", 0x9883: "unsigned char", 0xB083: "unsigned short"}


def soff(w0):
    o = w0 & 0xFFFF
    return o - 0x10000 if o >= 0x8000 else o


def kind(a, sz):
    if sz == 4:
        if struct.unpack('>I', rdb(a, 4))[0] == 0x4E800020:
            return ("empty", None)
    if sz == 8:
        b = rdb(a, 8)
        if len(b) < 8:
            return None
        w0, w1 = struct.unpack('>II', b)
        if w1 != 0x4E800020:
            return None
        hi = w0 >> 16
        if (w0 & 0xFFFF0000) == 0x38600000:
            return ("const", struct.unpack('>h', struct.pack('>H', w0 & 0xFFFF))[0])
        if hi in GET:
            return ("get", (GET[hi], soff(w0)))
        if hi in SET:
            return ("set", (SET[hi], soff(w0)))
        if (w0 & 0xFC0007FE) == 0x7C000378:  # or rA,rS,rB == mr alias when rS==rB
            rS, rA, rB = (w0 >> 21) & 0x1F, (w0 >> 16) & 0x1F, (w0 >> 11) & 0x1F
            if rA == 3 and rS == rB and 4 <= rS <= 10:  # return argN (r3=a0)
                return ("argret", rS - 3)
        if (w0 >> 26) == 14:  # addi rD,rA,SIMM
            rD, rA = (w0 >> 21) & 0x1F, (w0 >> 16) & 0x1F
            if rD == 3 and rA == 3:  # return a0 + imm
                return ("addimm", struct.unpack('>h', struct.pack('>H', w0 & 0xFFFF))[0])
        if (w0 & 0xFC0007FE) == 0x7C000214:  # add rD,rA,rB
            rD, rA, rB = (w0 >> 21) & 0x1F, (w0 >> 16) & 0x1F, (w0 >> 11) & 0x1F
            if rD == 3 and {rA, rB} == {3, 4}:  # return a0 + a1
                return ("add2", None)
        xop = w0 & 0xFC0007FE  # bits25-21=f1, bits20-16=f2, bits15-11=f3
        f1, f2, f3 = (w0 >> 21) & 0x1F, (w0 >> 16) & 0x1F, (w0 >> 11) & 0x1F
        if xop == 0x7C0001D6 and f1 == 3 and {f2, f3} == {3, 4}:  # mullw rD,rA,rB
            return ("binop", "*")
        if xop == 0x7C0000D0 and f1 == 3 and f2 == 3:  # neg rD,rA
            return ("unop", "-")
        if xop == 0x7C000038 and f2 == 3 and {f1, f3} == {3, 4}:  # and rA,rS,rB
            return ("binop", "&")
        if xop == 0x7C000278 and f2 == 3 and {f1, f3} == {3, 4}:  # xor rA,rS,rB
            return ("binop", "^")
        if xop == 0x7C000378 and f2 == 3 and {f1, f3} == {3, 4} and f1 != f3:  # or (non-mr)
            return ("binop", "|")
        if xop == 0x7C0000F8 and f2 == 3 and f1 == 3 and f3 == 3:  # nor => not
            return ("unop", "~")
    return None


done = []
splits = os.path.join(ROOT, "config/RSBE01_02/rels", module, "splits.txt")
for line in open(splits):
    m = re.search(r'\.text\s+start:0x([0-9A-Fa-f]+)\s+end:0x([0-9A-Fa-f]+)', line)
    if m:
        done.append((int(m.group(1), 16), int(m.group(2), 16)))
isd = lambda a: any(s <= a < e for s, e in done)

bad = set()
if os.path.exists(BADFILE):
    for l in open(BADFILE):
        l = l.strip()
        if l and l.startswith(module + ":"):
            bad.add(int(l.split(":")[1], 16))

funcs = []
for line in open(os.path.join(ROOT, "config/RSBE01_02/rels", module, "symbols.txt")):
    m = re.match(r'(\S+)\s*=\s*\.text:0x([0-9A-Fa-f]+);.*type:function size:0x([0-9A-Fa-f]+)', line)
    if not m:
        continue
    n, a, sz = m.group(1), int(m.group(2), 16), int(m.group(3), 16)
    if isd(a) or a in bad or '__' in n:
        continue
    k = kind(a, sz)
    if k:
        funcs.append((a, sz, n, k))
funcs.sort()

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


def gen(n, kk, v):
    if kk == "empty":
        return f"void {n}(void) {{\n}}\n"
    if kk == "const":
        return f"int {n}(void) {{\n    return {v};\n}}\n"
    if kk == "get":
        t, off = v
        return f"int {n}(void* p) {{\n    return *({t}*)((char*)p + {off});\n}}\n"
    if kk == "argret":
        params = ", ".join("int a%d" % i for i in range(v + 1))
        return f"int {n}({params}) {{\n    return a{v};\n}}\n"
    if kk == "addimm":
        return f"int {n}(int a0) {{\n    return a0 + {v};\n}}\n"
    if kk == "add2":
        return f"int {n}(int a0, int a1) {{\n    return a0 + a1;\n}}\n"
    if kk == "binop":
        return f"int {n}(int a0, int a1) {{\n    return a0 {v} a1;\n}}\n"
    if kk == "unop":
        return f"int {n}(int a0) {{\n    return {v}a0;\n}}\n"
    t, off = v
    return f"void {n}(void* p, int q) {{\n    *({t}*)((char*)p + {off}) = q;\n}}\n"


banked = 0
addrs = []
for g in groups:
    if banked >= maxf:
        break
    start = g[0][0]
    end = g[-1][0] + g[-1][1]
    src = "\n".join(gen(n, kk, v) for a, sz, n, (kk, v) in g)
    path = f"mo_stub/{module}/{g[0][2]}.c"
    add_unit_rel.add(module, path, start, end, src)
    addrs.extend(f"{module}:{f[0]:08X}" for f in g)
    banked += len(g)
open(LAST, "w").write("\n".join(addrs))
print(f"[{module}] banked {len(groups)} units / {banked} functions")

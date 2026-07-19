#!/usr/bin/env python3
"""Minimal PowerPC disassembler for REL/DOL functions, with relocation annotations.

Enough coverage for the instruction mix Brawl's compiled C actually uses. Unknown
encodings print as .4byte so nothing is silently misread.

Usage: python3 tools/disasm.py <module> <hex_addr> [size]
       python3 tools/disasm.py DOL <hex_vaddr> [size]
"""
import struct, sys, os, re

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"

# primary-opcode instructions: prim -> (mnemonic, form)
PRIM = {
    14: ("addi", "d"), 15: ("addis", "d"), 12: ("addic", "d"), 13: ("addic.", "d"),
    7: ("mulli", "d"), 8: ("subfic", "d"),
    24: ("ori", "s"), 25: ("oris", "s"), 26: ("xori", "s"), 27: ("xoris", "s"),
    28: ("andi.", "s"), 29: ("andis.", "s"),
    32: ("lwz", "m"), 33: ("lwzu", "m"), 34: ("lbz", "m"), 35: ("lbzu", "m"),
    36: ("stw", "m"), 37: ("stwu", "m"), 38: ("stb", "m"), 39: ("stbu", "m"),
    40: ("lhz", "m"), 41: ("lhzu", "m"), 42: ("lha", "m"), 43: ("lhau", "m"),
    44: ("sth", "m"), 45: ("sthu", "m"), 46: ("lmw", "m"), 47: ("stmw", "m"),
    48: ("lfs", "f"), 49: ("lfsu", "f"), 50: ("lfd", "f"), 51: ("lfdu", "f"),
    52: ("stfs", "f"), 53: ("stfsu", "f"), 54: ("stfd", "f"), 55: ("stfdu", "f"),
}
# extended (prim 31) -> mnemonic
X31 = {
    266: "add", 40: "subf", 10: "addc", 8: "subfc", 138: "adde", 136: "subfe",
    235: "mullw", 75: "mulhw", 11: "mulhwu", 491: "divw", 459: "divwu",
    28: "and", 444: "or", 316: "xor", 476: "nand", 124: "nor", 284: "eqv",
    60: "andc", 412: "orc", 104: "neg", 954: "extsb", 922: "extsh",
    24: "slw", 536: "srw", 792: "sraw", 824: "srawi",
    0: "cmpw", 32: "cmplw", 339: "mfspr", 467: "mtspr", 19: "mfcr", 144: "mtcrf",
    23: "lwzx", 87: "lbzx", 279: "lhzx", 343: "lhax", 151: "stwx", 215: "stbx", 407: "sthx",
    535: "lfsx", 599: "lfdx", 663: "stfsx", 727: "stfdx", 86: "dcbf", 982: "icbi",
}
# la condition dépend de BO *et* de BI (bit dans le CR) : BI%4 -> lt/gt/eq/so
BI_BIT = {0: "lt", 1: "gt", 2: "eq", 3: "so"}
BI_NEG = {"lt": "ge", "gt": "le", "eq": "ne", "so": "ns"}


def simm(w):
    v = w & 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def dis(w, addr):
    prim = w >> 26
    rD, rA, rB = (w >> 21) & 31, (w >> 16) & 31, (w >> 11) & 31
    if w == 0x4E800020:
        return "blr"
    if w == 0x4E800021:
        return "blrl"
    if w == 0x4C00012C:
        return "isync"
    if prim in PRIM:
        mn, form = PRIM[prim]
        if form == "d":
            if prim == 14 and rA == 0:
                return f"li r{rD}, {simm(w)}"
            if prim == 15 and rA == 0:
                return f"lis r{rD}, 0x{w & 0xFFFF:X}"
            return f"{mn} r{rD}, r{rA}, {simm(w)}"
        if form == "s":
            return f"{mn} r{rA}, r{rD}, 0x{w & 0xFFFF:X}"
        if form == "m":
            return f"{mn} r{rD}, {simm(w)}(r{rA})"
        if form == "f":
            return f"{mn} f{rD}, {simm(w)}(r{rA})"
    if prim == 11:
        return f"cmpwi r{rA}, {simm(w)}"
    if prim == 10:
        return f"cmplwi r{rA}, 0x{w & 0xFFFF:X}"
    if prim == 18:  # b / bl / ba / bla
        off = w & 0x03FFFFFC
        if off >= 0x02000000:
            off -= 0x04000000
        tgt = off if (w & 2) else addr + off
        return f"b{'l' if w & 1 else ''} 0x{tgt & 0xFFFFFFFF:X}"
    if prim == 16:  # conditional branch
        bo, bi = (w >> 21) & 31, (w >> 16) & 31
        off = w & 0xFFFC
        if off >= 0x8000:
            off -= 0x10000
        base = BI_BIT[bi & 3]
        cond = base if (bo & 8) else BI_NEG[base]   # BO bit 3 = branche si vrai
        return f"b{cond} cr{bi >> 2}, 0x{(addr + off) & 0xFFFFFFFF:X}"
    if prim == 19 and ((w >> 1) & 0x3FF) == 16:
        return "bclr"
    if prim == 20:  # rlwimi
        return f"rlwimi r{rA}, r{rD}, {rB}, {(w >> 6) & 31}, {(w >> 1) & 31}"
    if prim == 21:  # rlwinm
        sh, mb, me = rB, (w >> 6) & 31, (w >> 1) & 31
        if mb == 0 and me == 31 - sh:
            return f"slwi r{rA}, r{rD}, {sh}"
        if me == 31 and mb == 32 - sh and sh:
            return f"srwi r{rA}, r{rD}, {32 - sh}"
        return f"rlwinm r{rA}, r{rD}, {sh}, {mb}, {me}"
    if prim == 31:
        xo = (w >> 1) & 0x3FF
        mn = X31.get(xo)
        if mn:
            rc = "." if w & 1 else ""
            if mn in ("cmpw", "cmplw"):
                return f"{mn} r{rA}, r{rB}"
            if mn in ("neg", "extsb", "extsh"):
                return f"{mn}{rc} r{rA}, r{rD}"
            if mn == "or" and rD == rB:
                return f"mr{rc} r{rA}, r{rD}"
            if mn in ("and", "or", "xor", "nor", "nand", "slw", "srw", "sraw", "andc", "orc"):
                return f"{mn}{rc} r{rA}, r{rD}, r{rB}"
            if mn == "srawi":
                return f"srawi{rc} r{rA}, r{rD}, {rB}"
            if mn in ("mfspr", "mtspr"):
                spr = ((w >> 16) & 31) | (((w >> 11) & 31) << 5)
                name = {8: "lr", 9: "ctr", 1: "xer"}.get(spr, f"spr{spr}")
                return f"{'mf' if mn == 'mfspr' else 'mt'}{name} r{rD}"
            return f"{mn}{rc} r{rD}, r{rA}, r{rB}"
    if prim == 63 or prim == 59:  # floating point
        xo = (w >> 1) & 0x3FF
        fmap = {21: "fadd", 20: "fsub", 25: "fmul", 18: "fdiv", 72: "fmr",
                40: "fneg", 264: "fabs", 12: "frsp", 14: "fctiw", 15: "fctiwz"}
        mn = fmap.get(xo, f"fp_xo{xo}")
        p = "s" if prim == 59 else ""
        if mn in ("fmr", "fneg", "fabs", "frsp", "fctiw", "fctiwz"):
            return f"{mn} f{rD}, f{rB}"
        return f"{mn}{p} f{rD}, f{rA}, f{rB}"
    return f".4byte 0x{w:08X}"


def text_section(rel):
    so = struct.unpack('>I', rel[0x10:0x14])[0]
    num = struct.unpack('>I', rel[0xC:0x10])[0]
    for i in range(num):
        o, s = struct.unpack('>II', rel[so + i * 8:so + i * 8 + 8])
        if (o & 1) and s:
            return o & ~3, i
    return None, None


def relocs(rel, tidx):
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
            if cur_sec == tidx:
                out[cur] = (typ, mid, sec, add)
    return out


mod, addr = sys.argv[1], int(sys.argv[2], 16)
size = int(sys.argv[3]) if len(sys.argv) > 3 else 0

if mod == "DOL":
    dol = open(os.path.join(ROOT, "orig/RSBE01_02/sys/main.dol"), "rb").read()
    offs = struct.unpack('>7I', dol[0x00:0x1C])
    addrs = struct.unpack('>7I', dol[0x48:0x64])
    sizes = struct.unpack('>7I', dol[0x90:0xAC])
    code = None
    for o, a, s in zip(offs, addrs, sizes):
        if s and a <= addr < a + s:
            code = dol[o + addr - a:o + addr - a + (size or 256)]
    R = {}
else:
    rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{mod}.rel"), "rb").read()
    toff, tidx = text_section(rel)
    R = relocs(rel, tidx)
    if not size:
        for l in open(os.path.join(ROOT, f"config/RSBE01_02/rels/{mod}/symbols.txt")):
            m = re.match(r'\S+\s*=\s*\.text:0x0*%X;.*size:0x([0-9A-Fa-f]+)' % addr, l)
            if m:
                size = int(m.group(1), 16)
    code = rel[toff + addr:toff + addr + (size or 256)]

for i in range(0, len(code) - 3, 4):
    w = struct.unpack('>I', code[i:i + 4])[0]
    a = addr + i
    note = ""
    if a in R:
        t, mid, sec, add = R[a]
        note = f"   ; reloc t{t} -> mod{mid} sec{sec} +0x{add:X}"
    print(f"  {a:06X}  {w:08X}  {dis(w, a):<34}{note}")

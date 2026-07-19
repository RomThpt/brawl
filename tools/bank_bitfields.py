#!/usr/bin/env python3
"""Auto-decompile C bitfield accessors.

The compiler emits rlwimi/rlwinm for bitfield writes and reads, and the field's
position and width are fully recoverable from the instruction's SH/MB/ME fields.
So the C can be reconstructed exactly: a struct with a padding bitfield to place
the field, then the field itself.

PPC bit numbering has bit 0 = MSB, which is also the order big-endian bitfields
are allocated in, so MB maps straight to the padding width.

Shapes handled (r3 = object, offset OFF):
  lwz r0,OFF(r3) ; rlwimi r0,r4,SH,MB,ME ; stw r0,OFF(r3) ; blr   -> setter
  lwz r0,OFF(r3) ; rlwinm r3,r0,SH,MB,31 ; blr                     -> unsigned getter
  lwz r0,OFF(r3) ; rlwinm r0,r0,SH,MB,ME ; srawi r3,r0,N ; blr     -> signed getter

Usage: python3 tools/bank_bitfields.py <module> [max_functions]
"""
import struct, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_unit_rel

ROOT = add_unit_rel.ROOT
module = sys.argv[1]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 200
LAST = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/last_rel.txt"
BADFILE = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/bad_rel.txt"

rel = open(os.path.join(ROOT, f"orig/RSBE01_02/files/module/{module}.rel"), "rb").read()
sec_off = struct.unpack('>I', rel[0x10:0x14])[0]
num = struct.unpack('>I', rel[0xC:0x10])[0]
textoff = None
for i in range(num):
    o, s = struct.unpack('>II', rel[sec_off + i * 8:sec_off + i * 8 + 8])
    if (o & 1) and s:
        textoff = o & ~3
        break


def w(a, i):
    return struct.unpack('>I', rel[textoff + a + i * 4:textoff + a + i * 4 + 4])[0]


def lwz_off(x, rd, ra):
    """x is `lwz rd, imm(ra)` -> signed imm, else None."""
    if (x >> 26) != 32 or ((x >> 21) & 31) != rd or ((x >> 16) & 31) != ra:
        return None
    v = x & 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def stw_off(x, rs, ra):
    if (x >> 26) != 36 or ((x >> 21) & 31) != rs or ((x >> 16) & 31) != ra:
        return None
    v = x & 0xFFFF
    return v - 0x10000 if v >= 0x8000 else v


def rlw(x, prim):
    """rlwimi(20)/rlwinm(21) -> (rS, rA, SH, MB, ME)."""
    if (x >> 26) != prim:
        return None
    return ((x >> 21) & 31, (x >> 16) & 31, (x >> 11) & 31, (x >> 6) & 31, (x >> 1) & 31)


def struct_for(off, start, width, signed):
    pad = f"    unsigned int p0 : {start};\n" if start else ""
    ty = "int" if signed else "unsigned int"
    return (f"typedef struct {{\n    char pad[{off}];\n{pad}"
            f"    {ty} f : {width};\n}} S;\n\n")


def classify(a, sz):
    if sz == 16:
        w0, w1, w2, w3 = w(a, 0), w(a, 1), w(a, 2), w(a, 3)
        if w3 != 0x4E800020:
            return None
        off = lwz_off(w0, 0, 3)
        if off is None or off < 0:
            return None
        r = rlw(w1, 20)                                    # rlwimi -> setter
        if r and stw_off(w2, 0, 3) == off:
            rS, rA, SH, MB, ME = r
            if rA != 0 or rS != 4 or ME < MB:
                return None
            width = ME - MB + 1
            if SH != (32 - (ME + 1)) % 32:
                return None
            return ("set", off, MB, width, False)
        r = rlw(w1, 21)                                    # rlwinm + srawi -> signed get
        if r and (w2 >> 26) == 31 and ((w2 >> 1) & 0x3FF) == 824:
            rS, rA, SH, MB, ME = r
            if rS != 0 or rA != 0 or ((w2 >> 21) & 31) != 3 or ((w2 >> 16) & 31) != 0:
                return None
            n = (w2 >> 11) & 31
            width = 32 - n
            if width <= 0 or ME != MB + width:
                return None
            return ("get", off, (MB + SH) % 32, width, True)
        return None
    if sz == 12:
        w0, w1, w2 = w(a, 0), w(a, 1), w(a, 2)
        if w2 != 0x4E800020:
            return None
        off = lwz_off(w0, 0, 3)
        if off is None or off < 0:
            return None
        r = rlw(w1, 21)                                    # rlwinm -> unsigned get
        if not r:
            return None
        rS, rA, SH, MB, ME = r
        if rS != 0 or rA != 3 or ME != 31:
            return None
        return ("get", off, (MB + SH) % 32, 32 - MB, False)
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
    if isd(a) or a in bad or not re.match(r'^[A-Za-z_]\w*$', n):
        continue
    if banked >= maxf:
        break
    c = classify(a, sz)
    if not c:
        continue
    kind, off, start, width, signed = c
    if start + width > 32 or width <= 0:
        continue
    src = struct_for(off, start, width, signed)
    if kind == "set":
        src += f"void {n}(S* p, int v) {{\n    p->f = v;\n}}\n"
    else:
        ty = "int" if signed else "unsigned int"
        src += f"{ty} {n}(S* p) {{\n    return p->f;\n}}\n"
    add_unit_rel.add(module, f"mo_stub/{module}/bf_{n}.c", a, a + sz, src)
    addrs.append(f"{module}:{a:08X}")
    banked += 1

open(LAST, "w").write("\n".join(addrs) + "\n")
print(f"[{module}] banked {banked} bitfield accessors")

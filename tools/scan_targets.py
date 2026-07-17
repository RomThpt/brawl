import json, itertools, subprocess, os

ROOT = "/private/tmp/claude-501/-Users-romt/acb283f2-d321-48f9-955d-3b2312329564/scratchpad/brawl"
CLI = os.path.join(ROOT, "build/tools/objdiff-cli")

UNITS = [
    "main/sora/ac/ac_cmd_interpreter",
    "main/sora/gf/gf_slow_manager",
    "main/sora/ut/ut_relocate",
    "main/sora/ty/ty_fig_listmng",
    "main/sora/gf/gf_task_scheduler",
    "st_emblem/mo_stage/st_emblem/st_emblem",
    "sora_scene/mo_scene/sora_scene/sc_adv_gameover",
    "main/sora/ip/ip_network_producer",
    "main/sora/cm/cm_controller_menu_fixed",
]

def allsyms(side):
    out = []
    def rec(o):
        if isinstance(o, dict):
            if 'name' in o and 'instructions' in o and 'match_percent' in o:
                out.append(o)
            for v in o.values(): rec(v)
        elif isinstance(o, list):
            for v in o: rec(v)
    rec(side); return out

def ins_parts(x):
    ins = x.get('instruction', {})
    fmt = ins.get('formatted', '')
    mnem = fmt.split()[0] if fmt else ''
    # non-register tokens: labels/relocs/symbols
    toks = fmt.replace(',', ' ').split()[1:]
    labels = [t for t in toks if ('@' in t or 'lbl_' in t or t.startswith('__') or 'data' in t)]
    return fmt, mnem, labels

REGS = set(f"r{i}" for i in range(32)) | set(f"f{i}" for i in range(32))

def classify(li, ri):
    diffs = [(l, r) for l, r in itertools.zip_longest(li, ri, fillvalue=(None,)*3) if l[0] != r[0]]
    if len(li) != len(ri):
        return "STRUCT", len(diffs)
    only_reg = True
    data_related = False
    for l, r in diffs:
        if l[1] != r[1]:            # different mnemonic
            only_reg = False
        if l[2] != r[2]:            # different labels/relocs
            data_related = True
    if data_related:
        return "DATA", len(diffs)
    if only_reg:
        return "REGSWAP", len(diffs)
    return "STRUCT", len(diffs)

rows = []
for u in UNITS:
    out = "/tmp/scan_" + u.replace("/", "_") + ".json"
    subprocess.run([CLI, "diff", "-p", ROOT, "-u", u, "-o", out, "--format", "json"],
                   capture_output=True, text=True)
    if not os.path.exists(out):
        continue
    d = json.load(open(out))
    L = {s['name']: s for s in allsyms(d['left'])}
    R = {s['name']: s for s in allsyms(d['right'])}
    for name, rs in R.items():
        mp = rs.get('match_percent', 100)
        if mp >= 100:
            continue
        ls = L.get(name)
        li = [ins_parts(x) for x in ls['instructions']] if ls else []
        ri = [ins_parts(x) for x in rs['instructions']]
        kind, nd = classify(li, ri)
        rows.append((kind, nd, round(mp, 2), int(rs.get('size', 0)), rs.get('demangled_name', name)[:44], u.split('/')[-1]))

# crackable first: STRUCT, small #diffs
order = {"STRUCT": 0, "REGSWAP": 1, "DATA": 2}
rows.sort(key=lambda x: (order[x[0]], x[1]))
print(f"{'TYPE':8}{'#d':>4}{'match%':>8}{'size':>6}  fonction")
print("-" * 78)
for kind, nd, mp, sz, dn, unit in rows:
    print(f"{kind:8}{nd:>4}{mp:>7.2f}%{sz:>6}  {dn:46}[{unit}]")
print(f"\nTotal non-matché: {len(rows)} fonctions | STRUCT(crackables): {sum(1 for r in rows if r[0]=='STRUCT')}")

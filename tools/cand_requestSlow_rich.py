import itertools, random

FILE = "src/sora/gf/gf_slow_manager.cpp"
OBJ = "build/RSBE01_02/src/sora/gf/gf_slow_manager.o"
UNIT = "main/sora/gf/gf_slow_manager"
SYMBOL = "requestSlow__13gfSlowManagerFUc"

ORIGINAL = """u32 gfSlowManager::requestSlow(u8 rate) {
    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {
        curr = &reqs[i];
        if (curr->m_state == StateInactive) {
            res = i;
            s_needsUpdate = true;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
    }
    return static_cast<u32>(res) << 24;
}"""

def gen(res_type, access, state_temp, cmp_order, body_order, ret_style, loop):
    # element accessor 'E.' (member access prefix) and any per-iteration setup line
    pre = []          # lines before the loop (after res decl)
    itersetup = []    # lines at top of loop body
    iterend = []      # lines at end of loop body (before '}')
    if access == "curr_amp":
        pre += ["SlowRequest* reqs = s_gfSlowManager.m_reqs;", "SlowRequest* curr;"]
        itersetup += ["curr = &reqs[i];"]
        E = "curr->"
    elif access == "curr_add":
        pre += ["SlowRequest* reqs = s_gfSlowManager.m_reqs;", "SlowRequest* curr;"]
        itersetup += ["curr = reqs + i;"]
        E = "curr->"
    elif access == "inline":
        E = "s_gfSlowManager.m_reqs[i]."
    elif access == "ptrwalk":
        pre += ["SlowRequest* curr = s_gfSlowManager.m_reqs;"]
        E = "curr->"
        iterend += ["curr++;"]
    elif access == "ref":
        itersetup += ["SlowRequest& c = s_gfSlowManager.m_reqs[i];"]
        E = "c."

    # optional temp for the loaded state
    cmp_lhs = E + "m_state"
    if state_temp == "u8":
        itersetup2 = ["u8 st = " + E + "m_state;"]; cmp_lhs = "st"
    elif state_temp == "u32":
        itersetup2 = ["u32 st = " + E + "m_state;"]; cmp_lhs = "st"
    elif state_temp == "ref":
        itersetup2 = ["const u8& st = " + E + "m_state;"]; cmp_lhs = "st"
    else:
        itersetup2 = []

    cmp = (cmp_lhs + " == StateInactive") if cmp_order == "a" else ("StateInactive == " + cmp_lhs)

    stmts = {
        "res":   "res = i;",
        "need":  "s_needsUpdate = true;",
        "state": E + "m_state = StateActive;",
        "rate":  E + "m_slowRate = rate;",
    }
    body = [stmts[k] for k in body_order] + ["break;"]

    if ret_style == "cast":
        ret = "return static_cast<u32>(res) << 24;"
    elif ret_style == "temp":
        ret = "u32 ret = res;\n    return ret << 24;"
    else:
        ret = "return ((u32)res << 24);"

    # loop header/footer
    if loop == "for8":
        lh, cnt_decl = "for (u8 i = 0; i < NRequests; i++) {", ""
    elif loop == "for32":
        lh, cnt_decl = "for (u32 i = 0; i < NRequests; i++) {", ""
    else:  # while8
        lh, cnt_decl = "while (i < NRequests) {", "u8 i = 0;"
        iterend = iterend + ["i++;"]

    L = []
    L.append("u32 gfSlowManager::requestSlow(u8 rate) {")
    L.append("    " + res_type + " res = 0xFF;")
    for p in pre: L.append("    " + p)
    if cnt_decl: L.append("    " + cnt_decl)
    L.append("    " + lh)
    for s in itersetup: L.append("        " + s)
    for s in itersetup2: L.append("        " + s)
    L.append("        if (" + cmp + ") {")
    for b in body: L.append("            " + b)
    L.append("        }")
    for s in iterend: L.append("        " + s)
    L.append("    }")
    L.append("    " + ret)
    L.append("}")
    return "\n".join(L)

RES = ["u8", "u32", "s32", "int"]
ACCESS = ["curr_amp", "curr_add", "inline", "ptrwalk", "ref"]
STEMP = ["none", "u8", "u32", "ref"]
CMP = ["a", "b"]
RET = ["cast", "temp", "cstyle"]
LOOP = ["for8", "for32", "while8"]
# a representative subset of the 24 body orders (res must stay meaningful anywhere)
BODY = [
    ("res", "need", "state", "rate"),
    ("need", "res", "state", "rate"),
    ("state", "rate", "need", "res"),
    ("need", "state", "rate", "res"),
    ("res", "state", "rate", "need"),
    ("rate", "state", "need", "res"),
]

rng = random.Random(1234)
all_combos = list(itertools.product(RES, ACCESS, STEMP, CMP, BODY, RET, LOOP))
rng.shuffle(all_combos)

CANDIDATES = []
seen = set()
for res_type, access, stemp, cmp_order, body_order, ret_style, loop in all_combos:
    txt = gen(res_type, access, stemp, cmp_order, body_order, ret_style, loop)
    if txt in seen:
        continue
    seen.add(txt)
    name = f"{res_type[:3]}_{access[:4]}_{stemp[:3]}_{cmp_order}_{ret_style[:3]}_{loop}_{''.join(x[0] for x in body_order)}"
    CANDIDATES.append((name, txt))
    if len(CANDIDATES) >= 600:
        break

import itertools

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

# The 4 independent statements inside the `if` block (order permuted).
STMTS = {
    "res":   "res = i;",
    "need":  "s_needsUpdate = true;",
    "state": "curr->m_state = StateActive;",
    "rate":  "curr->m_slowRate = rate;",
}
# access forms for reading/writing the current request
# (obj expr used for m_state/m_slowRate; 'curr' variant needs the curr assignment)

def build_variant(res_type, cmp_order, ret_style, body_order):
    # comparison
    cmp = "curr->m_state == StateInactive" if cmp_order == "a" else "StateInactive == curr->m_state"
    # if-body statements in chosen order
    body = "\n".join("            " + STMTS[k] for k in body_order)
    # return
    if ret_style == "cast":
        ret = "    return static_cast<u32>(res) << 24;"
    elif ret_style == "cstyle":
        ret = "    return (u32)res << 24;"
    else:  # temp
        ret = "    u32 ret = res;\n    return ret << 24;"
    return f"""u32 gfSlowManager::requestSlow(u8 rate) {{
    {res_type} res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {{
        curr = &reqs[i];
        if ({cmp}) {{
{body}
            break;
        }}
    }}
{ret}
}}"""

CANDIDATES = []
seen = set()
# res assignment must come before break; all 4 stmts present; permute the 4.
for res_type in ["u8", "u32", "s32", "int"]:
    for cmp_order in ["a", "b"]:
        for ret_style in ["cast", "cstyle", "temp"]:
            for body_order in itertools.permutations(["res", "need", "state", "rate"]):
                txt = build_variant(res_type, cmp_order, ret_style, body_order)
                if txt in seen:
                    continue
                seen.add(txt)
                name = f"{res_type}_{cmp_order}_{ret_style}_{''.join(x[0] for x in body_order)}"
                CANDIDATES.append((name, txt))

# cap to keep the run bounded (~ a few hundred)
CANDIDATES = CANDIDATES[:240]

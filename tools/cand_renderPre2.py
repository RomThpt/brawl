import itertools

FILE = "src/sora/gf/gf_task_scheduler.cpp"
OBJ = "build/RSBE01_02/src/sora/gf/gf_task_scheduler.o"
UNIT = "main/sora/gf/gf_task_scheduler"
SYMBOL = "renderPre__15gfTaskSchedulerFv"

ORIGINAL = """void gfTaskScheduler::renderPre() {
    gfTask* next;
    gfTask* r3;
    unk0_1 = 2;
    for (s32 i = 0; i < unkF8Size; i++) {
        r3 = unkF8[i];
        unk6 = i;
        for (gfTask* task = r3; task; task = next) {
            next = task->m_0x18;
            if (task->m_alive && task->unk2C_b2) {
                task->renderPre();
            }
        }
    }
}"""

INNER_BODY = """            if (task->m_alive && task->unk2C_b2) {
                task->renderPre();
            }"""

def gen(decls, unk0_pos, setup_order, inner_init, next_pos, loopform):
    L = ["void gfTaskScheduler::renderPre() {"]
    # declarations block
    declmap = {
        "next_r3": ["    gfTask* next;", "    gfTask* r3;"],
        "r3_next": ["    gfTask* r3;", "    gfTask* next;"],
        "next_only": ["    gfTask* next;"],
    }
    unk0 = "    unk0_1 = 2;"
    dblock = declmap[decls]
    if unk0_pos == "after":
        L += dblock + [unk0]
    elif unk0_pos == "before":
        L += [unk0] + dblock
    else:  # mid (only meaningful with 2 decls)
        L += [dblock[0], unk0] + dblock[1:]

    L.append("    for (s32 i = 0; i < unkF8Size; i++) {")
    # inner setup: r3 assignment + unk6
    setup = {
        "r3_unk6": ["        r3 = unkF8[i];", "        unk6 = i;"],
        "unk6_r3": ["        unk6 = i;", "        r3 = unkF8[i];"],
    }
    if inner_init == "inline":
        # no r3, iterate from unkF8[i] directly
        L += ["        unk6 = i;"]
        init_expr = "unkF8[i]"
    else:
        L += setup[setup_order]
        init_expr = "r3"

    # inner loop
    if loopform == "for":
        L.append(f"        for (gfTask* task = {init_expr}; task; task = next) {{")
        if next_pos == "first":
            L.append("            next = task->m_0x18;")
            L.append(INNER_BODY)
        else:
            L.append(INNER_BODY)
            L.append("            next = task->m_0x18;")
        L.append("        }")
    else:  # while
        L.append(f"        gfTask* task = {init_expr};")
        L.append("        while (task) {")
        L.append("            next = task->m_0x18;")
        L.append(INNER_BODY)
        L.append("            task = next;")
        L.append("        }")
    L.append("    }")
    L.append("}")
    return "\n".join(L)

CANDIDATES = []
seen = set()
for decls in ["next_r3", "r3_next", "next_only"]:
    for unk0_pos in ["after", "before", "mid"]:
        if decls == "next_only" and unk0_pos == "mid":
            continue
        for setup_order in ["r3_unk6", "unk6_r3"]:
            for inner_init in ["r3", "inline"]:
                if inner_init == "inline" and decls != "next_only":
                    continue
                if inner_init == "r3" and decls == "next_only":
                    continue
                for next_pos in ["first", "last"]:
                    for loopform in ["for", "while"]:
                        txt = gen(decls, unk0_pos, setup_order, inner_init, next_pos, loopform)
                        if txt in seen:
                            continue
                        seen.add(txt)
                        name = f"{decls}_{unk0_pos}_{setup_order}_{inner_init}_{next_pos}_{loopform}"
                        CANDIDATES.append((name, txt))

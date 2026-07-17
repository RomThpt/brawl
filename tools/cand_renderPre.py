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

def mk(decls, top_order, inner):
    return f"""void gfTaskScheduler::renderPre() {{
{decls}
    for (s32 i = 0; i < unkF8Size; i++) {{
{top_order}
{inner}
    }}
}}"""

INNER_R3 = """        for (gfTask* task = r3; task; task = next) {
            next = task->m_0x18;
            if (task->m_alive && task->unk2C_b2) {
                task->renderPre();
            }
        }"""
INNER_INLINE = """        for (gfTask* task = unkF8[i]; task; task = next) {
            next = task->m_0x18;
            if (task->m_alive && task->unk2C_b2) {
                task->renderPre();
            }
        }"""

CANDIDATES = []
seen = set()
decl_variants = {
    "next_r3": "    gfTask* next;\n    gfTask* r3;\n    unk0_1 = 2;",
    "r3_next": "    gfTask* r3;\n    gfTask* next;\n    unk0_1 = 2;",
    "unk_first": "    unk0_1 = 2;\n    gfTask* next;\n    gfTask* r3;",
    "next_only": "    gfTask* next;\n    unk0_1 = 2;",  # for inline
}
top_variants = {
    "r3_unk6": "        r3 = unkF8[i];\n        unk6 = i;",
    "unk6_r3": "        unk6 = i;\n        r3 = unkF8[i];",
    "unk6_only": "        unk6 = i;",  # for inline
}
# with r3
for dn in ["next_r3", "r3_next", "unk_first"]:
    for tn in ["r3_unk6", "unk6_r3"]:
        txt = mk(decl_variants[dn], top_variants[tn], INNER_R3)
        name = f"r3_{dn}_{tn}"
        if txt not in seen:
            seen.add(txt); CANDIDATES.append((name, txt))
# inline r3 (no r3 decl)
for dn in ["next_only"]:
    for tn in ["unk6_only"]:
        txt = mk(decl_variants[dn], top_variants[tn], INNER_INLINE)
        name = f"inline_{dn}_{tn}"
        if txt not in seen:
            seen.add(txt); CANDIDATES.append((name, txt))

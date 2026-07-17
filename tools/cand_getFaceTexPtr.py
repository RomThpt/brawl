import itertools

FILE = "src/mo_enemy/sora_enemy/em_external_value_accesser.cpp"
OBJ = "build/RSBE01_02/src/mo_enemy/sora_enemy/em_external_value_accesser.o"
UNIT = "sora_enemy/mo_enemy/sora_enemy/em_external_value_accesser"
SYMBOL = "getFaceTexPtr__23emExternalValueAccesserFP5EnemyUl"

ORIGINAL = """nw4r::g3d::ResFileData* emExternalValueAccesser::getFaceTexPtr(Enemy* em, u32 taskId) {
    if (taskId == -1 || taskId == em->m_taskId) {
        return em->getFaceTexPtr();
    }

    const wnemSimple* wn = emWeaponManager::getInstance()->GetManagedWeaponFromTaskID(taskId);
    return (!wn) ? em->getFaceTexPtr() : em->getFaceTexPtr(wn->unk21EC);
}"""

HEAD = """nw4r::g3d::ResFileData* emExternalValueAccesser::getFaceTexPtr(Enemy* em, u32 taskId) {
    if (taskId == -1 || taskId == em->m_taskId) {
        return em->getFaceTexPtr();
    }
"""

def wn_decl(constness, wntype):
    c = "const " if constness else ""
    return f"    {c}wnemSimple* wn = emWeaponManager::getInstance()->GetManagedWeaponFromTaskID(taskId);"

def cond(nullstyle):
    return {"bang": "!wn", "eqnull": "wn == NULL", "eqzero": "wn == 0"}[nullstyle]

def condpos(nullstyle):
    return {"bang": "wn", "eqnull": "wn != NULL", "eqzero": "wn != 0"}[nullstyle]

def argexpr(argstyle):
    # returns (pre_lines, expr) for the wn->unk21EC argument
    if argstyle == "inline":
        return [], "wn->unk21EC"
    if argstyle == "tmp_u32":
        return ["    u32 v = wn->unk21EC;"], "v"
    if argstyle == "tmp_ul":
        return ["    unsigned long v = wn->unk21EC;"], "v"
    if argstyle == "tmp_ref":
        return ["    const u32& v = wn->unk21EC;"], "v"

CANDIDATES = []
seen = set()
for constness in [True, False]:
    for nullstyle in ["bang", "eqnull", "eqzero"]:
        for argstyle in ["inline", "tmp_u32", "tmp_ul", "tmp_ref"]:
            for structure in ["ternary", "ifA", "ifB"]:
                decl = wn_decl(constness, None)
                pre, aexpr = argexpr(argstyle)
                call_b = f"em->getFaceTexPtr({aexpr})"
                call_a = "em->getFaceTexPtr()"
                if structure == "ternary":
                    # ternary can't easily host a pre-line temp; only for inline
                    if pre:
                        continue
                    body = f"    return ({cond(nullstyle)}) ? {call_a} : {call_b};"
                elif structure == "ifA":
                    body = f"    if ({cond(nullstyle)}) {{\n        return {call_a};\n    }}\n" + \
                           ("\n".join(pre) + ("\n" if pre else "")) + f"    return {call_b};"
                else:  # ifB
                    body = f"    if ({condpos(nullstyle)}) {{\n" + \
                           ("\n".join("    " + p.strip() for p in pre) + ("\n" if pre else "")) + \
                           f"        return {call_b};\n    }}\n    return {call_a};"
                txt = HEAD + decl + "\n" + body + "\n}"
                if txt in seen:
                    continue
                seen.add(txt)
                name = f"{'c' if constness else 'm'}_{nullstyle}_{argstyle}_{structure}"
                CANDIDATES.append((name, txt))

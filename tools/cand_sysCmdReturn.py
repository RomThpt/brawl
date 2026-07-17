import itertools

FILE = "src/sora/ac/ac_cmd_interpreter.cpp"
OBJ = "build/RSBE01_02/src/sora/ac/ac_cmd_interpreter.o"
UNIT = "main/sora/ac/ac_cmd_interpreter"
SYMBOL = "systemCmdFuncReturn__16acCmdInterpreterFv"

ORIGINAL = """void acCmdInterpreter::systemCmdFuncReturn() {
    const s32 i = getIdxOfStackData(acCmdInterpreterStackData::ReturnAddress);
    if (i < 0) {
        m_currentCmd = 0;
        m_stack->clear();
        m_dontAdvance = false;
    } else {
        const acAnimCmdConv* returnAddr = m_stack->at(i).addressData;
        if (returnAddr) {
            m_currentCmd = returnAddr;
        }
        popStackToSize(i);
    }
}"""

def elsebranch(ra_style):
    if ra_style == "temp":
        return """        const acAnimCmdConv* returnAddr = m_stack->at(i).addressData;
        if (returnAddr) {
            m_currentCmd = returnAddr;
        }
        popStackToSize(i);"""
    else:  # nontemp/inline
        return """        acAnimCmdConv* returnAddr = m_stack->at(i).addressData;
        if (returnAddr) {
            m_currentCmd = returnAddr;
        }
        popStackToSize(i);"""

def ifbranch(order):
    stmts = {
        "cmd": "        m_currentCmd = 0;",
        "clr": "        m_stack->clear();",
        "adv": "        m_dontAdvance = false;",
    }
    return "\n".join(stmts[k] for k in order)

def mk(itype, structure, if_order, ra_style):
    decl = f"    {itype} i = getIdxOfStackData(acCmdInterpreterStackData::ReturnAddress);"
    ib = ifbranch(if_order)
    eb = elsebranch(ra_style)
    if structure == "ifelse":
        body = f"    if (i < 0) {{\n{ib}\n    }} else {{\n{eb}\n    }}"
    elif structure == "flip":
        body = f"    if (i >= 0) {{\n{eb}\n    }} else {{\n{ib}\n    }}"
    else:  # early
        body = f"    if (i < 0) {{\n{ib}\n        return;\n    }}\n{eb}"
    return f"void acCmdInterpreter::systemCmdFuncReturn() {{\n{decl}\n{body}\n}}"

CANDIDATES = []
seen = set()
for itype in ["const s32", "s32", "const int", "int"]:
    for structure in ["ifelse", "flip", "early"]:
        for if_order in [("cmd", "clr", "adv"), ("clr", "cmd", "adv"), ("cmd", "adv", "clr")]:
            for ra_style in ["temp", "nontemp"]:
                txt = mk(itype, structure, if_order, ra_style)
                if txt in seen:
                    continue
                seen.add(txt)
                name = f"{itype.replace(' ','')}_{structure}_{''.join(x[0] for x in if_order)}_{ra_style}"
                CANDIDATES.append((name, txt))

import itertools

FILE = "src/sora/gf/gf_task_scheduler.cpp"
OBJ = "build/RSBE01_02/src/sora/gf/gf_task_scheduler.o"
UNIT = "main/sora/gf/gf_task_scheduler"
SYMBOL = "changeTaskPriorityRequest__15gfTaskSchedulerFUlUc"

ORIGINAL = """void gfTaskScheduler::changeTaskPriorityRequest(u32 id, u8 priority) {
    gfTask* task = getTask(id);
    if (task) {
        UnkTaskRequest x(false);
        x.m_category = task->m_taskCategory;
        x.m_taskId = task->m_taskId;
        x.m_priority = priority;
        m_pendingPrioUpdates[m_numPendingPrioUpdates] = x;
        m_numPendingPrioUpdates++;
    }
}"""

FIELDS = {
    "cat":  "x.m_category = task->m_taskCategory;",
    "id":   "x.m_taskId = task->m_taskId;",
    "prio": "x.m_priority = priority;",
}

def mk(field_order, store_style, task_guard):
    fields = "\n".join("        " + FIELDS[k] for k in field_order)
    if store_style == "sep":
        store = """        m_pendingPrioUpdates[m_numPendingPrioUpdates] = x;
        m_numPendingPrioUpdates++;"""
    elif store_style == "post":
        store = "        m_pendingPrioUpdates[m_numPendingPrioUpdates++] = x;"
    else:  # temp index
        store = """        int n = m_numPendingPrioUpdates;
        m_pendingPrioUpdates[n] = x;
        m_numPendingPrioUpdates = n + 1;"""
    if task_guard == "if":
        head = """    gfTask* task = getTask(id);
    if (task) {"""
    else:  # early return
        head = """    gfTask* task = getTask(id);
    if (!task) {
        return;
    }
    {"""
    return f"""void gfTaskScheduler::changeTaskPriorityRequest(u32 id, u8 priority) {{
{head}
        UnkTaskRequest x(false);
{fields}
{store}
    }}
}}"""

CANDIDATES = []
seen = set()
for field_order in itertools.permutations(["cat", "id", "prio"]):
    for store_style in ["sep", "post", "temp"]:
        for task_guard in ["if", "early"]:
            txt = mk(field_order, store_style, task_guard)
            if txt in seen:
                continue
            seen.add(txt)
            name = f"{'_'.join(field_order)}_{store_style}_{task_guard}"
            CANDIDATES.append((name, txt))

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

def mk(body):
    return "u32 gfSlowManager::requestSlow(u8 rate) {\n" + body + "\n}"

CANDIDATES = [
    ("res_u32", mk("""    u32 res = 0xFF;
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
    return res << 24;""")),

    ("res_int", mk("""    int res = 0xFF;
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
    return static_cast<u32>(res) << 24;""")),

    ("cmp_swapped", mk("""    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {
        curr = &reqs[i];
        if (StateInactive == curr->m_state) {
            res = i;
            s_needsUpdate = true;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
    }
    return static_cast<u32>(res) << 24;""")),

    ("decl_res_last", mk("""    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    u8 res = 0xFF;
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
    return static_cast<u32>(res) << 24;""")),

    ("ptr_iter", mk("""    u8 res = 0xFF;
    SlowRequest* curr = s_gfSlowManager.m_reqs;
    for (u8 i = 0; i < NRequests; i++) {
        if (curr->m_state == StateInactive) {
            res = i;
            s_needsUpdate = true;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
        curr++;
    }
    return static_cast<u32>(res) << 24;""")),

    ("inline_array", mk("""    u8 res = 0xFF;
    for (u8 i = 0; i < NRequests; i++) {
        if (s_gfSlowManager.m_reqs[i].m_state == StateInactive) {
            res = i;
            s_needsUpdate = true;
            s_gfSlowManager.m_reqs[i].m_state = StateActive;
            s_gfSlowManager.m_reqs[i].m_slowRate = rate;
            break;
        }
    }
    return static_cast<u32>(res) << 24;""")),

    ("while_loop", mk("""    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    u8 i = 0;
    while (i < NRequests) {
        curr = &reqs[i];
        if (curr->m_state == StateInactive) {
            res = i;
            s_needsUpdate = true;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
        i++;
    }
    return static_cast<u32>(res) << 24;""")),

    ("ret_temp", mk("""    u8 res = 0xFF;
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
    u32 ret = res;
    return ret << 24;""")),

    ("res_assign_i_cast", mk("""    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {
        curr = &reqs[i];
        if (curr->m_state == StateInactive) {
            res = (u8)i;
            s_needsUpdate = true;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
    }
    return static_cast<u32>(res) << 24;""")),

    ("state_temp_u8", mk("""    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {
        curr = &reqs[i];
        u8 st = curr->m_state;
        if (st == StateInactive) {
            res = i;
            s_needsUpdate = true;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
    }
    return static_cast<u32>(res) << 24;""")),

    ("reorder_needs_first", mk("""    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {
        curr = &reqs[i];
        if (curr->m_state == StateInactive) {
            s_needsUpdate = true;
            res = i;
            curr->m_state = StateActive;
            curr->m_slowRate = rate;
            break;
        }
    }
    return static_cast<u32>(res) << 24;""")),

    ("res_s32", mk("""    s32 res = 0xFF;
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
    return static_cast<u32>(res) << 24;""")),

    ("slowrate_before_state", mk("""    u8 res = 0xFF;
    SlowRequest* reqs = s_gfSlowManager.m_reqs;
    SlowRequest* curr;
    for (u8 i = 0; i < NRequests; i++) {
        curr = &reqs[i];
        if (curr->m_state == StateInactive) {
            res = i;
            s_needsUpdate = true;
            curr->m_slowRate = rate;
            curr->m_state = StateActive;
            break;
        }
    }
    return static_cast<u32>(res) << 24;""")),
]

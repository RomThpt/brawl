extern void __dl__FPv(void* p);

void* __dt__18soTargetSearchUnitFv(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

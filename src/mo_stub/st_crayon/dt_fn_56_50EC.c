extern void __dl__FPv(void* p);

void* fn_56_50EC(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

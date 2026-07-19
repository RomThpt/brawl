extern void __dl__FPv(void* p);

void* fn_10_3F4(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

extern void __dl__FPv(void* p);

void* fn_32_2E4(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

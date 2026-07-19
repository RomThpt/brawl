extern void __dl__FPv(void* p);

void* fn_40_2811C(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

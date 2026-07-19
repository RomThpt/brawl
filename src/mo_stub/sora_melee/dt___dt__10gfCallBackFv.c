extern void __dl__FPv(void* p);

void* __dt__10gfCallBackFv(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

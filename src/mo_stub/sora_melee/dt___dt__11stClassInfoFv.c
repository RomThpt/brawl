extern void __dl__FPv(void* p);

void* __dt__11stClassInfoFv(void* p, int flag) {
    if (p) {
        if (flag > 0) {
            __dl__FPv(p);
        }
    }
    return p;
}

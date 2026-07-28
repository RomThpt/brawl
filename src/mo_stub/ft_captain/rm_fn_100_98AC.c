void fn_100_98AC(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] |= val;
}

void fn_105_DCDC(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] |= val;
}

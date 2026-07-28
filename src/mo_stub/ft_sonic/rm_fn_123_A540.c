void fn_123_A540(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 12))[i] -= val;
}

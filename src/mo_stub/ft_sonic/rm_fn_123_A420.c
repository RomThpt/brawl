void fn_123_A420(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] |= val;
}

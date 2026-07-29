int fn_123_141FC(void* p, int d, int i) {
    return *(int*)((char*)p + (i - *(int*)((char*)p + 24)) * 4 + 76);
}

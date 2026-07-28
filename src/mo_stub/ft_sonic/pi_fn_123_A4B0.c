void fn_123_A4B0(void* p, int i, float v) {
    ((float*)*(void**)((char*)p + 20))[i] = v;
}

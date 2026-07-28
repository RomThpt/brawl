void fn_123_A498(void* p, float val, int i) {
    ((float*)*(void**)((char*)p + 20))[i] += val;
}

void fn_123_A480(void* p, float val, int i) {
    ((float*)*(void**)((char*)p + 20))[i] -= val;
}

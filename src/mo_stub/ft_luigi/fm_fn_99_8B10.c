void fn_99_8B10(void* p, float val, int i) {
    ((float*)*(void**)((char*)p + 20))[i] -= val;
}

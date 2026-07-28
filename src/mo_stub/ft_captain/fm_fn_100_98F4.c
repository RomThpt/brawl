void fn_100_98F4(void* p, float val, int i) {
    ((float*)*(void**)((char*)p + 20))[i] *= val;
}

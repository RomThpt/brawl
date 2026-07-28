void fn_100_990C(void* p, float val, int i) {
    ((float*)*(void**)((char*)p + 20))[i] -= val;
}

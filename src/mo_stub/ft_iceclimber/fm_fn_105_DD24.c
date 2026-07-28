void fn_105_DD24(void* p, float val, int i) {
    ((float*)*(void**)((char*)p + 20))[i] *= val;
}

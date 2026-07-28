void fn_105_DCB0(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] &= ~val;
}

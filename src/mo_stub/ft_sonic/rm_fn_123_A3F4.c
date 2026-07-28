void fn_123_A3F4(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] &= ~val;
}

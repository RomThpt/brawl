void fn_100_99CC(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 12))[i] -= val;
}

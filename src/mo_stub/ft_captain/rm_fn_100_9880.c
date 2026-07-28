void fn_100_9880(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] &= ~val;
}

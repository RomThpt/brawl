void fn_101_D380(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] &= ~val;
}

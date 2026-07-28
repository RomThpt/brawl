void fn_121_B224(void* p, int val, int i) {
    ((int*)*(void**)((char*)p + 28))[i] &= ~val;
}

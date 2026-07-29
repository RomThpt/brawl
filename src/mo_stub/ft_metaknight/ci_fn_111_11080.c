int fn_111_11080(void* p, int d, int i) {
    return *(int*)((char*)p + (i - *(int*)((char*)p + 24)) * 4 + 36);
}

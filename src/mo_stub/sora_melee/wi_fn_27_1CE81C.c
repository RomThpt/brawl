void* fn_27_1CE81C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 25) + i;
    if (idx >= 32) idx -= 32;
    return (char*)p + idx * 12 + 28;
}

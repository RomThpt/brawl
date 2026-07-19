void* fn_27_1D0378(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 32) idx -= 32;
    return (char*)p + idx * 12 + 12;
}

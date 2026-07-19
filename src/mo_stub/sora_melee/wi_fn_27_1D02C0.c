void* fn_27_1D02C0(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 40) idx -= 40;
    return (char*)p + idx * 12 + 12;
}

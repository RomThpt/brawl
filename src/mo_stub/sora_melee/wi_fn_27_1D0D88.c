void* fn_27_1D0D88(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 16) idx -= 16;
    return (char*)p + idx * 12 + 12;
}

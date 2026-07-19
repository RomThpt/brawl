void* fn_27_1D0430(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 5) idx -= 5;
    return (char*)p + idx * 12 + 12;
}

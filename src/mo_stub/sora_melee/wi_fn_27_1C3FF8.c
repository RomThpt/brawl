void* fn_27_1C3FF8(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 29) + i;
    if (idx >= 2) idx -= 2;
    return (char*)p + idx * 12 + 28;
}

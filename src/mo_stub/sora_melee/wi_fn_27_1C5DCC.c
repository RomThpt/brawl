void* fn_27_1C5DCC(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 25) + i;
    if (idx >= 40) idx -= 40;
    return (char*)p + idx * 12 + 28;
}

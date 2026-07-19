void* fn_27_1AFCC4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 305) idx -= 305;
    return (char*)p + idx * 4 + 12;
}

void* fn_96_1E2D4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 4) idx -= 4;
    return (char*)p + idx * 96 + 12;
}

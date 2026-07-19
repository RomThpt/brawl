void* fn_27_FE2A4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 19) idx -= 19;
    return (char*)p + idx * 8 + 12;
}

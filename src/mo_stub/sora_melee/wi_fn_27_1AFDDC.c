void* fn_27_1AFDDC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 290) idx -= 290;
    return (char*)p + idx * 4 + 12;
}

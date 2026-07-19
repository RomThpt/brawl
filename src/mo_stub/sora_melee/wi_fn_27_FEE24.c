void* fn_27_FEE24(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 23) idx -= 23;
    return (char*)p + idx * 12 + 12;
}

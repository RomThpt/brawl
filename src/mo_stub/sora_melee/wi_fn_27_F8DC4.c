void* fn_27_F8DC4(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 23) idx -= 23;
    return (char*)p + idx * 12 + 28;
}

void* fn_27_292BA4(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 29) + i;
    if (idx >= 2) idx -= 2;
    return (char*)p + idx * 12 + 28;
}

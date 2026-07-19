void* fn_27_D9520(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 24) idx -= 24;
    return (char*)p + idx * 48 + 12;
}

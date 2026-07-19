void* fn_27_124E24(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 16) idx -= 16;
    return (char*)p + idx * 24 + 12;
}

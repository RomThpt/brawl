void* fn_40_1E490(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 24) idx -= 24;
    return (char*)p + idx * 56 + 12;
}

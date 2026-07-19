void* fn_40_30B80(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 13) idx -= 13;
    return (char*)p + idx * 56 + 12;
}

void* fn_27_1C9924(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 28) + i;
    if (idx >= 4) idx -= 4;
    return (char*)p + idx * 12 + 28;
}

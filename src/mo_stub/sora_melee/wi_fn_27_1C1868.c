void* fn_27_1C1868(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 8) idx -= 8;
    return (char*)p + idx * 12 + 28;
}

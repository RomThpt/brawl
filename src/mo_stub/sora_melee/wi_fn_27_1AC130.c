void* fn_27_1AC130(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 11) idx -= 11;
    return (char*)p + idx * 16 + 28;
}

void* fn_27_11B998(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 9) idx -= 9;
    return (char*)p + idx * 4 + 12;
}

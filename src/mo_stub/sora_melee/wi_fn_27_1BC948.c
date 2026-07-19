void* fn_27_1BC948(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 10) idx -= 10;
    return (char*)p + idx * 12 + 28;
}

void* fn_27_50D4C(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 23) + i;
    if (idx >= 255) idx -= 255;
    return (char*)p + idx * 12 + 28;
}

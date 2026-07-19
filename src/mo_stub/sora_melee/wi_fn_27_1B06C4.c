void* fn_27_1B06C4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 12) idx -= 12;
    return (char*)p + idx * 52 + 12;
}

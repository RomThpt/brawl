void* fn_27_3957EC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 7) idx -= 7;
    return (char*)p + idx * 120 + 12;
}

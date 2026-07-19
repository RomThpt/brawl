void* fn_27_1B0968(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 285) idx -= 285;
    return (char*)p + idx * 4 + 12;
}

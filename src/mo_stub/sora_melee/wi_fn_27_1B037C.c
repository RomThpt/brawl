void* fn_27_1B037C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 13) idx -= 13;
    return (char*)p + idx * 96 + 12;
}

void* fn_27_1B0D5C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 10) idx -= 10;
    return (char*)p + idx * 140 + 12;
}

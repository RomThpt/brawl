void* fn_27_1B0D0C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 11) idx -= 11;
    return (char*)p + idx * 16 + 12;
}

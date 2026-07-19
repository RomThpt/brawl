void* fn_27_D9AC0(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 15) idx -= 15;
    return (char*)p + idx * 36 + 12;
}

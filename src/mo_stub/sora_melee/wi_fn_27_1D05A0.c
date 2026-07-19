void* fn_27_1D05A0(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 17) idx -= 17;
    return (char*)p + idx * 12 + 12;
}

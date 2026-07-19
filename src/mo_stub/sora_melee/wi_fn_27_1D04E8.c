void* fn_27_1D04E8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 33) idx -= 33;
    return (char*)p + idx * 12 + 12;
}

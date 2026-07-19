void* fn_27_FF04C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 4) idx -= 4;
    return (char*)p + idx * 12 + 12;
}

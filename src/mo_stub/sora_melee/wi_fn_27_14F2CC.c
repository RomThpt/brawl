void* fn_27_14F2CC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 32) idx -= 32;
    return (char*)p + idx * 48 + 12;
}

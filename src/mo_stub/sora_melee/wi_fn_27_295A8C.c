void* fn_27_295A8C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 6) idx -= 6;
    return (char*)p + idx * 4 + 12;
}

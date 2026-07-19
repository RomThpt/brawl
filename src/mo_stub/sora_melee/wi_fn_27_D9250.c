void* fn_27_D9250(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 54) idx -= 54;
    return (char*)p + idx * 48 + 12;
}

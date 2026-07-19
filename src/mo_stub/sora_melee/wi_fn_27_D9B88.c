void* fn_27_D9B88(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 29) + i;
    if (idx >= 2) idx -= 2;
    return (char*)p + idx * 72 + 12;
}

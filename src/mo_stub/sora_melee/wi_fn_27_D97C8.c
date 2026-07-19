void* fn_27_D97C8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 29) + i;
    if (idx >= 3) idx -= 3;
    return (char*)p + idx * 144 + 12;
}

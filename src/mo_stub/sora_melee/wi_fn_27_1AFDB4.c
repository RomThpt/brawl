void* fn_27_1AFDB4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 291) idx -= 291;
    return (char*)p + idx * 4 + 12;
}

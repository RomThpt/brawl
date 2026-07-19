void* fn_27_1AFABC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 15) idx -= 15;
    return (char*)p + idx * 4 + 12;
}
